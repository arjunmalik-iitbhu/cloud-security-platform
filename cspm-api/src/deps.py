from collections.abc import AsyncGenerator

from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db import engine


async def get_session() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSession(engine) as session:
        yield session
