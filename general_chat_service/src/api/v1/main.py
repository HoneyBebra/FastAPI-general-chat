from fastapi import APIRouter

# from ...api.v1.users import router as users_router
from ...api.v1.auth import router as auth_router
from ...api.v1.chat import router as chat_router

# Temporarily, while the files are empty
from ...core.config import settings

router = APIRouter(prefix=settings.api_v1_prefix)
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(chat_router, prefix="/chat", tags=["chat"])
# router.include_router(users_router, prefix="/users", tags=["users"])
