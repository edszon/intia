from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..deps import get_session
from ..repositories.person_repository import PersonRepository
from ..services.person_service import PersonService
from ..schemas.person import PersonCreate, PersonRead

router = APIRouter(prefix="/persons", tags=["persons"])


@router.get("/", response_model=list[PersonRead])
def list_persons(session: Session = Depends(get_session)):
    service = PersonService(PersonRepository(session))
    return service.list_persons()


@router.post("/", response_model=PersonRead)
def create_person(payload: PersonCreate, session: Session = Depends(get_session)):
    service = PersonService(PersonRepository(session))
    return service.create_person(name=payload.name, pfp_image=payload.pfp_image)


