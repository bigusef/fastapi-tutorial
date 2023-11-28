from typing import AsyncIterator

from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from starlette import status
from uvicorn.config import logger


class AsyncDatabaseManager:
    __engine: AsyncEngine | None = None
    __session_factory: async_sessionmaker[AsyncSession] | None = None

    def init(self, db_connection: str, echo: bool):
        logger.info("initiate Engine and Session Factory instance an main singleton instance .....")

        self.__engine = create_async_engine(db_connection, echo=echo, future=True)
        self.__session_factory = async_sessionmaker(self.__engine, expire_on_commit=False)

    async def close(self) -> None:
        if self.__engine is None:
            logger.error("Closing the database manager, in spite of there are no active engine")
            return

        logger.info("Closing Active Engine .....")
        await self.__engine.dispose()
        self.__engine = None
        self.__session_factory = None

    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise IOError("DatabaseSessionManager is not initialized")

        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.rollback()
                logger.error(e)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong...")

    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Yield an async session.
        All conversations with the database are established via the session
        objects. Also. The sessions act as holding zone for ORM-mapped objects.
        """
        if self.__session_factory is None:
            raise IOError("DatabaseManager is not initialized")

        async with self.__session_factory() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(e)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong...")


DefaultManager = AsyncDatabaseManager()