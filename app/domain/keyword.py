from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Keyword:
    """Palavra usada para executar uma pesquisa."""

    search_id: int
    value: str
    negative: bool = False
    id: int | None = None
    active: bool = True
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.search_id <= 0:
            raise ValueError(
                "search_id deve ser maior que zero"
            )

        self.value = self.value.strip()

        if not self.value:
            raise ValueError(
                "A palavra-chave não pode ser vazia"
            )

    def deactivate(self) -> None:
        self.active = False
        self.updated_at = utc_now()

    def activate(self) -> None:
        self.active = True
        self.updated_at = utc_now()
