from contextlib import asynccontextmanager

from fastapi import FastAPI

from utilities.db import DefaultManager
from .settings import get_settings

app_settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the database manager
    DefaultManager.init(db_connection=app_settings.db_connection_str, echo=app_settings.log_sql_queries)

    yield

    # close the database manager engine and clean singleton object
    await DefaultManager.close()
