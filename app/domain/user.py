from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class User:
    telegram_id: str
    username: str | None = None
    id: int | None = None
    internal_code: str | None = None
    active: bool = True
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.telegram_id = self.telegram_id.strip()

        if not self.telegram_id:
            raise ValueError("telegram_id não pode ser vazio")

        if self.username is not None:
            self.username = self.username.strip() or None

    def deactivate(self) -> None:
        self.active = False
        self.updated_at = utc_now()

    def activate(self) -> None:
        self.active = True
        self.updated_at = utc_now()
