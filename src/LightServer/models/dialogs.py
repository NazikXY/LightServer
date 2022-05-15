from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from LightServer import models
from LightServer.settings import settings


class BaseDialog(BaseModel):
    title: str = Field(..., max_length=settings.max_title_length)


class DialogMembers(BaseModel):
    member_id_list: int


class DialogCreate(BaseDialog):
    pass

class Dialog(BaseDialog):
    id: int
    initiator_id: int
    create_date: datetime

    class Config:
        orm_mode = True

