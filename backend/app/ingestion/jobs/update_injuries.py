from datetime import date

from loguru import logger

from app.core.mongo import get_injury_collection
from app.ingestion.api_clients.injury_api_client import InjuryApiClient
from app.ingestion.scrapers.espn_injury_scraper import scrape_espn_injuries
from app.ingestion.scrapers.rotowire_injury_scraper import scrape_rotowire_injuries


def run_update_injuries(target_date: date | None = None) -> None:
    """
    API + scraping kaynaklarından injury verilerini toplayıp MongoDB'ye yazar.
    """
    target_date = target_date or date.today()
    logger.info(f"Updating injuries for {target_date}")

    collection = get_injury_collection()

    # 1) RapidAPI injury servisi
    api_client = InjuryApiClient()
    try:
        api_data = api_client.get_injuries_by_date(target_date)
        for item in api_data:
            item["_source_type"] = "rapidapi"
            item["_date"] = target_date.isoformat()
            collection.insert_one(item)
        logger.info(f"Stored {len(api_data)} injury docs from RapidAPI")
    except Exception as exc:
        logger.exception(f"RapidAPI injury fetch failed: {exc}")

    # 2) ESPN
    try:
        espn_data = scrape_espn_injuries()
        for item in espn_data:
            item["_source_type"] = "espn_scraper"
            item["_date"] = target_date.isoformat()
            collection.insert_one(item)
        logger.info(f"Stored {len(espn_data)} injury docs from ESPN scraper")
    except Exception as exc:
        logger.exception(f"ESPN scraping failed: {exc}")

    # 3) Rotowire
    try:
        roto_data = scrape_rotowire_injuries()
        for item in roto_data:
            item["_source_type"] = "rotowire_scraper"
            item["_date"] = target_date.isoformat()
            collection.insert_one(item)
        logger.info(f"Stored {len(roto_data)} injury docs from Rotowire scraper")
    except Exception as exc:
        logger.exception(f"Rotowire scraping failed: {exc}")


if __name__ == "__main__":
    run_update_injuries()

