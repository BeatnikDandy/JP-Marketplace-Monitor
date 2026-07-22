from app.infrastructure.database.models import (
    CollectionModel,
    KeywordModel,
    ListingModel,
    PriceHistoryModel,
    SearchModel,
    UserModel,
)
from app.infrastructure.database.session import Base, engine


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
