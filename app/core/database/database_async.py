from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from app.core.settings import settings

DATABASE_URL = settings.build_postgres_dsn_async()

engine = create_async_engine(DATABASE_URL,
                             echo=settings.db_echo,
                             pool_size=10,
                             max_overflow=10,
                             pool_timeout=30,
                             pool_recycle=60 * 30,  # Restart the pool after 30 minutes
                             )

async_session = sessionmaker(bind=engine,  # type: ignore
                             class_=AsyncSession,
                             expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
