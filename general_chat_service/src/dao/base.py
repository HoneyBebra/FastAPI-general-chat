from typing import Any
from uuid import UUID

from sqlalchemy import Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class BaseDAO:
    def __init__(  # type: ignore[no-untyped-def]
        self, session: AsyncSession, model=None
    ) -> None:
        self.session = session

        self.model = model

    async def get_one_by_id_or_none(self, data_id: UUID) -> Any | None:
        query = select(self.model).filter_by(id=data_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_one_or_none(self, **filter_by: Any) -> Any | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, **filter_by: Any) -> Sequence:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()  # type: ignore[return-value]

    async def add(self, **values: Any):  # type: ignore[no-untyped-def]
        new_instance = self.model(**values)
        self.session.add(new_instance)
        try:
            await self.session.commit()
        except SQLAlchemyError as Ex:
            await self.session.rollback()
            raise Ex
        return new_instance
