from typing import Any

from fastapi import Depends, Request

from ..exceptions.exceptions import TokenNoFoundException
from .utils import check_expire, get_payload, get_user_by_id, get_user_id


def get_token(request: Request) -> str:
    token: str | None = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(token: str = Depends(get_token)) -> Any:
    payload = await get_payload(token)
    await check_expire(payload)
    user_id = await get_user_id(payload)
    return await get_user_by_id(user_id)
