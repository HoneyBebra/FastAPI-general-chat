from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_async_engine(settings.postgres_dsn, echo=settings.postgres_echo, future=True)
async_session = sessionmaker(  # type: ignore[call-overload, attr-defined]
    bind=engine, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
