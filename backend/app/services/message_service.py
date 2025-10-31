from ..models import Message
from ..repositories.message_repository import MessageRepository
from ..ai.inferir import get_negativity_gradient


class MessageService:
    def __init__(self, repo: MessageRepository) -> None:
        self.repo = repo

    def list_messages(self, person_id: int | None = None) -> list[Message]:
        return self.repo.list(person_id=person_id)

    def create_message(self, message: str, person_id: int) -> Message:
        # Classify message sentiment automatically using AI
        message_score = get_negativity_gradient(message)
        msg = Message(message=message, message_score=message_score, person_id=person_id)
        return self.repo.create(msg)

    def delete_message(self, message_id: int) -> bool:
        return self.repo.delete(message_id)


