from ..models import Person
from ..repositories.person_repository import PersonRepository


class PersonService:
    def __init__(self, repo: PersonRepository) -> None:
        self.repo = repo

    def list_persons(self) -> list[Person]:
        return self.repo.list()

    def create_person(self, name: str, pfp_image: str | None) -> Person:
        person = Person(name=name, pfp_image=pfp_image)
        return self.repo.create(person)


