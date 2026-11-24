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

- [x] Tasca 2.1: Afegir el camp opcional `data_limit` al model `Task` de `src/models.py`, mantenint la compatibilitat amb tasques del JSON que no el tenen. (RF-05, RF-07)

- [x] Tasca 2.2: Afegir l'opció `--due` al comandament `add` amb validació del format YYYY-MM-DD. (RF-05, RF-06, RF-07)

- [x] Tasca 2.3: Crear tests de `add --due` a `test/test_tasks_app.py` segons GS-04 i GS-05.

- [x] Tasca 2.4: Implementar el comandament `edit --id` amb les opcions `--title`, `--subject`, `--due` i `--status`. (RF-08, RF-09, RF-10, RF-11, RF-12)

- [x] Tasca 2.5: Crear tests del comandament `edit` segons GS-06, GS-07 i GS-08.

- [x] Tasca 2.6: Implementar el comandament `complete --id`. (RF-13, RF-14)

- [x] Tasca 2.7: Crear tests del comandament `complete` segons GS-09 i GS-10.

- [x] Tasca 2.8: Ampliar el comandament `list` per mostrar la data límit i les etiquetes [CADUCADA] i [URGENT]. (RF-15, RF-16, RF-17, RF-18)

- [x] Tasca 2.9: Crear tests del llistat segons GS-11 i GS-12, fixant la data actual.

- [x] Tasca 2.10: Verificar que tots els tests (GS-01 a GS-12) passen amb `python3 -m pytest test`.

## Increment 3: Resum i filtres del llistat (v3.0)
Objectiu: Oferir modes de llistat que facilitin la consulta d'un registre de tasques gran.

### Tasques d'Execució:
- [x] Tasca 3.1: Implementar l'opció `--summary` del comandament `list`. (RF-19, RF-20, RF-21)

- [x] Tasca 3.2: Crear tests del resum segons GS-13 i GS-14, fixant la data actual.

- [x] Tasca 3.3: Implementar l'opció `--subject` del comandament `list`. (RF-22, RF-23, RF-27)

- [x] Tasca 3.4: Crear tests del filtre per assignatura segons GS-15 i GS-16.

- [ ] Tasca 3.5: Implementar l'opció `--keyword` del comandament `list` i la combinació amb `--subject`. (RF-24, RF-25, RF-26, RF-27)

- [ ] Tasca 3.6: Crear tests del filtre per paraula clau segons GS-17, GS-18 i GS-19.

- [ ] Tasca 3.7: Verificar que tots els tests (GS-01 a GS-19) passen amb `python3 -m pytest test`.