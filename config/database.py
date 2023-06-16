from abc import ABC, abstractmethod
from typing import Iterator

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

from config.settings import settings

engine = create_engine(settings.database_url, echo=settings.is_debugging)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Iterator[Session]:
    with Session() as session:
        yield session


@as_declarative()
class Entity:
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # TODO: add default value for tablename

    def __repr__(self) -> str:
        return f"<i{self.__class__.__name__}-{self.id}>"


class Repository(ABC):
    def __init__(self, session: Session):
        self._session: Session = session

    @abstractmethod
    def get(self):
        ...
