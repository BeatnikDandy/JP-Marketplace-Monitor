from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.domain import (
    CategoryKey,
    Collection,
    Keyword,
    Search,
    User,
)
from app.infrastructure.database.models import (
    CollectionModel,
    KeywordModel,
    SearchModel,
    UserModel,
)
from app.infrastructure.database.repositories import (
    CollectionRepository,
    KeywordRepository,
    SearchRepository,
    UserRepository,
)
from app.infrastructure.database.session import Base


def run_test() -> None:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        user_repository = UserRepository(session)
        collection_repository = CollectionRepository(session)
        search_repository = SearchRepository(session)
        keyword_repository = KeywordRepository(session)

        user = user_repository.add(
            User(
                telegram_id="123456789",
                username="Gabriel",
            )
        )

        collection = collection_repository.add(
            Collection(
                user_id=user.id,
                name="Relógios",
            )
        )

        search = search_repository.add(
            Search(
                user_id=user.id,
                collection_id=collection.id,
                name="Omega De Ville",
                category=CategoryKey.WATCH,
                max_price=100000,
            )
        )

        positive_keyword = keyword_repository.add(
            Keyword(
                search_id=search.id,
                value="オメガ デビル",
            )
        )

        negative_keyword = keyword_repository.add(
            Keyword(
                search_id=search.id,
                value="ジャンク",
                negative=True,
            )
        )

        session.commit()

        assert positive_keyword.id is not None
        assert negative_keyword.id is not None

        all_keywords = keyword_repository.list_by_search(
            search.id
        )

        assert len(all_keywords) == 2

        positive_keywords = (
            keyword_repository.list_positive_by_search(
                search.id
            )
        )

        assert len(positive_keywords) == 1
        assert positive_keywords[0].value == "オメガ デビル"
        assert positive_keywords[0].negative is False

        negative_keywords = (
            keyword_repository.list_negative_by_search(
                search.id
            )
        )

        assert len(negative_keywords) == 1
        assert negative_keywords[0].value == "ジャンク"
        assert negative_keywords[0].negative is True

        found = keyword_repository.find_by_id(
            positive_keyword.id
        )

        assert found is not None
        assert found.value == "オメガ デビル"

        duplicate = keyword_repository.find_duplicate(
            search_id=search.id,
            value=" オメガ デビル ",
            negative=False,
        )

        assert duplicate is not None
        assert duplicate.id == positive_keyword.id

        positive_keyword.deactivate()

        updated = keyword_repository.save(
            positive_keyword
        )

        session.commit()

        assert updated.active is False

        active_positive = (
            keyword_repository.list_positive_by_search(
                search.id,
                active_only=True,
            )
        )

        assert len(active_positive) == 0

    print("KeywordRepository OK")


if __name__ == "__main__":
    run_test()
