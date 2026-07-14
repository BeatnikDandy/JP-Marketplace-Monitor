from typing import Any

from .base_filter import BaseFilter


class PenFilter(BaseFilter):
    """Filtro para canetas."""

    ignored_terms = {
        "空箱",
        "箱のみ",
        "替芯のみ",
        "部品取り",
    }

    def is_valid(self, item: dict[str, Any]) -> bool:
        title = str(item.get("title", "")).lower()

        if not title:
            return False

        return not any(
            term.lower() in title
            for term in self.ignored_terms
        )
