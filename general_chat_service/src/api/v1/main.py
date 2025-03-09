from fastapi import APIRouter

# Temporarily, while the files are empty
from src.core.config import settings

# from src.api.v1.chat import router as chat_router
# from src.api.v1.users import router as users_router

router = APIRouter(prefix=settings.api_v1_prefix)
# router.include_router(chat_router, prefix="/chat", tags=["chat"])
# router.include_router(users_router, prefix="/users", tags=["users"])
