from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import Collection
from app.infrastructure.database.models import CollectionModel


class CollectionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, collection: Collection) -> Collection:
        model = CollectionModel(
            internal_code=collection.internal_code,
            user_id=collection.user_id,
            name=collection.name,
            description=collection.description,
            active=collection.active,
            created_at=collection.created_at,
            updated_at=collection.updated_at,
        )

        self.session.add(model)
        self.session.flush()

        if model.internal_code is None:
            model.internal_code = f"COL-{model.id:06d}"
            self.session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: CollectionModel) -> Collection:
        return Collection(
            id=model.id,
            internal_code=model.internal_code,
            user_id=model.user_id,
            name=model.name,
            description=model.description,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def find_by_id(
        self,
        collection_id: int,
    ) -> Collection | None:
        model = self.session.get(
            CollectionModel,
            collection_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_user(
        self,
        user_id: int,
    ) -> list[Collection]:
        statement = (
            select(CollectionModel)
            .where(CollectionModel.user_id == user_id)
            .order_by(CollectionModel.name)
        )

        models = self.session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def save(
        self,
        collection: Collection,
    ) -> Collection:
        if collection.id is None:
            raise ValueError(
                "Não é possível atualizar uma coleção sem id."
            )

        model = self.session.get(
            CollectionModel,
            collection.id,
        )

        if model is None:
            raise ValueError(
                f"Coleção não encontrada: {collection.id}"
            )

        model.internal_code = collection.internal_code
        model.user_id = collection.user_id
        model.name = collection.name
        model.description = collection.description
        model.active = collection.active
        model.updated_at = collection.updated_at

        self.session.flush()

        return self._to_domain(model)
