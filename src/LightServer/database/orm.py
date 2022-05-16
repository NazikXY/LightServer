from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from . import Base, MAX_DATA_LENGTH, MESSAGE_MAX_TEXT_LENGTH


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)

    login = Column(String(length=MAX_DATA_LENGTH), nullable=False, unique=True)
    name = Column(String(length=MAX_DATA_LENGTH), nullable=False)
    password_hash = Column(String(length=MAX_DATA_LENGTH), nullable=False)
    friend_list = Column(String, nullable=True, default='[]')


class Dialog(Base):
    __tablename__ = "dialogs"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    title = Column(String(50), nullable=False)

    initiator_id = Column(Integer, ForeignKey(User.id))
    initiator = relationship(User)

    create_date = Column(DateTime, default=datetime.utcnow())

    def remove_member(self, member: User, session):
        interlocutor = session.query(Interlocutor).filter(Interlocutor.member_id == member.id).first()
        session.delete(interlocutor)
        session.commit()

    def add_member(self, member, session):
        interlocutor = Interlocutor(dialog=self, member_id=member.id)
        session.add(interlocutor)
        session.commit()
        return interlocutor

    def add_message(self, author, text, session):
        message = Message(dialog=self, author_id=author.id, text=text)
        session.add(message)
        session.commit()
        return message

    def add_many_members(self, members_list):
        [self._session.add(Interlocutor(dialog_id=self.id, member_id=item.id)) for item in members_list]
        self._session.commit()

    def user_is_member(self, member: User, session):
        return True if member.id in [item.member_id for item in self.members(session=session)] else False

    def members(self, session):
        return session.query(Interlocutor).where(Interlocutor.dialog_id == self.id).all()

    def messages(self, session):
        return session.query(Message).where(Message.dialog_id == self.id).all()


class Interlocutor(Base):
    __tablename__ = "dialog_members"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    dialog_id = Column(Integer, ForeignKey(Dialog.id))
    dialog = relationship(Dialog, foreign_keys=[dialog_id])

    member_id = Column(Integer, ForeignKey(User.id))
    member = relationship(User, foreign_keys=[member_id])


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    dialog_id = Column(Integer, ForeignKey(Dialog.id))
    dialog = relationship(Dialog, foreign_keys=[dialog_id])

    author_id = Column(Integer, ForeignKey(User.id))
    author = relationship(User, foreign_keys=[author_id])

    created_time = Column(DateTime, default=datetime.utcnow())
    update_time = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    is_read = Column(Boolean, default=False)

    text = Column(String(MESSAGE_MAX_TEXT_LENGTH))


