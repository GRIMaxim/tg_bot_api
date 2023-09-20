import os

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

db_url: str = (f"{os.getenv('PG_DRIVERNAME')}://"
               f"{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@"
               f"{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}")
engine: AsyncEngine = create_async_engine(db_url, echo=True, future=True)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех создаваемых схем данных."""

    pk: Mapped[int] = mapped_column(primary_key=True)
