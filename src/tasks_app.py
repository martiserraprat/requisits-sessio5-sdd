import argparse
import json
from pathlib import Path

try:
    from models import Task
except ModuleNotFoundError:
    from src.models import Task

FITXER_TASQUES = Path("data") / "tasks.json"


def assegura_fitxer(ruta: str | Path = FITXER_TASQUES) -> None:
    cami = Path(ruta)
    cami.parent.mkdir(parents=True, exist_ok=True)
    if not cami.exists():
        cami.write_text("[]", encoding="utf-8")


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
) -> Task:
    tasques = llegeix_tasques(ruta)
    tasca = Task(seguent_identificador(tasques), titol, assignatura)
    tasques.append(tasca)
    desa_tasques(tasques, ruta)
    return tasca


def llista_de_tasques(ruta: str | Path = FITXER_TASQUES) -> list[str]:
    tasques = llegeix_tasques(ruta)
    if not tasques:
        return ["Registre de tasques buit."]
    return [
        f"[{tasca.id}] {tasca.titol} ({tasca.assignatura}) - estat: {tasca.estat}"
        for tasca in tasques
    ]


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

    comandes.add_parser("list", help="Mostra totes les tasques registrades.")

    arguments = analitzador.parse_args(argv)

    if arguments.comanda == "add":
        tasca = afegeix_tasca(arguments.titol, arguments.assignatura)
        print(f"Tasca [ID: {tasca.id}] creada amb èxit")
    else:
        for linia in llista_de_tasques():
            print(linia)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
