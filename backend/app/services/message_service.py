from ..models import Message
from ..repositories.message_repository import MessageRepository


class MessageService:
    def __init__(self, repo: MessageRepository) -> None:
        self.repo = repo

    def list_messages(self, person_id: int | None = None) -> list[Message]:
        return self.repo.list(person_id=person_id)

    def create_message(self, message: str, message_score: float, person_id: int) -> Message:
        msg = Message(message=message, message_score=message_score, person_id=person_id)
        return self.repo.create(msg)


