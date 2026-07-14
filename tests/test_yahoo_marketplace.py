from app.marketplaces.yahoo import YahooMarketplace


def main() -> None:
    marketplace = YahooMarketplace()

    items = marketplace.search("オメガ デビル")

    assert isinstance(items, list)
    assert len(items) > 0

    first_item = items[0]

    required_fields = {
        "title",
        "price",
        "url",
        "marketplace",
    }

    assert required_fields.issubset(first_item)
    assert first_item["marketplace"] == "yahoo"
    assert isinstance(first_item["price"], int)
    assert first_item["url"]

    print(f"Yahoo Marketplace OK: {len(items)} anúncios")
    print(first_item)


if __name__ == "__main__":
    main()
