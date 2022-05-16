import json
from typing import List

from fastapi import Depends, exceptions, status, Response

from ..database import orm
from ..database.database import get_session, Session
from .. import models


class FriendsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self, user: models.User) -> List[orm.User]:
        friends_ids = json.loads((
            self.session
            .query(orm.User, orm.User.friend_list)
            .filter(orm.User.id == user.id)
            .first()
        ).friend_list)

        friends_list = (
            self.session
            .query(orm.User)
            .where(orm.User.id.in_(friends_ids))
            .all()
        )
        return friends_list

    def add_friend(self, user: models.User, another_user_id: int):
        user = (
             self.session
             .query(orm.User)
             .filter(orm.User.id == user.id)
             .first()
        )
        another_user = (
            self.session
                .query(orm.User)
                .filter(orm.User.id == another_user_id)
                .first()
        )

        if not another_user:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        friends_ids: List = json.loads(user.friend_list)

        if another_user_id in friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        friends_ids.append(another_user_id)
        user.friend_list = json.dumps(friends_ids)
        self.session.commit()

        another_user_friends_ids: List = json.loads(another_user.friend_list)
        if user.id in another_user_friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        another_user_friends_ids.append(user.id)
        another_user.friend_list = json.dumps(another_user_friends_ids)
        self.session.commit()

    def remove_friend(self, user: models.User, another_user_id: int):
        user = (
            self.session
                .query(orm.User)
                .filter(orm.User.id == user.id)
                .first()
        )
        friends_ids: List = json.loads(user.friend_list)

        if another_user_id not in friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        friends_ids.remove(another_user_id)

        user.friend_list = json.dumps(friends_ids)
        self.session.commit()

        another_user = (
            self.session
                .query(orm.User)
                .filter(orm.User.id == another_user_id)
                .first()
        )
        another_user_friends_ids: List = json.loads(another_user.friend_list)
        if user.id not in another_user_friends_ids:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        another_user_friends_ids.remove(user.id)
        another_user.friend_list = json.dumps(another_user_friends_ids)
        self.session.commit()

