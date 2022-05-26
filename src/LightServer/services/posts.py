from typing import List, Optional

from fastapi import Depends, exceptions, status

from .. import models
from ..database import orm
from ..database.database import get_session, Session


class PostsService:

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def create(self, user: models.User, new_post: models.PostCreate) -> orm.Post:
        post = orm.Post(**new_post.dict(), author_id=user.id)
        self._session.add(post)
        self._session.commit()
        return post

    def update(self, user: models.User, post: orm.Post, new_values: models.PostCreate) -> orm.Post:
        if post.author_id != user.id:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        self._session\
            .query(orm.Post)\
            .filter(orm.Post.id == post.id)\
            .update(new_values.dict())
        self._session.commit()
        return post

    def delete(self, user: models.User, post: orm.Post):
        if post.author_id != user.id:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        self._session.delete(post)
        self._session.commit()

    def get_user_posts(self, user: models.User) -> List[orm.Post]:
        posts = (
            self._session.query(orm.Post)
                .filter(orm.Post.author_id == user.id)
                .all()
        )
        return posts



