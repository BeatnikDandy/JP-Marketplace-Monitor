from sqlalchemy.orm import Session

from .models import (
    User,
    Search,
    Listing,
    PriceHistory,
    Notification
)


# -----------------------
# USERS
# -----------------------

def get_or_create_user(
    db: Session,
    telegram_id: str,
    username: str = None
):

    user = (
        db.query(User)
        .filter(
            User.telegram_id == telegram_id
        )
        .first()
    )

    if user:
        return user


    user = User(
        telegram_id=telegram_id,
        username=username
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



# -----------------------
# SEARCHES
# -----------------------

def add_search(
    db: Session,
    user_id: int,
    keyword: str,
    max_price=None,
    marketplace="yahoo"
):

    search = Search(
        user_id=user_id,
        keyword=keyword,
        max_price=max_price,
        marketplace=marketplace
    )

    db.add(search)
    db.commit()
    db.refresh(search)

    return search



def get_active_searches(
    db: Session
):

    return (
        db.query(Search)
        .filter(
            Search.active == True
        )
        .all()
    )



# -----------------------
# LISTINGS
# -----------------------

def save_listing(
    db: Session,
    data: dict
):

    existing = (
        db.query(Listing)
        .filter(
            Listing.url == data["url"]
        )
        .first()
    )

    if existing:
        return existing


    listing = Listing(
        **data
    )

    db.add(listing)
    db.commit()
    db.refresh(listing)

    return listing



def listing_exists(
    db: Session,
    url: str
):

    return (
        db.query(Listing)
        .filter(
            Listing.url == url
        )
        .first()
        is not None
    )
