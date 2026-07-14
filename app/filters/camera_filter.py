from typing import Any

from .base_filter import BaseFilter


class CameraFilter(BaseFilter):
    """Filtro para câmeras e lentes."""

    ignored_terms = {
        "部品取り",
        "空箱",
        "説明書のみ",
    }

    def is_valid(self, item: dict[str, Any]) -> bool:
        title = str(item.get("title", "")).lower()

        if not title:
            return False

        return not any(
            term.lower() in title
            for term in self.ignored_terms
        )
