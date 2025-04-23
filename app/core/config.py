from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    environment: str = "development"
    project_name: str = "SGIO"
    api_v1_str: str = "/api/v1"
    jwt_secret: str
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
