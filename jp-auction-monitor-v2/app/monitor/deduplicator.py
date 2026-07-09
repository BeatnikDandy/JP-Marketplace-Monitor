from app.database.repository import listing_exists


class Deduplicator:


    def is_new(self, db, item):

        return not listing_exists(
            db,
            item["url"]
        )
