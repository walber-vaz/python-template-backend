from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import registry

from app.config import settings
from app.constants import DB_NAMING_CONVENTION, Environment

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
table_registry = registry(metadata=metadata)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == Environment.LOCAL,
    future=True,
)
