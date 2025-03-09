import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
