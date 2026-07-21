from sqlalchemy.orm import sessionmaker

from app.domain import Listing
from app.domain.category import CategoryKey
from app.infrastructure.database.models import ListingModel
from app.infrastructure.database.repositories import ListingRepository
from app.infrastructure.database.session import (
    Base,
    create_database_engine,
)


def test_listing_repository() -> None:
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
        repository = ListingRepository(session)

        listing = Listing(
            marketplace="yahoo",
            external_id="j1234567890",
            title="OMEGA De Ville Vintage",
            price=25000,
            url=(
                "https://auctions.yahoo.co.jp/"
                "jp/auction/j1234567890"
            ),
            category=CategoryKey.WATCH,
        )

        created = repository.add(listing)
        session.commit()

        assert created.id is not None
        assert created.internal_code == (
            f"LST-{created.id:08d}"
        )
        assert created.marketplace == "yahoo"
        assert created.external_id == "j1234567890"
        assert created.price == 25000
        assert created.currency == "JPY"

        found_by_id = repository.find_by_id(
            created.id
        )

        assert found_by_id is not None
        assert found_by_id.id == created.id
        assert found_by_id.external_id == (
            "j1234567890"
        )

        found_by_external_id = (
            repository.find_by_external_id(
                marketplace="YAHOO",
                external_id="j1234567890",
            )
        )

        assert found_by_external_id is not None
        assert found_by_external_id.id == created.id

        price_changed = (
            found_by_external_id.update_price(22000)
        )

        assert price_changed is True
        assert found_by_external_id.price == 22000

        updated = repository.save(
            found_by_external_id
        )

        session.commit()

        assert updated.price == 22000

        reloaded = repository.find_by_id(
            created.id
        )

        assert reloaded is not None
        assert reloaded.price == 22000

        unchanged = reloaded.update_price(22000)

        assert unchanged is False

        try:
            repository.add(
                Listing(
                    marketplace="yahoo",
                    external_id="j1234567890",
                    title="Anúncio duplicado",
                    price=30000,
                    url=(
                        "https://auctions.yahoo.co.jp/"
                        "jp/auction/j1234567890"
                    ),
                    category=CategoryKey.WATCH,
                )
            )
        except ValueError as exc:
            assert "já existe" in str(exc)
        else:
            raise AssertionError(
                "O repositório deveria rejeitar "
                "um anúncio duplicado."
            )

    engine.dispose()


if __name__ == "__main__":
    test_listing_repository()
    print("ListingRepository OK")
