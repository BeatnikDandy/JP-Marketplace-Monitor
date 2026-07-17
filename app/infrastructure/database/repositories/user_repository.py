from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import User
from app.infrastructure.database.models import UserModel


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user: User) -> User:
        existing = self.find_by_telegram_id(
            user.telegram_id
        )

        if existing is not None:
            raise ValueError(
                "Já existe um usuário com esse telegram_id"
            )

        model = UserModel(
            internal_code=user.internal_code,
            telegram_id=user.telegram_id,
            username=user.username,
            active=user.active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self.session.add(model)
        self.session.flush()

        if model.internal_code is None:
            model.internal_code = f"USR-{model.id:06d}"
            self.session.flush()

        return self._to_domain(model)

    def find_by_id(self, user_id: int) -> User | None:
        model = self.session.get(
            UserModel,
            user_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def find_by_telegram_id(
        self,
        telegram_id: str,
    ) -> User | None:
        normalized_id = telegram_id.strip()

        statement = select(UserModel).where(
            UserModel.telegram_id == normalized_id
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(self) -> list[User]:
        statement = select(UserModel).order_by(
            UserModel.id
        )

        models = self.session.scalars(
            statement
        ).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def save(self, user: User) -> User:
        if user.id is None:
            raise ValueError(
                "Não é possível atualizar usuário sem id"
            )

        model = self.session.get(
            UserModel,
            user.id,
        )

        if model is None:
            raise ValueError(
                f"Usuário não encontrado: {user.id}"
            )

        model.internal_code = user.internal_code
        model.telegram_id = user.telegram_id
        model.username = user.username
        model.active = user.active
        model.updated_at = user.updated_at

        self.session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            internal_code=model.internal_code,
            telegram_id=model.telegram_id,
            username=model.username,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
