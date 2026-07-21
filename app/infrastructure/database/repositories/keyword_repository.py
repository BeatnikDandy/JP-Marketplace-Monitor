from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import Keyword
from app.infrastructure.database.models import KeywordModel


class KeywordRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, keyword: Keyword) -> Keyword:
        existing = self.find_duplicate(
            search_id=keyword.search_id,
            value=keyword.value,
            negative=keyword.negative,
        )

        if existing is not None:
            raise ValueError(
                "Essa palavra-chave já existe nesta pesquisa."
            )

        model = KeywordModel(
            search_id=keyword.search_id,
            value=keyword.value,
            negative=keyword.negative,
            active=keyword.active,
            created_at=keyword.created_at,
            updated_at=keyword.updated_at,
        )

        self.session.add(model)
        self.session.flush()

        return self._to_domain(model)

    def find_by_id(
        self,
        keyword_id: int,
    ) -> Keyword | None:
        model = self.session.get(
            KeywordModel,
            keyword_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def find_duplicate(
        self,
        search_id: int,
        value: str,
        negative: bool,
    ) -> Keyword | None:
        normalized_value = value.strip()

        statement = select(KeywordModel).where(
            KeywordModel.search_id == search_id,
            KeywordModel.value == normalized_value,
            KeywordModel.negative == negative,
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_search(
        self,
        search_id: int,
        active_only: bool = False,
    ) -> list[Keyword]:
        statement = select(KeywordModel).where(
            KeywordModel.search_id == search_id
        )

        if active_only:
            statement = statement.where(
                KeywordModel.active.is_(True)
            )

        statement = statement.order_by(
            KeywordModel.negative,
            KeywordModel.value,
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def list_positive_by_search(
        self,
        search_id: int,
        active_only: bool = True,
    ) -> list[Keyword]:
        statement = select(KeywordModel).where(
            KeywordModel.search_id == search_id,
            KeywordModel.negative.is_(False),
        )

        if active_only:
            statement = statement.where(
                KeywordModel.active.is_(True)
            )

        statement = statement.order_by(
            KeywordModel.value
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def list_negative_by_search(
        self,
        search_id: int,
        active_only: bool = True,
    ) -> list[Keyword]:
        statement = select(KeywordModel).where(
            KeywordModel.search_id == search_id,
            KeywordModel.negative.is_(True),
        )

        if active_only:
            statement = statement.where(
                KeywordModel.active.is_(True)
            )

        statement = statement.order_by(
            KeywordModel.value
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def save(self, keyword: Keyword) -> Keyword:
        if keyword.id is None:
            raise ValueError(
                "Não é possível atualizar uma palavra-chave sem id."
            )

        model = self.session.get(
            KeywordModel,
            keyword.id,
        )

        if model is None:
            raise ValueError(
                f"Palavra-chave não encontrada: {keyword.id}"
            )

        model.search_id = keyword.search_id
        model.value = keyword.value
        model.negative = keyword.negative
        model.active = keyword.active
        model.updated_at = keyword.updated_at

        self.session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: KeywordModel) -> Keyword:
        return Keyword(
            id=model.id,
            search_id=model.search_id,
            value=model.value,
            negative=model.negative,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
