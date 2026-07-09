from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def search(self, keyword: str):
        pass


    @abstractmethod
    def parse(self, html: str):
        pass
