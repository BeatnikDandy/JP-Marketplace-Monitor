IGNORE_WORDS = [

    "ジャンク",
    "不動品",
    "部品",
    "まとめ売り",
    "セット",
    "14点",
    "動作未確認"

]


def is_valid_listing(title):

    title_lower = title.lower()


    for word in IGNORE_WORDS:

        if word.lower() in title_lower:
            return False


    return True
