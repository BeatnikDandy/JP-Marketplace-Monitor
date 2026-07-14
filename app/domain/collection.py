from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Collection:
    user_id: int
    name: str
    description: str | None = None
    id: int | None = None
    internal_code: str | None = None
    active: bool = True
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.user_id <= 0:
            raise ValueError("user_id deve ser maior que zero")

        self.name = self.name.strip()

        if not self.name:
            raise ValueError("O nome da coleção não pode ser vazio")

        if self.description is not None:
            self.description = self.description.strip() or None

    def rename(self, name: str) -> None:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("O nome da coleção não pode ser vazio")

        self.name = normalized_name
        self.updated_at = utc_now()

    def deactivate(self) -> None:
        self.active = False
        self.updated_at = utc_now()
