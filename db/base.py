from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import config

# Адмін
ADMIN_DATABASE_URL = f"postgresql+asyncpg://admin:admin1pass@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
admin_engine = create_async_engine(ADMIN_DATABASE_URL)
admin_async_session_maker = async_sessionmaker(admin_engine, class_=AsyncSession, expire_on_commit=False)

# Користувач
USER_DATABASE_URL = f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS.get_secret_value()}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
user_engine = create_async_engine(USER_DATABASE_URL)
user_async_session_maker = async_sessionmaker(user_engine, class_=AsyncSession, expire_on_commit=False)

# Менеджер
MANAGER_DATABASE_URL = f"postgresql+asyncpg://manager:manager2pass@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
manager_engine = create_async_engine(MANAGER_DATABASE_URL)
manager_async_session_maker = async_sessionmaker(manager_engine, class_=AsyncSession, expire_on_commit=False)

# Аналітик
ANALYST_DATABASE_URL = f"postgresql+asyncpg://analyst:analyst3pass@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
analyst_engine = create_async_engine(ANALYST_DATABASE_URL)
analyst_async_session_maker = async_sessionmaker(analyst_engine, class_=AsyncSession, expire_on_commit=False)

base = declarative_base()


class Base(base):
    __abstract__ = True

    def dict(self, exclude: list = None) -> dict:
        if exclude is None:
            exclude = []
        data = self.__dict__.copy()
        for item in exclude:
            del data[item]
        return data
