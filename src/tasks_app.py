import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path

try:
    from models import Task
except ModuleNotFoundError:
    from src.models import Task

FITXER_TASQUES = Path("data") / "tasks.json"
MISSATGE_DATA_INVALIDA = "Error: la data límit ha de tenir el format YYYY-MM-DD"
ESTATS_VALID = ("pendent", "completada")
MISSATGE_CAMP_BUIT = "Error: cal indicar almenys un camp a modificar"
MISSATGE_ESTAT_INVALID = "Error: l'estat ha de ser 'pendent' o 'completada'"
MISSATGE_ID_NO_EXISTEIX = "Error: no existeix cap tasca amb ID {}"


def assegura_fitxer(ruta: str | Path = FITXER_TASQUES) -> None:
    cami = Path(ruta)
    cami.parent.mkdir(parents=True, exist_ok=True)
    if not cami.exists():
        cami.write_text("[]", encoding="utf-8")


def es_data_valida(valor: str) -> bool:
    try:
        data = datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return False
    return data.isoformat() == valor


def llegeix_tasques(ruta: str | Path = FITXER_TASQUES) -> list[Task]:
    cami = Path(ruta)
    assegura_fitxer(cami)
    contingut = cami.read_text(encoding="utf-8").strip()
    dades = json.loads(contingut) if contingut else []
    return [Task.from_dict(registre) for registre in dades]


def desa_tasques(
    tasques: list[Task], ruta: str | Path = FITXER_TASQUES
) -> None:
    cami = Path(ruta)
    cami.parent.mkdir(parents=True, exist_ok=True)
    dades = [tasca.to_dict() for tasca in tasques]
    cami.write_text(
        json.dumps(dades, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def seguent_identificador(tasques: list[Task]) -> int:
    return max((tasca.id for tasca in tasques), default=0) + 1


def afegeix_tasca(
    titol: str,
    assignatura: str,
    ruta: str | Path = FITXER_TASQUES,
    data_limit: str | None = None,
) -> Task:
    tasques = llegeix_tasques(ruta)
    tasca = Task(
        seguent_identificador(tasques),
        titol,
        assignatura,
        data_limit=data_limit,
    )
    tasques.append(tasca)
    desa_tasques(tasques, ruta)
    return tasca


def edita_tasca(
    identificador: int,
    titol: str | None = None,
    assignatura: str | None = None,
    data_limit: str | None = None,
    estat: str | None = None,
    ruta: str | Path = FITXER_TASQUES,
) -> Task | None:
    tasques = llegeix_tasques(ruta)
    for tasca in tasques:
        if tasca.id != identificador:
            continue
        if titol is not None:
            tasca.titol = titol
        if assignatura is not None:
            tasca.assignatura = assignatura
        if data_limit is not None:
            tasca.data_limit = data_limit
        if estat is not None:
            tasca.estat = estat
        desa_tasques(tasques, ruta)
        return tasca
    return None


def completa_tasca(
    identificador: int, ruta: str | Path = FITXER_TASQUES
) -> Task | None:
    return edita_tasca(identificador, estat="completada", ruta=ruta)


def data_actual() -> date:
    valor = os.environ.get("TASKS_TODAY")
    if valor is None:
        return date.today()
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return date.today()


def etiqueta_per_tasca(tasca: Task, actual: date) -> str:
    if tasca.estat != "pendent" or tasca.data_limit is None:
        return ""
    try:
        limit = date.fromisoformat(tasca.data_limit)
    except ValueError:
        return ""
    dies = (limit - actual).days
    if dies < 0:
        return " [CADUCADA]"
    if dies <= 6:
        return " [URGENT]"
    return ""


def llista_de_tasques(ruta: str | Path = FITXER_TASQUES) -> list[str]:
    tasques = llegeix_tasques(ruta)
    if not tasques:
        return ["Registre de tasques buit."]
    actual = data_actual()
    linies = []
    for tasca in tasques:
        linia = (
            f"[{tasca.id}] {tasca.titol} ({tasca.assignatura})"
            f" - estat: {tasca.estat}"
        )
        if tasca.data_limit is not None:
            linia += f" - límit: {tasca.data_limit}"
        linia += etiqueta_per_tasca(tasca, actual)
        linies.append(linia)
    return linies


def main(argv: list[str] | None = None) -> int:
    analitzador = argparse.ArgumentParser(
        description="Eina CLI per gestionar tasques acadèmiques."
    )
    comandes = analitzador.add_subparsers(dest="comanda", required=True)

    afegir = comandes.add_parser("add", help="Crea una nova tasca pendent.")
    afegir.add_argument(
        "--title", required=True, dest="titol", help="Títol de la tasca."
    )
    afegir.add_argument(
        "--subject",
        required=True,
        dest="assignatura",
        help="Assignatura de la tasca.",
    )
    afegir.add_argument(
        "--due",
        help="Data límit amb format YYYY-MM-DD.",
    )

    editar = comandes.add_parser("edit", help="Modifica una tasca existent.")
    editar.add_argument(
        "--id",
        required=True,
        type=int,
        dest="identificador",
        help="ID de la tasca a modificar.",
    )
    editar.add_argument("--title", dest="titol", help="Nou títol de la tasca.")
    editar.add_argument(
        "--subject", dest="assignatura", help="Nova assignatura de la tasca."
    )
    editar.add_argument(
        "--due", help="Nova data límit amb format YYYY-MM-DD."
    )
    editar.add_argument(
        "--status",
        dest="estat",
        help="Nou estat: pendent o completada.",
    )

    completar = comandes.add_parser(
        "complete", help="Marca una tasca com a completada."
    )
    completar.add_argument(
        "--id",
        required=True,
        type=int,
        dest="identificador",
        help="ID de la tasca a completar.",
    )

    comandes.add_parser("list", help="Mostra totes les tasques registrades.")

    arguments = analitzador.parse_args(argv)

    if arguments.comanda == "add":
        assegura_fitxer()
        if arguments.due is not None and not es_data_valida(arguments.due):
            print(MISSATGE_DATA_INVALIDA)
            return 0
        tasca = afegeix_tasca(
            arguments.titol,
            arguments.assignatura,
            data_limit=arguments.due,
        )
        print(f"Tasca [ID: {tasca.id}] creada amb èxit")
    elif arguments.comanda == "edit":
        camps = (
            arguments.titol,
            arguments.assignatura,
            arguments.due,
            arguments.estat,
        )
        if all(camp is None for camp in camps):
            print(MISSATGE_CAMP_BUIT)
            return 0
        if arguments.estat is not None and arguments.estat not in ESTATS_VALID:
            print(MISSATGE_ESTAT_INVALID)
            return 0
        if arguments.due is not None and not es_data_valida(arguments.due):
            print(MISSATGE_DATA_INVALIDA)
            return 0
        tasca = edita_tasca(
            arguments.identificador,
            titol=arguments.titol,
            assignatura=arguments.assignatura,
            data_limit=arguments.due,
            estat=arguments.estat,
        )
        if tasca is None:
            print(MISSATGE_ID_NO_EXISTEIX.format(arguments.identificador))
            return 0
        print(f"Tasca [ID: {tasca.id}] modificada amb èxit")
    elif arguments.comanda == "complete":
        tasca = completa_tasca(arguments.identificador)
        if tasca is None:
            print(MISSATGE_ID_NO_EXISTEIX.format(arguments.identificador))
            return 0
        print(f"Tasca [ID: {tasca.id}] marcada com a completada")
    else:
        for linia in llista_de_tasques():
            print(linia)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
