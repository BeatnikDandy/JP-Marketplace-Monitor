from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import Search
from app.domain.category import CategoryKey
from app.infrastructure.database.models import SearchModel


class SearchRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, search: Search) -> Search:
        model = SearchModel(
            internal_code=search.internal_code,
            user_id=search.user_id,
            collection_id=search.collection_id,
            name=search.name,
            category=search.category.value,
            max_price=search.max_price,
            active=search.active,
            created_at=search.created_at,
            updated_at=search.updated_at,
        )

        self.session.add(model)
        self.session.flush()

        if model.internal_code is None:
            model.internal_code = f"SRC-{model.id:06d}"
            self.session.flush()

        return self._to_domain(model)

    def find_by_id(
        self,
        search_id: int,
    ) -> Search | None:
        model = self.session.get(
            SearchModel,
            search_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_user(
        self,
        user_id: int,
        active_only: bool = False,
    ) -> list[Search]:
        statement = select(SearchModel).where(
            SearchModel.user_id == user_id
        )

        if active_only:
            statement = statement.where(
                SearchModel.active.is_(True)
            )

        statement = statement.order_by(
            SearchModel.name
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def list_by_collection(
        self,
        collection_id: int,
        active_only: bool = False,
    ) -> list[Search]:
        statement = select(SearchModel).where(
            SearchModel.collection_id == collection_id
        )

        if active_only:
            statement = statement.where(
                SearchModel.active.is_(True)
            )

        statement = statement.order_by(
            SearchModel.name
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def list_active(self) -> list[Search]:
        statement = (
            select(SearchModel)
            .where(SearchModel.active.is_(True))
            .order_by(
                SearchModel.user_id,
                SearchModel.name,
            )
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def save(self, search: Search) -> Search:
        if search.id is None:
            raise ValueError(
                "Não é possível atualizar uma pesquisa sem id."
            )

        model = self.session.get(
            SearchModel,
            search.id,
        )

        if model is None:
            raise ValueError(
                f"Pesquisa não encontrada: {search.id}"
            )

        model.internal_code = search.internal_code
        model.user_id = search.user_id
        model.collection_id = search.collection_id
        model.name = search.name
        model.category = search.category.value
        model.max_price = search.max_price
        model.active = search.active
        model.updated_at = search.updated_at

        self.session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: SearchModel) -> Search:
        return Search(
            id=model.id,
            internal_code=model.internal_code,
            user_id=model.user_id,
            collection_id=model.collection_id,
            name=model.name,
            category=CategoryKey(model.category),
            max_price=model.max_price,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
