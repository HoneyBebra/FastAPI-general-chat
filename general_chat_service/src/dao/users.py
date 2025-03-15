from ..dao.base import BaseDAO
from ..models.users import Users


class UsersDAO(BaseDAO):
    def __init__(self) -> None:
        super().__init__(model=Users)
