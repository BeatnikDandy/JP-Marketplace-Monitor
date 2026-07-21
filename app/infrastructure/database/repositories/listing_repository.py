from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import Listing
from app.domain.category import CategoryKey
from app.infrastructure.database.models import ListingModel


class ListingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, listing: Listing) -> Listing:
        existing = self.find_by_external_id(
            marketplace=listing.marketplace,
            external_id=listing.external_id,
        )

        if existing is not None:
            raise ValueError(
                "Esse anúncio já existe no marketplace."
            )

        model = ListingModel(
            internal_code=listing.internal_code,
            marketplace=listing.marketplace,
            external_id=listing.external_id,
            title=listing.title,
            price=listing.price,
            url=listing.url,
            category=listing.category.value,
            currency=listing.currency,
            image_url=listing.image_url,
            seller=listing.seller,
            auction_end=listing.auction_end,
            translated_title=listing.translated_title,
            first_seen=listing.first_seen,
            last_seen=listing.last_seen,
        )

        self.session.add(model)
        self.session.flush()

        if model.internal_code is None:
            model.internal_code = f"LST-{model.id:08d}"
            self.session.flush()

        return self._to_domain(model)

    def find_by_id(
        self,
        listing_id: int,
    ) -> Listing | None:
        model = self.session.get(
            ListingModel,
            listing_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def find_by_external_id(
        self,
        marketplace: str,
        external_id: str,
    ) -> Listing | None:
        statement = select(ListingModel).where(
            ListingModel.marketplace == marketplace.strip().lower(),
            ListingModel.external_id == external_id.strip(),
        )

        model = self.session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def save(self, listing: Listing) -> Listing:
        if listing.id is None:
            raise ValueError(
                "Não é possível atualizar um anúncio sem id."
            )

        model = self.session.get(
            ListingModel,
            listing.id,
        )

        if model is None:
            raise ValueError(
                f"Anúncio não encontrado: {listing.id}"
            )

        model.internal_code = listing.internal_code
        model.marketplace = listing.marketplace
        model.external_id = listing.external_id
        model.title = listing.title
        model.price = listing.price
        model.url = listing.url
        model.category = listing.category.value
        model.currency = listing.currency
        model.image_url = listing.image_url
        model.seller = listing.seller
        model.auction_end = listing.auction_end
        model.translated_title = listing.translated_title
        model.first_seen = listing.first_seen
        model.last_seen = listing.last_seen

        self.session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: ListingModel) -> Listing:
        return Listing(
            id=model.id,
            internal_code=model.internal_code,
            marketplace=model.marketplace,
            external_id=model.external_id,
            title=model.title,
            price=model.price,
            url=model.url,
            category=CategoryKey(model.category),
            currency=model.currency,
            image_url=model.image_url,
            seller=model.seller,
            auction_end=model.auction_end,
            translated_title=model.translated_title,
            first_seen=model.first_seen,
            last_seen=model.last_seen,
        )
