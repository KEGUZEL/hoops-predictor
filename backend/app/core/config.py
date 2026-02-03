from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "HoopsPredictor API"
    environment: str = Field("development", env="ENVIRONMENT")

    # Database
    postgres_dsn: str = Field(
        "postgresql+psycopg2://hoops:hoops@postgres:5432/hoops",
        env="POSTGRES_DSN",
    )
    mongo_dsn: str = Field("mongodb://mongo:27017", env="MONGO_DSN")
    redis_url: str = Field("redis://redis:6379/0", env="REDIS_URL")

    # RapidAPI
    rapidapi_key: str = Field("", env="RAPIDAPI_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

