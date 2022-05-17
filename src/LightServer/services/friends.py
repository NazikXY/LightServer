import json
from typing import List

from fastapi import Depends, exceptions, status, Response

from .dependencies import get_user_from_id
from ..database import orm
from ..database.database import get_session, Session
from .. import models


class FriendsService:

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def get_list(self, user: models.User) -> List[orm.User]:
        friends_ids = json.loads(get_user_from_id(user.id, session=self._session).friend_list)

        friends_list = (
            self._session
            .query(orm.User)
            .where(orm.User.id.in_(friends_ids))
            .all()
        )
        return friends_list

    def add_friend(self, user: models.User, another_user: orm.User):
        user = get_user_from_id(user.id, session=self._session)
        friends_ids: List = json.loads(user.friend_list)

        if another_user.id in friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        friends_ids.append(another_user.id)
        user.friend_list = json.dumps(friends_ids)

        self._session.commit()

        another_user_friends_ids: List = json.loads(another_user.friend_list)

        if user.id in another_user_friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        another_user_friends_ids.append(user.id)
        another_user.friend_list = json.dumps(another_user_friends_ids)
        self._session.commit()

    def remove_friend(self, user: models.User, another_user: orm.User):
        user = get_user_from_id(user.id, session=self._session)

        friends_ids: List = json.loads(user.friend_list)

        if another_user.id not in friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        friends_ids.remove(another_user.id)

        user.friend_list = json.dumps(friends_ids)
        self._session.commit()

        another_user_friends_ids: List = json.loads(another_user.friend_list)

        if user.id not in another_user_friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        another_user_friends_ids.remove(user.id)
        another_user.friend_list = json.dumps(another_user_friends_ids)
        self._session.commit()

