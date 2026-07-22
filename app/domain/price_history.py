from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(slots=True)
class PriceHistory:
    listing_id: int
    price: int
    previous_price: int | None = None
    id: int | None = None
    recorded_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if self.listing_id <= 0:
            raise ValueError(
                "listing_id deve ser maior que zero"
            )

        if self.price < 0:
            raise ValueError(
                "price não pode ser negativo"
            )

        if (
            self.previous_price is not None
            and self.previous_price < 0
        ):
            raise ValueError(
                "previous_price não pode ser negativo"
            )

    @property
    def changed(self) -> bool:
        return (
            self.previous_price is not None
            and self.previous_price != self.price
        )

    @property
    def difference(self) -> int | None:
        if self.previous_price is None:
            return None

        return self.price - self.previous_price

    @property
    def percentage_change(self) -> float | None:
        if (
            self.previous_price is None
            or self.previous_price == 0
        ):
            return None

        return (
            (self.price - self.previous_price)
            / self.previous_price
            * 100
        )
