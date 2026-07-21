from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SearchModel(Base):
    __tablename__ = "searches"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    internal_code: Mapped[str | None] = mapped_column(
        String(32),
        unique=True,
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    collection_id: Mapped[int | None] = mapped_column(
        ForeignKey("collections.id"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    max_price: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
