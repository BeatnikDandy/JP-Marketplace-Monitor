from dataclasses import dataclass, field
from datetime import datetime, timezone

from .category import CategoryKey


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class Listing:
    """Representa um anúncio encontrado em um marketplace."""

    marketplace: str
    external_id: str
    title: str
    price: int
    url: str
    category: CategoryKey
    currency: str = "JPY"
    image_url: str | None = None
    seller: str | None = None
    auction_end: datetime | None = None
    translated_title: str | None = None
    id: int | None = None
    internal_code: str | None = None
    first_seen: datetime = field(default_factory=utc_now)
    last_seen: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        self.marketplace = self.marketplace.strip().lower()
        self.external_id = self.external_id.strip()
        self.title = self.title.strip()
        self.url = self.url.strip()
        self.currency = self.currency.strip().upper()

        if isinstance(self.category, str):
            try:
                self.category = CategoryKey(self.category)
            except ValueError as exc:
                raise ValueError(
                    f"Categoria inválida: {self.category}"
                ) from exc

        if not self.marketplace:
            raise ValueError(
                "marketplace não pode ser vazio"
            )

        if not self.external_id:
            raise ValueError(
                "external_id não pode ser vazio"
            )

        if not self.title:
            raise ValueError(
                "title não pode ser vazio"
            )

        if self.price < 0:
            raise ValueError(
                "price não pode ser negativo"
            )

        if not self.url:
            raise ValueError(
                "url não pode ser vazia"
            )

        if not self.currency:
            raise ValueError(
                "currency não pode ser vazia"
            )

        if self.image_url is not None:
            self.image_url = self.image_url.strip() or None

        if self.seller is not None:
            self.seller = self.seller.strip() or None

        if self.translated_title is not None:
            self.translated_title = (
                self.translated_title.strip() or None
            )

    def update_price(self, new_price: int) -> bool:
        """Atualiza o preço e informa se ele mudou."""

        if new_price < 0:
            raise ValueError(
                "new_price não pode ser negativo"
            )

        changed = new_price != self.price

        if changed:
            self.price = new_price

        self.last_seen = utc_now()

        return changed

    def mark_seen(self) -> None:
        self.last_seen = utc_now()
