import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.main import router as api_v1_router
from src.core.config import settings
from src.core.logger import LOGGING

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=f"{settings.api_v1_prefix}/openapi",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.app_port,
        log_config=LOGGING,
        log_level=settings.log_level,
    )
