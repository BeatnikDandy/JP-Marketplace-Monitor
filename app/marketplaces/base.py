from abc import ABC, abstractmethod
from typing import Any


class BaseMarketplace(ABC):
    """Interface comum para todos os marketplaces."""

    name: str

    @abstractmethod
    def search(self, keyword: str) -> list[dict[str, Any]]:
        """Pesquisa uma palavra-chave e retorna anúncios normalizados."""
        raise NotImplementedError
