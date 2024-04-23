from typing import TypeVar, Generic, Type, List, Any

from sqlalchemy import select, func, update, insert, delete

T = TypeVar('T')


class BaseService(Generic[T]):
    session_maker: Type[T] = None
    model: Type[T] = None

    @classmethod
    async def execute(cls, query) -> Any:
        async with cls.session_maker() as session:
            result = await session.execute(query)
            return result.scalars()

    @classmethod
    async def select_one(cls, *args_filters, **filters) -> T:
        async with cls.session_maker() as session:
            query = select(cls.model).where(*args_filters).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def select(cls, *args_filters, order_by=None, **filters) -> List[T]:
        async with cls.session_maker() as session:
            query = select(cls.model).where(*args_filters).filter_by(**filters)
            if order_by is not None:
                query = query.order_by(order_by)
            result = await session.execute(query)
            return result.scalars()

    @classmethod
    async def add(cls, **data) -> T:
        async with cls.session_maker() as session:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            return obj


    @classmethod
    async def save(cls, obj: T) -> T:
        async with cls.session_maker() as session:
            session.add(obj)
            await session.commit()
        return obj

    @classmethod
    async def update(cls, filters: dict, **data) -> bool:
        async with cls.session_maker() as session:
            query = update(cls.model).values(**data).filter_by(**filters)
            await session.execute(query)
            await session.commit()
            return True

    @classmethod
    async def update_by_id(cls, pk: int, **data) -> bool:
        return await cls.update({"id": pk}, **data)

    @classmethod
    async def delete(cls, **filter_by) -> bool:
        async with cls.session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
            return True

    @classmethod
    async def count(cls, **filters):
        async with cls.session_maker() as session:
            query = select(func.count()).select_from(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar()
