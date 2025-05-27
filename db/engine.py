"""
    Функции для работы с базой данных
"""
import asyncio
from typing import Union
from .configuration import DatabaseConfig
from .base import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


class DatabaseEngine:
    def __create_async_engine(self, url: Union[str]) -> AsyncEngine:
        return create_async_engine(url=url, pool_pre_ping=True, echo=True)

    async def __proceed_schemas(self, engine: AsyncEngine, metadata: MetaData) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    def __get_session_maker(self, engine: AsyncEngine) -> sessionmaker:
        return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    def create_session(self):
        async_engine = self.__create_async_engine(DatabaseConfig().build_connection_str())
        return self.__get_session_maker(engine=async_engine)

    async def proceed_schemas(self):
        async_engine = self.__create_async_engine(DatabaseConfig().build_connection_str())
        await self.__proceed_schemas(engine=async_engine, metadata=BaseModel.metadata)
