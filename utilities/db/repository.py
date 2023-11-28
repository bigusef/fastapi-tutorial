from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Sequence, Annotated

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from .setup import DefaultManager
from .entity import BaseEntity

TEntity = TypeVar("TEntity", bound=BaseEntity)


class Paginator(ABC, BaseModel):
    @property
    @abstractmethod
    def query_data(self) -> tuple[int, int]:
        ...


class OffsetLimitPaginator(Paginator):
    offset: int = Query(default=0, ge=0)
    limit: int = Query(default=10, gt=0)

    @property
    def query_data(self) -> tuple[int, int]:
        return self.limit, self.offset


class PagePaginator(Paginator):
    page: int = Query(default=1, gt=0)
    size: int = Query(default=10, le=100)

    @property
    def query_data(self) -> tuple[int, int]:
        limit = self.size * self.page
        offset = (self.page - 1) * self.size
        return limit, offset


class Repository(Generic[TEntity], ABC):
    _model: Type[TEntity]
    _session: AsyncSession

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        cls._model = cls.__orig_bases__[0].__args__[0]

    def __init__(self, session: Annotated[AsyncSession, Depends(DefaultManager.session)]):
        self._session = session

    async def count(self, *clauses: BinaryExpression) -> int:
        stmt = select(count()).select_from(self._model)
        if clauses:
            stmt.where(*clauses)

        result = await self._session.scalar(stmt)
        return result

    async def select(self, paginator: Paginator | None = None, *clauses: BinaryExpression) -> Sequence[TEntity]:
        stmt = select(self._model)

        if clauses:
            stmt.where(*clauses)

        if paginator:
            stmt.limit(paginator.query_data[0]).offset(paginator.query_data[1])

        result = await self._session.scalars(stmt.order_by(self._model.id))
        return result.all()

    async def select_all(self, paginator: Paginator | None = None) -> Sequence[TEntity]:
        stmt = select(self._model)
        if paginator:
            stmt.limit(paginator.query_data[0]).offset(paginator.query_data[1])

        result = await self._session.scalars(stmt.order_by(self._model.id))
        return result.all()

    async def select_by_id(self, pk: int) -> TEntity | None:
        return await self._session.get(self._model, pk)

    async def get_by_id(self, pk: int) -> TEntity:
        return await self._session.get_one(self._model, pk)

    async def create(self, **data) -> TEntity:
        instance = self._model(**data)
        self._session.add(instance)
        await self._session.commit()
        return instance

    async def delete(self, instance: TEntity) -> None:
        await self._session.delete(instance)
        await self._session.commit()
