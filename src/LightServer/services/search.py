from fastapi import Depends

from ..database import orm
from ..database.database import Session, get_session

from sqlalchemy import func


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
        return another_user
