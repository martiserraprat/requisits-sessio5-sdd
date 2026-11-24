import json


class Task:
    def __init__(
        self,
        id: int,
        titol: str,
        assignatura: str,
        estat: str = "pendent",
    ) -> None:
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }

    @classmethod
    def from_dict(cls, dades: dict[str, object]) -> "Task":
        return cls(
            id=int(dades["id"]),
            titol=str(dades["titol"]),
            assignatura=str(dades["assignatura"]),
            estat=str(dades.get("estat", "pendent")),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_json(cls, cadena: str) -> "Task":
        return cls.from_dict(json.loads(cadena))

    def __eq__(self, altre: object) -> bool:
        if not isinstance(altre, Task):
            return NotImplemented
        return self.to_dict() == altre.to_dict()
