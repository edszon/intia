from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    message: str = Field(max_length=150, min_length=1)
    person_id: int


class MessageRead(BaseModel):
    id: int
    message: str
    message_score: float
    person_id: int

    class Config:
        from_attributes = True


