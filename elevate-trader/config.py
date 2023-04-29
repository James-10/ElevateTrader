"""Config module for elevate_trader"""

from pydantic import (
    BaseSettings
)


class Settings(BaseSettings):
    auth_key: str
    symbols_api_key: str
    database_uri: str = ""
    jpy_multiplier: int = 1000
    other_multiplier: int = 100000
    std_lot_contract: int = 100000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


Config = Settings()