from typing import Any

from .base_filter import BaseFilter


class LighterFilter(BaseFilter):
    """Filtro para isqueiros."""

    ignored_terms = {
        "空箱",
        "箱のみ",
        "部品取り",
        "ケースのみ",
    }

    def is_valid(self, item: dict[str, Any]) -> bool:
        title = str(item.get("title", "")).lower()

        if not title:
            return False

        return not any(
            term.lower() in title
            for term in self.ignored_terms
        )
