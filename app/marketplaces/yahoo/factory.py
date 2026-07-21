from urllib.parse import urlparse

from app.domain import Listing
from app.domain.category import CategoryKey


class YahooListingFactory:
    @staticmethod
    def from_dict(
        data: dict,
        *,
        category: CategoryKey,
    ) -> Listing:

        url = str(data["url"]).strip()

        external_id = urlparse(url).path.rstrip("/").split("/")[-1]

        return Listing(
            marketplace="yahoo",
            external_id=external_id,
            title=str(data["title"]),
            price=int(data["price"]),
            url=url,
            category=category,
            currency="JPY",
            image_url=data.get("image_url"),
            seller=data.get("seller"),
            auction_end=data.get("auction_end"),
        )
