from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse


async def token_exception_handler(request: Request, exc: HTTPException) -> RedirectResponse:
    return RedirectResponse(url="/auth")
