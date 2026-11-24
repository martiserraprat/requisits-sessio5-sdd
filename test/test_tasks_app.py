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
