from typing import List

from sqlmodel import Session, select

from ..models import Person


class PersonRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> List[Person]:
        return self.session.exec(select(Person)).all()

    def create(self, person: Person) -> Person:
        self.session.add(person)
        self.session.commit()
        self.session.refresh(person)
        return person


