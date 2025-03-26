from fastapi import HTTPException, status


class TokenExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )


class TokenNoFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

PasswordMismatchException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="The passwords do not match",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The token is not valid",
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User ID not found",
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient rights",
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found",
)

AuthorizationHeaderMissingException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing"
)

InvalidAuthenticationSchemeException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme"
)
