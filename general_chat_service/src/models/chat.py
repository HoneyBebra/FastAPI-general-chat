import uuid

from sqlalchemy import UUID, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base import Base


class Message(Base):
    __tablename__ = "messages"

    sender_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
