from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    telegram_id = Column(
        String,
        unique=True,
        nullable=False
    )

    username = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    searches = relationship(
        "Search",
        back_populates="user"
    )



class Search(Base):

    __tablename__ = "searches"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    keyword = Column(
        String,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True
    )

    max_price = Column(Integer)

    marketplace = Column(
        String,
        default="yahoo"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    user = relationship(
        "User",
        back_populates="searches"
    )



class Listing(Base):

    __tablename__ = "listings"


    id = Column(
        Integer,
        primary_key=True
    )

    title = Column(
        String,
        nullable=False
    )

    price = Column(
        Integer,
        nullable=False
    )

    currency = Column(
        String,
        default="JPY"
    )

    url = Column(
        String,
        unique=True,
        nullable=False
    )

    marketplace = Column(
        String,
        nullable=False
    )

    image_url = Column(String)

    seller = Column(String)

    auction_end = Column(String)


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class PriceHistory(Base):

    __tablename__ = "price_history"

    id = Column(
        Integer,
        primary_key=True
    )

    listing_id = Column(
        Integer,
        ForeignKey("listings.id")
    )

    price = Column(
        Integer,
        nullable=False
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow
    )



class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    listing_id = Column(
        Integer,
        ForeignKey("listings.id")
    )

    notification_type = Column(
        String,
        nullable=False
    )

    sent_at = Column(
        DateTime,
        default=datetime.utcnow
    )
