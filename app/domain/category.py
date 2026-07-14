from dataclasses import dataclass
from enum import Enum


class CategoryKey(str, Enum):
    WATCH = "watch"
    CAMERA = "camera"
    PEN = "pen"
    LIGHTER = "lighter"
    OTHER = "other"


@dataclass(frozen=True, slots=True)
class Category:
    key: CategoryKey
    label: str
    icon: str


CATEGORIES: dict[CategoryKey, Category] = {
    CategoryKey.WATCH: Category(
        key=CategoryKey.WATCH,
        label="Relógios",
        icon="⌚",
    ),
    CategoryKey.CAMERA: Category(
        key=CategoryKey.CAMERA,
        label="Câmeras",
        icon="📷",
    ),
    CategoryKey.PEN: Category(
        key=CategoryKey.PEN,
        label="Canetas",
        icon="🖋️",
    ),
    CategoryKey.LIGHTER: Category(
        key=CategoryKey.LIGHTER,
        label="Isqueiros",
        icon="🔥",
    ),
    CategoryKey.OTHER: Category(
        key=CategoryKey.OTHER,
        label="Outros",
        icon="📦",
    ),
}


def get_category(value: str | CategoryKey) -> Category:
    try:
        key = CategoryKey(value)
    except ValueError as exc:
        raise ValueError(
            f"Categoria inválida: {value}"
        ) from exc

    return CATEGORIES[key]
