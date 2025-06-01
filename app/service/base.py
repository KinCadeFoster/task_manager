from typing import Any, Optional, TypeVar, Type
from sqlalchemy import select, insert, update
from app.database import async_session_maker

T = TypeVar("T")

class BaseService:
    model: Type[Any] = None

    @classmethod
    async def find_by_id(cls, model_id: int) -> Optional[Any]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = select(cls.model).where(cls.model.id == model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[Any]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by) -> list[Any]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data) -> Any:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def update_by_id(cls, object_id: int, **data) -> Optional[Any]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == object_id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()
            return await cls.find_by_id(object_id)

    @classmethod
    async def delete_by_id(cls, object_id: int) -> Optional[Any]:
        if cls.model is None:
            raise NotImplementedError("Model must be set for BaseService subclass")
        async with async_session_maker() as session:
            obj = await session.get(cls.model, object_id)
            if obj is None:
                return None
            await session.delete(obj)
            await session.commit()
            return obj