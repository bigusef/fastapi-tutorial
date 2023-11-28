from enum import StrEnum
from functools import lru_cache
from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from uvicorn.config import logger


class Profile(StrEnum):
    LOCAL = "local"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class AppLanguage(StrEnum):
    ARABIC = "ar"
    ENGLISH = "en"

    @classmethod
    def _missing_(cls, value):
        # Return the default value when an invalid value is provided
        return cls.ENGLISH


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file_encoding="utf-8")

    # Build paths inside the project like this: root_dir / 'subdir'.
    root_dir: Path = Path(__file__).parent.parent.resolve()

    active_profile: Profile

    db_dsn: PostgresDsn = Field(alias="DATABASE_URL")
    log_sql_queries: bool = Field(default=False)

    @property
    def db_connection_str(self) -> str:
        return self.db_dsn.unicode_string()


@lru_cache()
def get_settings() -> AppSettings:
    import os

    logger.info("Enter get_settings function...")
    active_profile = os.environ.get("ACTIVE_PROFILE", Profile.LOCAL)
    file_source = [".env", f".env.{active_profile}"] if active_profile != Profile.LOCAL else ".env"

    return AppSettings(active_profile=active_profile, _env_file=file_source)
