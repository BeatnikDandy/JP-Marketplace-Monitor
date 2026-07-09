from app.database.db import SessionLocal

from app.database.repository import (
    get_active_searches,
    save_listing
)

from app.auctions.yahoo.scraper import YahooScraper

from app.monitor.filter import is_valid_listing

from app.monitor.deduplicator import Deduplicator



class SearchManager:


    def __init__(self):

        self.scrapers = {
            "yahoo": YahooScraper()
        }

        self.deduplicator = Deduplicator()



    def run(self):

        db = SessionLocal()


        searches = get_active_searches(db)


        saved = 0
        ignored = 0


        for search in searches:


            scraper = self.scrapers.get(
                search.marketplace
            )


            if not scraper:
                continue


            items = scraper.search(
                search.keyword
            )


            for item in items:


                if not is_valid_listing(
                    item["title"]
                ):
                    ignored += 1
                    continue



                if not self.deduplicator.is_new(
                    db,
                    item
                ):
                    ignored += 1
                    continue



                save_listing(
                    db,
                    item
                )

                saved += 1



        db.close()


        return {
            "saved": saved,
            "ignored": ignored
        }
