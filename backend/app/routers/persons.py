import os
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session

from ..deps import get_session
from ..repositories.person_repository import PersonRepository
from ..repositories.message_repository import MessageRepository
from ..services.person_service import PersonService
from ..schemas.person import PersonCreate, PersonRead, PersonReadWithScore, PersonUpdate

router = APIRouter(prefix="/persons", tags=["persons"])

# Path to frontend static pfps directory
PFP_DIR = Path(__file__).parent.parent.parent.parent / "frontend" / "static" / "pfps"
PFP_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/", response_model=list[PersonRead])
def list_persons(session: Session = Depends(get_session)):
    service = PersonService(PersonRepository(session))
    return service.list_persons()


@router.post("/", response_model=PersonRead)
async def create_person(
    name: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    service = PersonService(PersonRepository(session))
    # Create person first to get ID (repository will auto-set pfp_image)
    person = service.create_person(name=name, pfp_image=None)
    
    # Save file as {id}.png
    file_path = PFP_DIR / f"{person.id}.png"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return person


@router.get("/{person_id}", response_model=PersonReadWithScore)
def get_person(person_id: int, session: Session = Depends(get_session)):
    person_service = PersonService(PersonRepository(session))
    person = person_service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Calculate average score from messages
    message_repo = MessageRepository(session)
    messages = message_repo.list(person_id=person_id)
    
    average_score = None
    if messages:
        total_score = sum(msg.message_score for msg in messages)
        average_score = total_score / len(messages)
    
    return PersonReadWithScore(
        id=person.id,
        name=person.name,
        pfp_image=person.pfp_image,
        average_score=average_score
    )


@router.put("/{person_id}", response_model=PersonRead)
async def update_person(
    person_id: int,
    name: str | None = Form(None),
    file: UploadFile | None = File(None),
    session: Session = Depends(get_session)
):
    service = PersonService(PersonRepository(session))
    person = service.get_person_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Update name if provided
    updated_name = name if name is not None else person.name
    
    # Save file if provided
    if file:
        file_path = PFP_DIR / f"{person_id}.png"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        pfp_image = f"/pfps/{person_id}.png"
    else:
        pfp_image = person.pfp_image
    
    # Update person
    updated_person = service.update_person(
        person_id=person_id,
        name=updated_name,
        pfp_image=pfp_image
    )
    return updated_person


@router.delete("/{person_id}", status_code=204)
def delete_person(person_id: int, session: Session = Depends(get_session)):
    service = PersonService(PersonRepository(session))
    if not service.delete_person(person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return None


