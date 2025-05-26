from sqlalchemy import select, insert, update, delete

from app.database import async_session_maker


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def update_by_id(cls, object_id: int, **data):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == object_id)
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)
            await session.commit()
            result = await session.execute(
                select(cls.model).where(cls.model.id == object_id)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, object_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == object_id)
            await session.execute(query)
            await session.commit()