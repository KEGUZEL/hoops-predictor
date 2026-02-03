from functools import lru_cache

from pymongo import MongoClient

from app.core.config import get_settings


@lru_cache
def get_mongo_client() -> MongoClient:
    settings = get_settings()
    return MongoClient(settings.mongo_dsn)


def get_injury_collection():
    """
    Injury verilerini saklamak için basit bir koleksiyon helper'ı.
    """
    client = get_mongo_client()
    db = client["hoops"]
    return db["injury_reports"]

