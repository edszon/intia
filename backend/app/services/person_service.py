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

    def get_person_by_id(self, person_id: int) -> Person | None:
        return self.repo.get_by_id(person_id)

    def update_person(self, person_id: int, name: str | None = None, pfp_image: str | None = None) -> Person | None:
        person = self.repo.get_by_id(person_id)
        if not person:
            return None
        if name is not None:
            person.name = name
        if pfp_image is not None:
            person.pfp_image = pfp_image
        return self.repo.update(person)

    def delete_person(self, person_id: int) -> bool:
        return self.repo.delete(person_id)


