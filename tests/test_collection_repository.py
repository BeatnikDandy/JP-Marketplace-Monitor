from sqlalchemy.orm import sessionmaker

from app.domain import Collection, User
from app.infrastructure.database.models import (
    CollectionModel,
    UserModel,
)
from app.infrastructure.database.repositories import (
    CollectionRepository,
    UserRepository,
)
from app.infrastructure.database.session import (
    Base,
    create_database_engine,
)


def main() -> None:
    engine = create_database_engine(
        "sqlite+pysqlite:///:memory:"
    )

    Base.metadata.create_all(bind=engine)

    SessionFactory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with SessionFactory() as session:
        user_repository = UserRepository(session)
        collection_repository = CollectionRepository(session)

        user = user_repository.add(
            User(
                telegram_id="123456789",
                username="gabriel",
            )
        )

        session.commit()

        collection = collection_repository.add(
            Collection(
                user_id=user.id,
                name="Relógios",
                description="Coleção de relógios vintage",
            )
        )

        session.commit()

        assert collection.id == 1
        assert collection.internal_code == "COL-000001"

        found = collection_repository.find_by_id(1)

        assert found is not None
        assert found.name == "Relógios"

        collections = collection_repository.list_by_user(user.id)

        assert len(collections) == 1

        found.rename("Omega")

        updated = collection_repository.save(found)

        session.commit()

        assert updated.name == "Omega"

        updated.deactivate()

        updated = collection_repository.save(updated)

        session.commit()

        assert updated.active is False

    print("CollectionRepository OK")


if __name__ == "__main__":
    main()
