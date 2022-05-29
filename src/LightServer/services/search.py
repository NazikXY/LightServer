from typing import List

from fastapi import Depends, exceptions, status

from ..database import orm
from ..database.database import Session, get_session

from sqlalchemy import func

import LightServer.models as models


class SearchService:

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def by_login(self, login: str) -> orm.User:
        another_user = (
            self._session
                .query(orm.User)
                .filter(orm.User.login == func.lower(login))
                .first()
        )
        if not another_user:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                           detail="User with such login can`t be found")
        return another_user

    def by_tags(self, tag_list: List[models.Tag]) -> List[orm.Post]:
        posts_with_tag: List[orm.PostTag] = (
            self._session
                .query(orm.PostTag)
                .filter(orm.PostTag.tag_id.in_([item.id for item in tag_list]))
                .all()
        )

        if not posts_with_tag:
            return []

        return [item.post for item in posts_with_tag]


