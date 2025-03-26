from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..dao.base import BaseDAO
from ..db.postgres import get_session
from ..models.users import Users


class UsersDAO(BaseDAO):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(model=Users, session=session)
