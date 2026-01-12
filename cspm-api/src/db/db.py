from sqlalchemy.ext.asyncio import create_async_engine
from src.config import get_settings

settings = get_settings()
postgres_user = settings.postgres_user
postgres_password = settings.postgres_password
postgres_host = settings.postgres_host
postgres_port = settings.postgres_port
postgres_db = settings.postgres_db

_DATABASE_URI = f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

engine = create_async_engine(str(_DATABASE_URI), echo=True)
