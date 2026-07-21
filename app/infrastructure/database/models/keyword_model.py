from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class KeywordModel(Base):
    __tablename__ = "keywords"

    __table_args__ = (
        UniqueConstraint(
            "search_id",
            "value",
            "negative",
            name="uq_keyword_search_value_negative",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    search_id: Mapped[int] = mapped_column(
        ForeignKey("searches.id"),
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    negative: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
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
