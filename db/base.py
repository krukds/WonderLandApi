from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import config

DATABASE_URL = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS.get_secret_value()}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
