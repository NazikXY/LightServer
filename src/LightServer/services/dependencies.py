from typing import List

from fastapi import Depends, exceptions, status, Body, Query

from .tags import TagsService
from .. import models, services
from ..database import orm
from ..database.database import get_session, Session


def get_dialog_from_id(
        dialog_id: int,
        user: models.User = Depends(services.get_current_user),
        session: Session = Depends(get_session)
):
    dialog: orm.Dialog = (
        session
            .query(orm.Dialog)
            .filter(orm.Dialog.id == dialog_id)
            .first()
    )
    if not dialog:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not dialog.user_is_member(user, session):
        raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return dialog


def get_user_from_id(
        another_user_id: int = Body(...),
        session: Session = Depends(get_session)
) -> orm.User:
    user = (
        session
            .query(orm.User)
            .filter(orm.User.id == another_user_id)
            .first()
    )
    if not user:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def user_is_dialog_owner(user: orm.User, dialog: orm.Dialog):
    return dialog.initiator_id == user.id


def get_post_from_id(
        post_id: int = Query(..., gt=0),
        session: Session = Depends(get_session)
) -> orm.Post:
    post = (
        session
            .query(orm.Post)
            .filter(orm.Post.id == post_id)
            .first()
    )
    if not post:
        raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


def get_tags_from_names(tags_list: List[models.TagCreate], tags_service: TagsService = Depends()) -> List[orm.Tag]:
    return [tags_service.get_tag(tag) for tag in tags_list]

