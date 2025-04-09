import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from .api.v1.handlers import token_exception_handler
from .api.v1.main import router as api_v1_router
from .core.config import settings
from .core.logger import LOGGING
from .exceptions.exceptions import TokenExpiredException, TokenNoFoundException

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=f"{settings.api_v1_prefix}/openapi",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(api_v1_router)
app.mount("/static", StaticFiles(directory=settings.static_path), name="static")
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=settings.middleware_allow_origins.split(","),
    allow_credentials=True,
    allow_methods=settings.middleware_allow_methods.split(","),
    allow_headers=settings.middleware_allow_headers.split(","),
)
app.add_exception_handler(TokenExpiredException, token_exception_handler)  # type: ignore[arg-type]
app.add_exception_handler(TokenNoFoundException, token_exception_handler)  # type: ignore[arg-type]


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.app_port,
        log_config=LOGGING,
        log_level=settings.log_level,
    )

    # TODO: Add index to DB in messages
    # TODO: Make messages load lazy
    # TODO: Move authorization to a separate service
    # TODO: Code messages
