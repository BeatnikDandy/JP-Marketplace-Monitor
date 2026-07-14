from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    key: str
    label: str


WATCH = Category("watch", "⌚ Relógios")
CAMERA = Category("camera", "📷 Câmeras")
PEN = Category("pen", "🖋️ Canetas")
LIGHTER = Category("lighter", "🔥 Isqueiros")
OTHER = Category("other", "📦 Outros")


ALL_CATEGORIES = {
    WATCH.key: WATCH,
    CAMERA.key: CAMERA,
    PEN.key: PEN,
    LIGHTER.key: LIGHTER,
    OTHER.key: OTHER,
}
