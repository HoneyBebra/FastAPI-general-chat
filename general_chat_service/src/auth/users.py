from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from ..core.config import settings
from ..dao.users import UsersDAO

# TODO: Add refresh token


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(settings.current_timezone) + timedelta(
        minutes=settings.access_token_minutes
    )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.encryption_algorithm)
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str, users_dao: UsersDAO) -> Any:
    user = await users_dao.get_one_or_none(email=email)
    if (
        not user
        or verify_password(
            plain_password=password,
            hashed_password=user.hashed_password,
        )
        is False
    ):
        return None
    return user
