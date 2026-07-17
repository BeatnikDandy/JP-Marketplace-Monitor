from app.infrastructure.database.models import UserModel  # noqa: F401
from app.infrastructure.database.session import Base, engine


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
