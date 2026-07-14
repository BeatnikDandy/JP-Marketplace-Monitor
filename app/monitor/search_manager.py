from app.database.db import SessionLocal
from app.database.repository import (
    get_active_searches,
    save_listing,
)
from app.marketplaces.yahoo import YahooMarketplace
from app.monitor.deduplicator import Deduplicator
from app.monitor.filter import is_valid_listing


class SearchManager:
    """Coordena pesquisas, marketplaces, filtros e persistência."""

    def __init__(self) -> None:
        self.marketplaces = {
            "yahoo": YahooMarketplace(),
        }

        self.deduplicator = Deduplicator()

    def run(self) -> dict[str, int]:
        db = SessionLocal()

        saved = 0
        ignored = 0

        try:
            searches = get_active_searches(db)

            for search in searches:
                marketplace = self.marketplaces.get(
                    search.marketplace
                )

                if marketplace is None:
                    ignored += 1
                    continue

                items = marketplace.search(
                    search.keyword
                )

                for item in items:
                    if not is_valid_listing(
                        item["title"]
                    ):
                        ignored += 1
                        continue

                    if not self.deduplicator.is_new(
                        db,
                        item,
                    ):
                        ignored += 1
                        continue

                    save_listing(
                        db,
                        item,
                    )

                    saved += 1

            return {
                "saved": saved,
                "ignored": ignored,
            }

        finally:
            db.close()
