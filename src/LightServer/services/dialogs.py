from typing import List, Optional

from fastapi import Depends, exceptions, status

from LightServer import models
from LightServer.database import orm
from LightServer.database.database import get_session, Session


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

    def get_members(self, user, dialog_id):
        if not self.is_i_dialog_member(user, dialog_id):
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        interlocutors = self._session.query(orm.Interlocutor).filter(orm.Interlocutor.dialog_id == dialog_id).all()
        users = [item.member for item in interlocutors]
        return users

    def get_messages(self, user, dialog_id):
        if not self.is_i_dialog_member(user, dialog_id):
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        dialog = self._session.query(orm.Dialog).filter(orm.Dialog.id == dialog_id).first()
        messages = dialog.messages(self._session)
        return messages

    def create(self, user: models.User, new_dialog: models.DialogCreate, member_ids: Optional[List[int]] = None):
        dialog = orm.Dialog(**new_dialog.dict(), initiator_id=user.id)
        users = self._session.query(orm.User).filter(orm.User.id.in_(member_ids)).all()

        if len(users) < len(member_ids):
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                           detail="Some of member_id is invalid.")
        self._session.add(dialog)
        dialog.add_member(user, self._session)

        if member_ids:
            self.add_many_members(user, dialog.id, users)
        return dialog

    def add_many_members(self, user: models.User, dialog_id: int, members_list: List[orm.User]):
        [self._session.add(orm.Interlocutor(dialog_id=dialog_id, member_id=item.id)) for item in members_list]
        self._session.commit()

    def is_i_dialog_member(self, user: models.User, dialog_id: int):
        return True if dialog_id in (item.id for item in self.get_list(user)) else False

    def add_member(self, user: models.User, dialog_id: int, another_user_id: int):
        dialog: orm.Dialog = (
            self._session
                .query(orm.Dialog)
                .filter(orm.Dialog.id == dialog_id)
                .first()
        )
        if not dialog:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        is_i_dialog_member = dialog.user_is_member(user, session=self._session)

        if not is_i_dialog_member:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        another_user = (
            self._session
                .query(orm.User)
                .filter(orm.User.id == another_user_id)
                .first()
        )
        if not another_user:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if dialog.user_is_member(member=another_user, session=self._session):
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        dialog.add_member(member=another_user, session=self._session)

    def leave_dialog(self, user: models.User, dialog_id: int, ):
        dialog: orm.Dialog = (
            self._session
                .query(orm.Dialog)
                .filter(orm.Dialog.id == dialog_id)
                .first()
        )
        if not dialog:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        is_i_dialog_member = dialog.user_is_member(user, session=self._session)
        is_i_owner = dialog.initiator_id == user.id
        if is_i_owner:
            self.delete_dialog(user, dialog_id)

        if not is_i_dialog_member:
            raise exceptions.HTTPException(status_code=status.HTTP_409_CONFLICT)

        dialog.remove_member(user, session=self._session)

    def remove_member_from_dialog(self, user: models.User, dialog_id: int, another_user_id: int):
        dialog: orm.Dialog = (
            self._session
                .query(orm.Dialog)
                .filter(orm.Dialog.id == dialog_id)
                .first()
        )

        if not dialog:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        is_i_owner = dialog.initiator_id == user.id

        if not is_i_owner:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        another_user = (
            self._session
                .query(orm.User)
                .filter(orm.User.id == another_user_id)
                .first()
        )
        if not another_user:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        self.leave_dialog(another_user, dialog_id)

    def delete_dialog(self, user: models.User, dialog_id: int):
        dialog: orm.Dialog = (
            self._session
                .query(orm.Dialog)
                .filter(orm.Dialog.id == dialog_id)
                .first()
        )
        if not dialog:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        is_i_owner = dialog.initiator_id == user.id

        if not is_i_owner:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        list(map(self._session.delete, dialog.messages(self._session)))
        list(map(self._session.delete, dialog.members(self._session)))

        self._session.delete(dialog)
        self._session.commit()
