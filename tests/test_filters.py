from app.filters.factory import FilterFactory


def main() -> None:
    watch_filter = FilterFactory.create("watch")
    camera_filter = FilterFactory.create("camera")
    pen_filter = FilterFactory.create("pen")
    lighter_filter = FilterFactory.create("lighter")
    fallback_filter = FilterFactory.create("unknown")

    assert type(watch_filter).__name__ == "WatchFilter"
    assert type(camera_filter).__name__ == "CameraFilter"
    assert type(pen_filter).__name__ == "PenFilter"
    assert type(lighter_filter).__name__ == "LighterFilter"
    assert type(fallback_filter).__name__ == "OtherFilter"

    assert watch_filter.is_valid({
        "title": "OMEGA DE VILLE 手巻き",
        "url": "https://example.com/watch",
    })

    assert not watch_filter.is_valid({
        "title": "OMEGA ジャンク 部品取り",
        "url": "https://example.com/junk-watch",
    })

    assert camera_filter.is_valid({
        "title": "Nikon FM2 動作未確認",
        "url": "https://example.com/camera",
    })

    assert not pen_filter.is_valid({
        "title": "モンブラン 箱のみ",
        "url": "https://example.com/pen-box",
    })

    assert lighter_filter.is_valid({
        "title": "S.T. Dupont Ligne 2 ガスライター",
        "url": "https://example.com/lighter",
    })

    print("Filtros OK")


if __name__ == "__main__":
    main()

