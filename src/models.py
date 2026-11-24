import json


class Task:
    def __init__(
        self,
        id: int,
        titol: str,
        assignatura: str,
        estat: str = "pendent",
        data_limit: str | None = None,
    ) -> None:
        self.id = id
        self.titol = titol
        self.assignatura = assignatura
        self.estat = estat
        self.data_limit = data_limit

    def to_dict(self) -> dict[str, object]:
        dades: dict[str, object] = {
            "id": self.id,
            "titol": self.titol,
            "assignatura": self.assignatura,
            "estat": self.estat,
        }
        if self.data_limit is not None:
            dades["data_limit"] = self.data_limit
        return dades

    @staticmethod
    def _normalitza_data_limit(valor: object) -> str | None:
        if valor is None or valor == "":
            return None
        return str(valor)

    @classmethod
    def from_dict(cls, dades: dict[str, object]) -> "Task":
        return cls(
            id=int(dades["id"]),
            titol=str(dades["titol"]),
            assignatura=str(dades["assignatura"]),
            estat=str(dades.get("estat", "pendent")),
            data_limit=cls._normalitza_data_limit(dades.get("data_limit")),
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
