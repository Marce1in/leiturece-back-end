from contextlib import asynccontextmanager
from typing import Annotated, Any, AsyncIterator
from fastapi import Depends

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from ...settings import config


class Base(DeclarativeBase):
    pass


class DatabaseSessionManager:
    def __init__(self, database_url: str, engine_kwargs: dict[str, Any] = {}):
        self.__engine = create_async_engine(database_url, **engine_kwargs)
        self.__sessionmaker = async_sessionmaker(autocommit=False, bind=self.__engine)

    async def close(self):
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        await self.__engine.dispose()

        self.__engine = None
        self.__sessionmaker = None

    async def get_engine(self) -> AsyncEngine | None:
        return self.__engine

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.__engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self.__engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.__sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        Session = self.__sessionmaker()
        try:
            yield Session
        except Exception:
            await Session.rollback()
            raise
        finally:
            await Session.close()


SessionManager = DatabaseSessionManager(config.DB_URL, {"echo": config.DB_ECHO})


async def get_db_session():
    async with SessionManager.session() as session:
        yield session


db_dependency = Annotated[AsyncSession, Depends(get_db_session)]
