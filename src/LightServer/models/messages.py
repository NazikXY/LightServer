from datetime import datetime

from pydantic import BaseModel, Field

from LightServer.settings import settings


class BaseMessage(BaseModel):
    text: str = Field(..., max_length=settings.max_message_length)


class MessageCreate(BaseMessage):
    dialog_id: int = Field(..., gt=0)


class Message(BaseMessage):
    id: int
    dialog_id: int
    author_id: int = Field(..., gt=0)
    created_time: datetime
    update_time: datetime
    is_read: bool = False

    class Config:
        orm_mode = True


class MessageUpdate(BaseMessage):
    message_id: int = Field(..., gt=0)


class MessageForward(BaseModel):
    id: int = Field(..., gt=0)
    target_dialog_id: int = Field(..., gt=0)
