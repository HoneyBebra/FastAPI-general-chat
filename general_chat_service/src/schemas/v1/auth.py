from pydantic import BaseModel, EmailStr, Field


class SBaseAuth(BaseModel):
    email: EmailStr = Field(..., description="EMail")
    password: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Password, from 5 to 50 characters",
    )


class SBaseAuthResponse(BaseModel):
    message: str = Field(description="Response message")


class SUserRegister(SBaseAuth):
    password_check: str = Field(
        ...,
        min_length=5,
        max_length=50,
        description="Repeat password for verification, from 5 to 50 characters",
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Name, from 3 to 50 characters",
    )


class SLoginResponse(SBaseAuthResponse):
    access_token: str
    refresh_token: str | None
