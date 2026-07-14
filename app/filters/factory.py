from .base_filter import BaseFilter
from .camera_filter import CameraFilter
from .lighter_filter import LighterFilter
from .other_filter import OtherFilter
from .pen_filter import PenFilter
from .watch_filter import WatchFilter


class FilterFactory:
    """Seleciona o filtro correto para cada categoria."""

    _filters: dict[str, BaseFilter] = {
        "watch": WatchFilter(),
        "camera": CameraFilter(),
        "pen": PenFilter(),
        "lighter": LighterFilter(),
        "other": OtherFilter(),
    }

    @classmethod
    def create(cls, category: str) -> BaseFilter:
        normalized_category = category.strip().lower()

        return cls._filters.get(
            normalized_category,
            cls._filters["other"],
        )
