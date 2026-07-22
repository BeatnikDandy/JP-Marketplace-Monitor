from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import PriceHistory
from app.infrastructure.database.models import (
    PriceHistoryModel,
)


class PriceHistoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(
        self,
        history: PriceHistory,
    ) -> PriceHistory:
        model = PriceHistoryModel(
            listing_id=history.listing_id,
            previous_price=history.previous_price,
            price=history.price,
            recorded_at=history.recorded_at,
        )

        self.session.add(model)
        self.session.flush()

        return self._to_domain(model)

    def find_by_id(
        self,
        history_id: int,
    ) -> PriceHistory | None:
        model = self.session.get(
            PriceHistoryModel,
            history_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_listing(
        self,
        listing_id: int,
    ) -> list[PriceHistory]:
        statement = (
            select(PriceHistoryModel)
            .where(
                PriceHistoryModel.listing_id
                == listing_id
            )
            .order_by(
                PriceHistoryModel.recorded_at,
                PriceHistoryModel.id,
            )
        )

        models = self.session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def get_latest(
        self,
        listing_id: int,
    ) -> PriceHistory | None:
        statement = (
            select(PriceHistoryModel)
            .where(
                PriceHistoryModel.listing_id
                == listing_id
            )
            .order_by(
                PriceHistoryModel.recorded_at.desc(),
                PriceHistoryModel.id.desc(),
            )
            .limit(1)
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: PriceHistoryModel,
    ) -> PriceHistory:
        return PriceHistory(
            id=model.id,
            listing_id=model.listing_id,
            previous_price=model.previous_price,
            price=model.price,
            recorded_at=model.recorded_at,
        )
