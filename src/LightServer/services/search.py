from fastapi import Depends

from LightServer import models
from LightServer.database import orm
from LightServer.database.database import Session, get_session


class SearchService:

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def by_login(self, login: str) -> models.User:
        another_user = (
            self._session
                .query(orm.User)
                .filter(orm.User.login == login)
                .first()
        )
        return another_user
