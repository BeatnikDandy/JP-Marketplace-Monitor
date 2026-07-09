from .db import Base, engine
from . import models


def init_database():

    Base.metadata.create_all(
        bind=engine
    )
