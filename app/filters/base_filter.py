from abc import ABC
from typing import Any


class BaseFilter(ABC):
    """Filtro-base usado por todas as categorias."""

    def is_valid(self, item: dict[str, Any]) -> bool:
        """Retorna True quando o anúncio pode ser processado."""
        return True

