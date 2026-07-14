from typing import Any

from .base_filter import BaseFilter


class WatchFilter(BaseFilter):
    """Filtro para relógios."""

    ignored_terms = {
        "ジャンク",
        "部品取り",
        "まとめ売り",
        "不動品",
    }

    def is_valid(self, item: dict[str, Any]) -> bool:
        title = str(item.get("title", "")).lower()

        if not title:
            return False

        return not any(
            term.lower() in title
            for term in self.ignored_terms
        )
