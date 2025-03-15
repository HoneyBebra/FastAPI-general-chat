from datetime import datetime
from typing import Any
from uuid import UUID

from jose import JWTError, jwt

from ..core.config import settings
from ..dao import users_dao
from ..exceptions.exceptions import (
    NoJwtException,
    NoUserIdException,
    TokenExpiredException,
    UserNotFoundException,
)


async def get_payload(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except JWTError as Ex:
        raise NoJwtException from Ex


async def check_expire(payload: dict[str, Any]) -> None:
    expire: str | None = payload.get("exp")
    if not expire:
        raise TokenExpiredException
    expire_time = datetime.fromtimestamp(int(expire), tz=settings.current_timezone)
    if expire_time < datetime.now(settings.current_timezone):
        raise TokenExpiredException


async def get_user_id(payload: dict[str, Any]) -> UUID:
    user_id: UUID | None = payload.get("sub")
    if not user_id:
        raise NoUserIdException
    return user_id


async def get_user_by_id(user_id: UUID) -> Any:
    user = await users_dao.find_one_or_none_by_id(user_id)
    if not user:
        raise UserNotFoundException
    return user
