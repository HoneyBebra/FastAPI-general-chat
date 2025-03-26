from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse

from ...auth.users import authenticate_user, create_access_token, get_password_hash
from ...dao.users import UsersDAO
from ...exceptions.exceptions import (
    IncorrectEmailOrPasswordException,
    PasswordMismatchException,
    UserAlreadyExistsException,
)
from ...schemas.v1.auth import SBaseAuth, SBaseAuthResponse, SLoginResponse, SUserRegister
from ..v1 import templates

router = APIRouter()


@router.post(
    "/register",
    response_model=SBaseAuthResponse,
    summary="User registration",
    description="User registration",
    response_description="Message or exception detail",
)
async def register_user(
    user_data: SUserRegister, users_dao: UsersDAO = Depends()
) -> SBaseAuthResponse:
    user = await users_dao.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException
    hashed_password = get_password_hash(user_data.password)
    await users_dao.add(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    return SBaseAuthResponse(message="Registration successful!")


# TODO: Rewrite
@router.post(
    "/login/",
    response_model=SLoginResponse,
    summary="User login",
    description="User login",
    response_description="Message, accesstoken and refresh token or exception detail",
)
async def auth_user(
    response: Response, user_data: SBaseAuth, users_dao: UsersDAO = Depends()
) -> SLoginResponse:
    check = await authenticate_user(
        email=user_data.email,
        password=user_data.password,
        users_dao=users_dao,
    )
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return SLoginResponse(
        access_token=access_token,
        refresh_token=None,
        message="Authentication successful!",
    )


@router.post(
    "/logout/",
    response_model=SBaseAuthResponse,
    summary="User login",
    description="User login",
    response_description="Message, accesstoken and refresh token or exception detail",
)
async def logout_user(response: Response) -> SBaseAuthResponse:
    response.delete_cookie(key="users_access_token")
    return SBaseAuthResponse(message="Logout successful!")


@router.get(
    "/",
    response_class=HTMLResponse,
    summary="Auth page",
    description="Page with authorization",
    response_description="Return html template",
)
async def get_auth_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth.html", {"request": request})
