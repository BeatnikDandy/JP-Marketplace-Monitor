BASE_URL = "https://auctions.yahoo.co.jp/search/search"


def search_url(keyword):

    return (
        f"{BASE_URL}"
        f"?p={keyword}"
    )
