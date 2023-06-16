from pydantic import BaseSettings, Field, PostgresDsn


class AppEnvironment(BaseSettings):
    is_debugging: bool = Field(..., env="DEBUGGING")
    database_url: PostgresDsn

    @property
    def is_production(self) -> bool:
        return not self.is_debugging


# TODO: make sure this object is created once
settings = AppEnvironment()