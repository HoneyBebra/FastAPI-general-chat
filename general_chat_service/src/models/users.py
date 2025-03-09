from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Users(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
