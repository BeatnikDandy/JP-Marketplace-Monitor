from typing import Any

from .base_filter import BaseFilter


class OtherFilter(BaseFilter):
    """Filtro genérico para categorias não especializadas."""

    def is_valid(self, item: dict[str, Any]) -> bool:
        title = str(item.get("title", "")).strip()
        url = str(item.get("url", "")).strip()

        return bool(title and url)
