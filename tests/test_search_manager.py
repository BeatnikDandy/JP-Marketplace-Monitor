from app.monitor.search_manager import SearchManager


def main() -> None:
    manager = SearchManager()
    result = manager.run()

    assert isinstance(result, dict)
    assert "saved" in result
    assert "ignored" in result
    assert isinstance(result["saved"], int)
    assert isinstance(result["ignored"], int)

    print(f"SearchManager OK: {result}")


if __name__ == "__main__":
    main()
