import uuid

from pydantic import BaseModel, Field


class SMessage(BaseModel):
    id: uuid.UUID | None = Field(default=None, description="Message ID")
    content: str = Field(description="Message content")
    sender_id: uuid.UUID | None = Field(default=None, description="Message sender ID")
