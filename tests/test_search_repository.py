from sqlalchemy.orm import sessionmaker

from app.domain import Collection, Search, User
from app.domain.category import CategoryKey
from app.infrastructure.database.models import (
    CollectionModel,
    SearchModel,
    UserModel,
)
from app.infrastructure.database.repositories import (
    CollectionRepository,
    SearchRepository,
    UserRepository,
)
from app.infrastructure.database.session import (
    Base,
    create_database_engine,
)


def main() -> None:
    engine = create_database_engine("sqlite+pysqlite:///:memory:")

    Base.metadata.create_all(bind=engine)

    SessionFactory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with SessionFactory() as session:
        user_repo = UserRepository(session)
        collection_repo = CollectionRepository(session)
        search_repo = SearchRepository(session)

        user = user_repo.add(
            User(
                telegram_id="123456789",
                username="gabriel",
            )
        )
        session.commit()

        collection = collection_repo.add(
            Collection(
                user_id=user.id,
                name="Relógios",
            )
        )
        session.commit()

        search = search_repo.add(
            Search(
                user_id=user.id,
                collection_id=collection.id,
                name="Omega De Ville",
                category=CategoryKey.WATCH,
                max_price=80000,
            )
        )
        session.commit()

        assert search.id == 1
        assert search.internal_code == "SRC-000001"

        found = search_repo.find_by_id(search.id)

        assert found is not None
        assert found.name == "Omega De Ville"

        by_user = search_repo.list_by_user(user.id)

        assert len(by_user) == 1

        by_collection = search_repo.list_by_collection(collection.id)

        assert len(by_collection) == 1

        found.set_max_price(75000)

        updated = search_repo.save(found)

        session.commit()

        assert updated.max_price == 75000

        updated.deactivate()

        updated = search_repo.save(updated)

        session.commit()

        assert updated.active is False

    print("SearchRepository OK")


if __name__ == "__main__":
    main()
