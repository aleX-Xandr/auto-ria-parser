from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import Optional

from config import DATABASE_URL


class DB:
    _engine: Optional[AsyncEngine] = None
    _async_session: Optional[AsyncSession] = None

    def __init__(self, *, debug: bool = False):
        self._debug = debug

    async def init_db(self):
        self._engine = create_async_engine(
            DATABASE_URL,
            echo=self._debug,
            future=True,
            poolclass=NullPool,
        )

        self._async_session = sessionmaker(
            self._engine, class_=AsyncSession, expire_on_commit=False
        )

    async def dispose(self):
        await self._engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        await self.init_db()
        session: AsyncSession = self._async_session()
        async with session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            else:
                await session.commit()
            finally:
                await session.close()