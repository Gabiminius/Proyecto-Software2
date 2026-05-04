from urllib.parse import urlsplit
from collections.abc import AsyncGenerator

from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.models.base import Base

settings = get_settings()


def _build_connect_args() -> dict[str, object]:
    connect_args: dict[str, object] = {
        "timeout": settings.db_connect_timeout,
        "command_timeout": settings.db_command_timeout,
    }
    host = urlsplit(settings.database_url).hostname

    # Require TLS by default for non-local PostgreSQL hosts.
    if host and host not in {"localhost", "127.0.0.1"}:
        connect_args["ssl"] = "require"

    return connect_args

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args=_build_connect_args(),
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    if not getattr(request.app.state, "db_ready", False):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable. Try again in a few seconds.",
        )

    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
