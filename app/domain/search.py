from dataclasses import dataclass, field
from datetime import datetime, timezone

from .category import CategoryKey


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Search:
    """Representa o objetivo de pesquisa de um usuário."""

    user_id: int
    name: str
    category: CategoryKey
    collection_id: int | None = None
    max_price: int | None = None
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
            raise ValueError("O nome da pesquisa não pode ser vazio")

        if isinstance(self.category, str):
            try:
                self.category = CategoryKey(self.category)
            except ValueError as exc:
                raise ValueError(
                    f"Categoria inválida: {self.category}"
                ) from exc

        if self.collection_id is not None and self.collection_id <= 0:
            raise ValueError(
                "collection_id deve ser maior que zero"
            )

        if self.max_price is not None and self.max_price < 0:
            raise ValueError(
                "max_price não pode ser negativo"
            )

    def rename(self, name: str) -> None:
        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError(
                "O nome da pesquisa não pode ser vazio"
            )

        self.name = normalized_name
        self.updated_at = utc_now()

    def set_max_price(self, max_price: int | None) -> None:
        if max_price is not None and max_price < 0:
            raise ValueError(
                "max_price não pode ser negativo"
            )

        self.max_price = max_price
        self.updated_at = utc_now()

    def deactivate(self) -> None:
        self.active = False
        self.updated_at = utc_now()

    def activate(self) -> None:
        self.active = True
        self.updated_at = utc_now()
