from app.domain import (
    CategoryKey,
    Keyword,
    Listing,
    Search,
)


def test_search() -> None:
    search = Search(
        user_id=1,
        collection_id=2,
        name=" Omega De Ville Tank ",
        category="watch",
        max_price=50000,
    )

    assert search.name == "Omega De Ville Tank"
    assert search.category == CategoryKey.WATCH
    assert search.max_price == 50000
    assert search.active is True

    search.rename("Omega De Ville")
    assert search.name == "Omega De Ville"

    search.set_max_price(60000)
    assert search.max_price == 60000

    search.deactivate()
    assert search.active is False

    search.activate()
    assert search.active is True


def test_keyword() -> None:
    keyword = Keyword(
        search_id=1,
        value=" オメガ デビル ",
    )

    negative_keyword = Keyword(
        search_id=1,
        value=" ジャンク ",
        negative=True,
    )

    assert keyword.value == "オメガ デビル"
    assert keyword.negative is False

    assert negative_keyword.value == "ジャンク"
    assert negative_keyword.negative is True

    keyword.deactivate()
    assert keyword.active is False


def test_listing() -> None:
    listing = Listing(
        marketplace=" Yahoo ",
        external_id=" s1234567890 ",
        title=" OMEGA DE VILLE 手巻き ",
        price=38500,
        url=" https://auctions.yahoo.co.jp/jp/auction/s1234567890 ",
        category="watch",
        currency="jpy",
        seller=" vendedor ",
    )

    assert listing.marketplace == "yahoo"
    assert listing.external_id == "s1234567890"
    assert listing.title == "OMEGA DE VILLE 手巻き"
    assert listing.price == 38500
    assert listing.category == CategoryKey.WATCH
    assert listing.currency == "JPY"
    assert listing.seller == "vendedor"

    changed = listing.update_price(32000)

    assert changed is True
    assert listing.price == 32000

    unchanged = listing.update_price(32000)

    assert unchanged is False
    assert listing.price == 32000


def test_validation() -> None:
    try:
        Search(
            user_id=1,
            name="",
            category="watch",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Search vazia deveria gerar ValueError"
        )

    try:
        Keyword(
            search_id=1,
            value="",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Keyword vazia deveria gerar ValueError"
        )

    try:
        Listing(
            marketplace="yahoo",
            external_id="test",
            title="Teste",
            price=-1,
            url="https://example.com",
            category="other",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Preço negativo deveria gerar ValueError"
        )


def main() -> None:
    test_search()
    test_keyword()
    test_listing()
    test_validation()

    print("Núcleo de pesquisas OK")


if __name__ == "__main__":
    main()
