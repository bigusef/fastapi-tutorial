from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class APPSettings(BaseSettings):
    is_debugging: bool = Field(..., env="WSL_DEBUGGING")
    db_connection: str = f"sqlite:///{BASE_DIR}/db.sqlite3"

    @property
    def is_production(self) -> bool:
        return not self.is_debugging

    class Config:
        env_prefix = "WSL_"
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> APPSettings:
    return APPSettings()
