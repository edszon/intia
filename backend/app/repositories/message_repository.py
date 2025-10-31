from typing import List, Optional

from sqlmodel import Session, select

from ..models import Message


class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self, person_id: Optional[int] = None) -> List[Message]:
        query = select(Message)
        if person_id is not None:
            query = query.where(Message.person_id == person_id)
        return self.session.exec(query).all()

    def create(self, message: Message) -> Message:
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def delete(self, message_id: int) -> bool:
        message = self.session.get(Message, message_id)
        if message:
            self.session.delete(message)
            self.session.commit()
            return True
        return False


