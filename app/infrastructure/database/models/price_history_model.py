from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PriceHistoryModel(Base):
    __tablename__ = "price_history"

    __table_args__ = (
        Index(
            "ix_price_history_listing_recorded",
            "listing_id",
            "recorded_at",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    listing_id: Mapped[int] = mapped_column(
        ForeignKey(
            "listings_v2.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    previous_price: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )
