from sqlalchemy.orm import sessionmaker

from app.domain import User
from app.infrastructure.database.models import UserModel  # noqa: F401
from app.infrastructure.database.repositories import UserRepository
from app.infrastructure.database.session import (
    Base,
    create_database_engine,
)


def main() -> None:
    engine = create_database_engine(
        "sqlite+pysqlite:///:memory:"
    )

    Base.metadata.create_all(bind=engine)

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with session_factory() as session:
        repository = UserRepository(session)

        created = repository.add(
            User(
                telegram_id="123456789",
                username="gabriel",
            )
        )

        assert created.id == 1
        assert created.internal_code == "USR-000001"
        assert created.telegram_id == "123456789"
        assert created.username == "gabriel"
        assert created.active is True

        session.commit()

        found_by_id = repository.find_by_id(1)
        assert found_by_id is not None
        assert found_by_id.telegram_id == "123456789"

        found_by_telegram = (
            repository.find_by_telegram_id(
                "123456789"
            )
        )

        assert found_by_telegram is not None
        assert found_by_telegram.id == 1

        users = repository.list_all()
        assert len(users) == 1

        created.deactivate()
        updated = repository.save(created)
        session.commit()

        assert updated.active is False

        try:
            repository.add(
                User(
                    telegram_id="123456789",
                    username="duplicado",
                )
            )
        except ValueError:
            session.rollback()
        else:
            raise AssertionError(
                "Usuário duplicado deveria gerar ValueError"
            )

    print("UserRepository OK")


if __name__ == "__main__":
    main()
