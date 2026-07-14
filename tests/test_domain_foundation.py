from app.domain import (
    CATEGORIES,
    CategoryKey,
    Collection,
    User,
    get_category,
)


def test_categories() -> None:
    assert len(CATEGORIES) == 5

    watch = get_category("watch")
    lighter = get_category(CategoryKey.LIGHTER)

    assert watch.key == CategoryKey.WATCH
    assert watch.label == "Relógios"
    assert lighter.label == "Isqueiros"

    try:
        get_category("invalid")
    except ValueError:
        pass
    else:
        raise AssertionError("Categoria inválida deveria gerar ValueError")


def test_user() -> None:
    user = User(
        telegram_id=" 123456789 ",
        username=" gabriel ",
    )

    assert user.telegram_id == "123456789"
    assert user.username == "gabriel"
    assert user.active is True

    user.deactivate()
    assert user.active is False

    user.activate()
    assert user.active is True


def test_collection() -> None:
    collection = Collection(
        user_id=1,
        name=" Relógios Vintage ",
        description=" Minha coleção principal ",
    )

    assert collection.name == "Relógios Vintage"
    assert collection.description == "Minha coleção principal"

    collection.rename("Câmeras Analógicas")
    assert collection.name == "Câmeras Analógicas"

    collection.deactivate()
    assert collection.active is False


def main() -> None:
    test_categories()
    test_user()
    test_collection()

    print("Fundação do domínio OK")


if __name__ == "__main__":
    main()
