from typing import List, Optional

from fastapi import Depends, exceptions, status

from LightServer import models
from LightServer.database import orm
from LightServer.database.database import get_session, Session
from LightServer.services.dependencies import get_dialog_from_id, user_is_dialog_owner


class DialogService:
    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def get_list(self, user: models.User) -> List[orm.Dialog]:
        dialogs = (
            self._session
                .query(orm.Dialog)
                .filter(orm.Dialog.id.in_(
                [
                    member.dialog_id for member in
                    self._session.query(orm.Interlocutor).filter(orm.Interlocutor.member_id == user.id).all()
                ]
            )
            ).all()
        )
        return dialogs

    def get_members(self, dialog: orm.Dialog):
        interlocutors = self._session.query(orm.Interlocutor).filter(orm.Interlocutor.dialog_id == dialog.id).all()
        users = [item.member for item in interlocutors]
        return users

    def get_messages(self, dialog: orm.Dialog):
        messages = dialog.messages(self._session)
        return messages

    def create(self, user: models.User, new_dialog: models.DialogCreate, member_ids: Optional[List[int]] = None):
        dialog = orm.Dialog(**new_dialog.dict(), initiator_id=user.id)
        users = self._session.query(orm.User).filter(orm.User.id.in_(member_ids)).all()

        if len(users) < len(member_ids):
            raise exceptions.HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Some of member_id is invalid."
            )
        self._session.add(dialog)
        dialog.add_member(user, self._session)

        if member_ids:
            dialog.add_many_members(users)
        return dialog

    def add_member(self, dialog: orm.Dialog, another_user: orm.User):

        if dialog.user_is_member(another_user, session=self._session):
            raise exceptions.HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This user is already part of this dialog"
            )

        dialog.add_member(member=another_user, session=self._session)

    def leave_dialog(self, user, dialog: orm.Dialog):
        if not user_is_dialog_owner(user, dialog):
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        dialog.remove_member(user, session=self._session)

    def remove_member_from_dialog(self, user: models.User, dialog: orm.Dialog, another_user: orm.User):
        if not user_is_dialog_owner(user, dialog):
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        self.leave_dialog(another_user, dialog)

    def delete_dialog(self, user: models.User, dialog: orm.Dialog):
        if not user_is_dialog_owner(user, dialog):
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        list(map(self._session.delete, dialog.messages(self._session)))
        list(map(self._session.delete, dialog.members(self._session)))

        self._session.delete(dialog)
        self._session.commit()
