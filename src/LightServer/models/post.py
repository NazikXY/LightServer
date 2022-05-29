from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from .. import models
from ..settings import settings


class BasePost(BaseModel):
    title: str = Field(..., max_length=settings.blog_post_title_length)
    body_text: str = Field(
        ...,
        max_length=settings.blog_post_text_max_length,
        min_length=settings.blog_post_text_min_length,
    )


class PostCreate(BasePost):
    pass


class Post(BasePost):
    id: int
    author_id: int = Field(..., gt=0)
    created_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True

