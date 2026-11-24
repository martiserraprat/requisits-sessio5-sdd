\# TASKS.md - Tasks\_app



\## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.



\### Tasques d'Execució:

\- [x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02) 

\- [x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.

\- [x] Tasca 1.3: Desenvolupar Tasks\_app a `src/tasks\_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)

\- [x] Tasca 1.4: Crear test d'integració a `test/test\_tasks\_app.py` segons els escenaris GS-01, GS-02 i GS-03.

\- [x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).


## Increment 2: Data límit, modificació, completar i avisos (v2.0)
Objectiu: Ampliar Tasks_app amb data límit, edició i compleció de tasques, i etiquetes [CADUCADA]/[URGENT] al llistat.

### Tasques d'Execució:

- [ ] Tasca 2.1: Afegir el camp opcional `data_limit` al model `Task` de `src/models.py`, mantenint la compatibilitat amb tasques del JSON que no el tenen. (RF-05, RF-07)

- [ ] Tasca 2.2: Afegir l'opció `--due` al comandament `add` amb validació del format YYYY-MM-DD. (RF-05, RF-06, RF-07)

- [ ] Tasca 2.3: Crear tests de `add --due` a `test/test_tasks_app.py` segons GS-04 i GS-05.

- [ ] Tasca 2.4: Implementar el comandament `edit --id` amb les opcions `--title`, `--subject`, `--due` i `--status`. (RF-08, RF-09, RF-10, RF-11, RF-12)

- [ ] Tasca 2.5: Crear tests del comandament `edit` segons GS-06, GS-07 i GS-08.

- [ ] Tasca 2.6: Implementar el comandament `complete --id`. (RF-13, RF-14)

- [ ] Tasca 2.7: Crear tests del comandament `complete` segons GS-09 i GS-10.

- [ ] Tasca 2.8: Ampliar el comandament `list` per mostrar la data límit i les etiquetes [CADUCADA] i [URGENT]. (RF-15, RF-16, RF-17, RF-18)

- [ ] Tasca 2.9: Crear tests del llistat segons GS-11 i GS-12, fixant la data actual.

- [ ] Tasca 2.10: Verificar que tots els tests (GS-01 a GS-12) passen amb `python3 -m pytest test`.
