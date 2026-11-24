import json
import subprocess
import sys
from pathlib import Path

ARREL = Path(__file__).resolve().parents[1]
GUIÓ = ARREL / "src" / "tasks_app.py"


def executa_cli(directori: Path, *arguments: str) -> str:
    resultat = subprocess.run(
        [sys.executable, str(GUIÓ), *arguments],
        cwd=directori,
        capture_output=True,
        text=True,
        check=True,
    )
    return resultat.stdout.strip()


def llegeix_registres(directori: Path) -> list[dict]:
    fitxer = directori / "data" / "tasks.json"
    return json.loads(fitxer.read_text(encoding="utf-8"))


def escriu_registres(directori: Path, registres: list[dict]) -> None:
    directori_dades = directori / "data"
    directori_dades.mkdir(exist_ok=True)
    fitxer = directori_dades / "tasks.json"
    fitxer.write_text(
        json.dumps(registres, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def test_gs01_creacio_correcta_duna_tasca(tmp_path: Path) -> None:
    sortida = executa_cli(
        tmp_path, "add", "--title", "Pràctica 1", "--subject", "RS"
    )

    assert sortida == "Tasca [ID: 1] creada amb èxit"
    assert llegeix_registres(tmp_path) == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_gs02_llistat_de_tasques_buit(tmp_path: Path) -> None:
    sortida = executa_cli(tmp_path, "list")

    assert sortida == "Registre de tasques buit."
    assert llegeix_registres(tmp_path) == []


def test_gs03_llistat_de_tasques_amb_registres(tmp_path: Path) -> None:
    directori_dades = tmp_path / "data"
    directori_dades.mkdir()
    (directori_dades / "tasks.json").write_text(
        json.dumps(
            [
                {
                    "id": 1,
                    "titol": "Pràctica 1",
                    "assignatura": "RS",
                    "estat": "pendent",
                },
                {
                    "id": 2,
                    "titol": "Examen parcial",
                    "assignatura": "SO",
                    "estat": "pendent",
                },
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    sortida = executa_cli(tmp_path, "list")

    assert sortida == (
        "[1] Pràctica 1 (RS) - estat: pendent\n"
        "[2] Examen parcial (SO) - estat: pendent"
    )


def test_gs04_creacio_amb_data_limit(tmp_path: Path) -> None:
    sortida = executa_cli(
        tmp_path,
        "add",
        "--title",
        "Examen",
        "--subject",
        "SO",
        "--due",
        "2026-12-15",
    )

    assert sortida == "Tasca [ID: 1] creada amb èxit"
    assert llegeix_registres(tmp_path) == [
        {
            "id": 1,
            "titol": "Examen",
            "assignatura": "SO",
            "estat": "pendent",
            "data_limit": "2026-12-15",
        }
    ]


def test_gs05_data_limit_en_format_incorrecte(tmp_path: Path) -> None:
    sortida = executa_cli(
        tmp_path,
        "add",
        "--title",
        "Examen",
        "--subject",
        "SO",
        "--due",
        "15/12/2026",
    )

    assert sortida == "Error: la data límit ha de tenir el format YYYY-MM-DD"
    assert llegeix_registres(tmp_path) == []


def test_gs06_modificacio_correcta_del_titol(tmp_path: Path) -> None:
    escriu_registres(
        tmp_path,
        [
            {
                "id": 1,
                "titol": "Practica 1",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ],
    )

    sortida = executa_cli(
        tmp_path, "edit", "--id", "1", "--title", "Pràctica 1"
    )

    assert sortida == "Tasca [ID: 1] modificada amb èxit"
    assert llegeix_registres(tmp_path) == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "pendent",
        }
    ]


def test_gs07_modificacio_duna_tasca_inexistent(tmp_path: Path) -> None:
    escriu_registres(
        tmp_path,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ],
    )
    fitxer = tmp_path / "data" / "tasks.json"
    abans = fitxer.read_text(encoding="utf-8")

    sortida = executa_cli(
        tmp_path, "edit", "--id", "99", "--title", "Nou títol"
    )

    assert sortida == "Error: no existeix cap tasca amb ID 99"
    assert fitxer.read_text(encoding="utf-8") == abans


def test_gs08_modificacio_sense_cap_camp(tmp_path: Path) -> None:
    escriu_registres(
        tmp_path,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ],
    )
    fitxer = tmp_path / "data" / "tasks.json"
    abans = fitxer.read_text(encoding="utf-8")

    sortida = executa_cli(tmp_path, "edit", "--id", "1")

    assert sortida == "Error: cal indicar almenys un camp a modificar"
    assert fitxer.read_text(encoding="utf-8") == abans


def test_gs09_marcar_tasca_completada(tmp_path: Path) -> None:
    escriu_registres(
        tmp_path,
        [
            {
                "id": 1,
                "titol": "Pràctica 1",
                "assignatura": "RS",
                "estat": "pendent",
            }
        ],
    )

    sortida = executa_cli(tmp_path, "complete", "--id", "1")

    assert sortida == "Tasca [ID: 1] marcada com a completada"
    assert llegeix_registres(tmp_path) == [
        {
            "id": 1,
            "titol": "Pràctica 1",
            "assignatura": "RS",
            "estat": "completada",
        }
    ]


def test_gs10_completar_tasca_inexistent(tmp_path: Path) -> None:
    escriu_registres(tmp_path, [])
    fitxer = tmp_path / "data" / "tasks.json"
    abans = fitxer.read_text(encoding="utf-8")

    sortida = executa_cli(tmp_path, "complete", "--id", "5")

    assert sortida == "Error: no existeix cap tasca amb ID 5"
    assert fitxer.read_text(encoding="utf-8") == abans
