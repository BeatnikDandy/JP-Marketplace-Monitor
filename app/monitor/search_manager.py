from typing import Any

from app.domain import Listing, PriceHistory
from app.infrastructure.database.repositories import (
    KeywordRepository,
    ListingRepository,
    PriceHistoryRepository,
    SearchRepository,
)
from app.infrastructure.database.session import session_scope
from app.marketplaces.yahoo import YahooMarketplace
from app.marketplaces.yahoo.factory import YahooListingFactory
from app.monitor.filter import is_valid_listing


class SearchManager:
    """Coordena pesquisas, marketplaces, filtros e persistência."""

    def __init__(self) -> None:
        self.marketplaces = {
            "yahoo": YahooMarketplace(),
        }


    def search_now(
        self,
        keyword: str,
        marketplace_name: str = "yahoo",
    ) -> list[dict[str, Any]]:
        """Executa uma pesquisa manual, usada pela POC do Telegram."""

        keyword = keyword.strip()

        if not keyword:
            raise ValueError(
                "A palavra de pesquisa não pode ser vazia."
            )

        marketplace = self.marketplaces.get(
            marketplace_name
        )

        if marketplace is None:
            raise ValueError(
                f"Marketplace não suportado: {marketplace_name}"
            )

        items = marketplace.search(keyword)

        return [
            item
            for item in items
            if is_valid_listing(
                str(item.get("title", ""))
            )
        ]

    def run(self) -> dict[str, Any]:
        """
        Executa pesquisas armazenadas na nova infraestrutura.

        Nesta etapa, os anúncios são consultados e filtrados,
        mas ainda não são persistidos.
        """

        marketplace = self.marketplaces["yahoo"]

        searches_processed = 0
        keywords_processed = 0
        found = 0
        accepted = 0
        ignored = 0
        inserted = 0
        updated = 0
        unchanged = 0
        price_history_created = 0

        results: list[Listing] = []
        new_listings: list[dict[str, Any]] = []
        price_drops: list[dict[str, Any]] = []
        seen_urls: set[str] = set()

        with session_scope() as session:
            search_repository = SearchRepository(session)
            keyword_repository = KeywordRepository(session)
            listing_repository = ListingRepository(session)
            price_history_repository = (
                PriceHistoryRepository(session)
            )

            searches = search_repository.list_active()

            for search in searches:
                if search.id is None:
                    ignored += 1
                    continue

                positive_keywords = (
                    keyword_repository.list_positive_by_search(
                        search_id=search.id,
                        active_only=True,
                    )
                )

                negative_keywords = (
                    keyword_repository.list_negative_by_search(
                        search_id=search.id,
                        active_only=True,
                    )
                )

                negative_values = [
                    keyword.value.casefold()
                    for keyword in negative_keywords
                ]

                searches_processed += 1

                for keyword in positive_keywords:
                    keywords_processed += 1

                    items = marketplace.search(
                        keyword.value
                    )

                    found += len(items)

                    for item in items:
                        title = str(
                            item.get("title") or ""
                        )

                        if not is_valid_listing(title):
                            ignored += 1
                            continue

                        normalized_title = title.casefold()

                        if any(
                            negative_value in normalized_title
                            for negative_value in negative_values
                        ):
                            ignored += 1
                            continue

                        price = item.get("price")

                        if (
                            search.max_price is not None
                            and isinstance(price, (int, float))
                            and price > search.max_price
                        ):
                            ignored += 1
                            continue

                        url = str(
                            item.get("url") or ""
                        )

                        if url and url in seen_urls:
                            ignored += 1
                            continue

                        if url:
                            seen_urls.add(url)

                        listing = YahooListingFactory.from_dict(
                            item,
                            category=search.category,
                        )

                        accepted += 1

                        existing = (
                            listing_repository.find_by_external_id(
                                marketplace=listing.marketplace,
                                external_id=listing.external_id,
                            )
                        )

                        if existing is None:
                            persisted_listing = (
                                listing_repository.add(listing)
                            )

                            price_history_repository.add(
                                PriceHistory(
                                    listing_id=(
                                        persisted_listing.id
                                    ),
                                    previous_price=None,
                                    price=(
                                        persisted_listing.price
                                    ),
                                )
                            )

                            inserted += 1
                            price_history_created += 1

                            new_listings.append(
                                {
                                    "search_name": search.name,
                                    "keyword": keyword.value,
                                    "listing": persisted_listing,
                                }
                            )
                        else:
                            previous_price = existing.price

                            price_changed = (
                                existing.update_price(
                                    listing.price
                                )
                            )

                            existing.title = listing.title
                            existing.url = listing.url
                            existing.category = listing.category
                            existing.currency = listing.currency
                            existing.image_url = listing.image_url
                            existing.seller = listing.seller
                            existing.auction_end = listing.auction_end

                            persisted_listing = (
                                listing_repository.save(existing)
                            )

                            if price_changed:
                                price_history_repository.add(
                                    PriceHistory(
                                        listing_id=(
                                            persisted_listing.id
                                        ),
                                        previous_price=(
                                            previous_price
                                        ),
                                        price=(
                                            persisted_listing.price
                                        ),
                                    )
                                )

                                updated += 1
                                price_history_created += 1

                                if (
                                    persisted_listing.price
                                    < previous_price
                                ):
                                    price_drops.append(
                                        {
                                            "search_name": search.name,
                                            "keyword": keyword.value,
                                            "listing": (
                                                persisted_listing
                                            ),
                                            "previous_price": (
                                                previous_price
                                            ),
                                        }
                                    )
                            else:
                                unchanged += 1

                        results.append(persisted_listing)

        return {
            "searches_processed": searches_processed,
            "keywords_processed": keywords_processed,
            "found": found,
            "accepted": accepted,
            "ignored": ignored,
            "inserted": inserted,
            "updated": updated,
            "unchanged": unchanged,
            "price_history_created": (
                price_history_created
            ),
            "new_listings": new_listings,
            "price_drops": price_drops,
            "results": results,
        }
