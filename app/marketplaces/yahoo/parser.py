from bs4 import BeautifulSoup
import re


def parse_items(html):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    items = []


    cards = soup.select(
        ".Product"
    )


    for card in cards:

        title = card.select_one(
            ".Product__title"
        )

        price = card.select_one(
            ".Product__price"
        )

        link = card.select_one(
            "a"
        )


        if not title or not link:
            continue


        items.append({

            "title": title.get_text(
                strip=True
            ),

            "price": extract_price(
                price.get_text(" ", strip=True)
                if price else ""
            ),

            "url": link.get(
                "href"
            ),

            "marketplace": "yahoo"

        })


    return items



def extract_price(text):

    if not text:
        return 0


    text = (
        text
        .replace(",", "")
    )


    # procura valores seguidos de 円
    prices = re.findall(
        r"(\d+)円",
        text
    )


    if prices:
        return int(prices[-1])


    return 0
