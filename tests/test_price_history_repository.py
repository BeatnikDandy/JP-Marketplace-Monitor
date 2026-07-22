from sqlalchemy.orm import sessionmaker

from app.domain import Listing, PriceHistory
from app.domain.category import CategoryKey
from app.infrastructure.database.repositories import (
    ListingRepository,
    PriceHistoryRepository,
)
from app.infrastructure.database.session import (
    Base,
    create_database_engine,
)


def test_price_history_repository() -> None:
    engine = create_database_engine(
        "sqlite+pysqlite:///:memory:"
    )

    Base.metadata.create_all(bind=engine)

    TestSessionFactory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    with TestSessionFactory() as session:
        listing_repository = ListingRepository(
            session
        )
        history_repository = (
            PriceHistoryRepository(session)
        )

        listing = listing_repository.add(
            Listing(
                marketplace="yahoo",
                external_id="j1234567890",
                title="OMEGA De Ville",
                price=25000,
                url=(
                    "https://auctions.yahoo.co.jp/"
                    "jp/auction/j1234567890"
                ),
                category=CategoryKey.WATCH,
            )
        )

        initial = history_repository.add(
            PriceHistory(
                listing_id=listing.id,
                previous_price=None,
                price=25000,
            )
        )

        changed = history_repository.add(
            PriceHistory(
                listing_id=listing.id,
                previous_price=25000,
                price=20000,
            )
        )

        session.commit()

        assert initial.id is not None
        assert changed.id is not None
        assert changed.difference == -5000
        assert changed.percentage_change == -20.0

        histories = (
            history_repository.list_by_listing(
                listing.id
            )
        )

        assert len(histories) == 2
        assert histories[0].price == 25000
        assert histories[1].price == 20000

        latest = history_repository.get_latest(
            listing.id
        )

        assert latest is not None
        assert latest.price == 20000
        assert latest.previous_price == 25000

    engine.dispose()


if __name__ == "__main__":
    test_price_history_repository()
    print("PriceHistoryRepository OK")
