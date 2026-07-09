import httpx

from .urls import search_url
from .parser import parse_items


class YahooScraper:


    def search(self, keyword):

        url = search_url(keyword)


        response = httpx.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            },
            timeout=20
        )


        response.raise_for_status()


        return parse_items(
            response.text
        )
