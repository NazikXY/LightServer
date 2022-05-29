from pydantic import BaseModel, Field

from ..settings import settings


class BaseTag(BaseModel):
    title: str = Field(..., max_length=settings.blog_post_title_length)


class TagCreate(BaseTag):
    ...


class Tag(BaseTag):
    id: int

