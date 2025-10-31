from typing import Optional

from pydantic import BaseModel


class PersonCreate(BaseModel):
    name: str


class PersonUpdate(BaseModel):
    name: Optional[str] = None


class PersonRead(BaseModel):
    id: int
    name: str
    pfp_image: Optional[str] = None

    class Config:
        from_attributes = True


class PersonReadWithScore(BaseModel):
    id: int
    name: str
    pfp_image: Optional[str] = None
    average_score: Optional[float] = None

    class Config:
        from_attributes = True


