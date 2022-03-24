from typing import Iterator

from sqlmodel import Session, create_engine

from .settings import get_settings


settings = get_settings()


engine = create_engine(settings.db_connection, echo=settings.is_debugging)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
