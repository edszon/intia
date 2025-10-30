from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from ..deps import get_session
from ..repositories.message_repository import MessageRepository
from ..services.message_service import MessageService
from ..schemas.message import MessageCreate, MessageRead

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=list[MessageRead])
def list_messages(
    person_id: Optional[int] = Query(default=None),
    session: Session = Depends(get_session),
):
    service = MessageService(MessageRepository(session))
    return service.list_messages(person_id=person_id)


@router.post("/", response_model=MessageRead)
def create_message(payload: MessageCreate, session: Session = Depends(get_session)):
    service = MessageService(MessageRepository(session))
    return service.create_message(
        message=payload.message,
        message_score=payload.message_score,
        person_id=payload.person_id,
    )


