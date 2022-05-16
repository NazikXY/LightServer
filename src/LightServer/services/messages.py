from fastapi import Depends, exceptions, status

from ..database import orm
from ..database.database import Session, get_session
from .. import models


class MessageService:

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def _get_message(self, id: int):
        return self._session.query(orm.Message).filter(orm.Message.id == id).first()

    def send_message(self, user: models.User, message: models.MessageCreate):
        dialog: orm.Dialog = (
            self._session
            .query(orm.Dialog)
            .filter(orm.Dialog.id == message.dialog_id)
            .first()
        )
        if not dialog:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        i_member = dialog.user_is_member(user, session=self._session)
        if not i_member:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        new_message = dialog.add_message(user, message.text, session=self._session)
        return new_message

    def edit_message(self, user: models.User, message: models.MessageUpdate):
        message_orm: orm.Message = (
            self._session
                .query(orm.Message)
                .filter(orm.Message.id == message.message_id)
                .first()
        )

        if not message_orm:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if message_orm.author_id != user.id:
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        message_orm.text = message.text
        self._session.commit()
        return message_orm

    def forward(self, message_forward: models.MessageForward):
        # message: orm.Message = self._get_message(message_forward.id)
        # self.send_message(message.author, models.MessageCreate())
        ...

    def delete_message(self, user: models.User, message_id: int):
        message: orm.Message = (
            self._session
                .query(orm.Message)
                .filter(orm.Message.id == message_id)
                .first()
        )
        if not message:
            raise exceptions.HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        dialog: orm.Dialog = (
            self._session
                .query(orm.Dialog)
                .filter(orm.Dialog.id == message.dialog_id)
                .first()
        )
        if (user.id != dialog.initiator_id) or (message.author_id != user.id):
            raise exceptions.HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        self._session.delete(message)
        self._session.commit()


