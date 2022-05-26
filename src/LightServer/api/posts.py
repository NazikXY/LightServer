from typing import List

from fastapi import APIRouter, Depends, Body
from .. import models
from ..database import orm
from ..services.auth import get_current_user
from ..services.dependencies import get_post_from_id
from ..services.posts import PostsService

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


@router.get("/{post_id}", response_model=models.Post)
def get(
        post: orm.Post = Depends(get_post_from_id)
):
    return post


@router.get("/my_posts", response_model=List[models.Post])
def get_my_posts(
        user: models.User = Depends(get_current_user),
        post_service: PostsService = Depends()
):
    return post_service.get_user_posts(user=user)


@router.post("/create", response_model=models.Post)
def create(
        post: models.PostCreate,
        user: models.User = Depends(get_current_user),
        post_service: PostsService = Depends()
):
    return post_service.create(user=user, new_post=post)


@router.patch("/update", response_model=models.Post)
def update_post(
        post: orm.Post = Depends(get_post_from_id),
        new_values: models.PostCreate = Body(...),
        user: models.User = Depends(get_current_user),
        post_service: PostsService = Depends()

):
    return post_service.update(user=user, post=post, new_values=new_values)
