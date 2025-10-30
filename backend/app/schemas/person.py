from typing import Optional

from pydantic import BaseModel


class PersonCreate(BaseModel):
    name: str
    pfp_image: Optional[str] = None


class PersonRead(BaseModel):
    id: int
    name: str
    pfp_image: Optional[str] = None

    class Config:
        from_attributes = True


