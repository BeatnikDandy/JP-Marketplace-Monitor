from typing import Any

import httpx

from app.marketplaces.base import BaseMarketplace

from .parser import parse_items
from .urls import search_url


class YahooMarketplace(BaseMarketplace):
    """Conector de pesquisa do Yahoo Auctions Japan."""

    name = "yahoo"

    def search(self, keyword: str) -> list[dict[str, Any]]:
        url = search_url(keyword)

        response = httpx.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            },
            timeout=30.0,
            follow_redirects=True,
        )

        response.raise_for_status()

        return parse_items(response.text)


# Alias temporário para preservar compatibilidade com código antigo.
YahooScraper = YahooMarketplace
