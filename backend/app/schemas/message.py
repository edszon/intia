from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    message: str
    message_score: float = Field(ge=0.0, le=1.0)
    person_id: int


class MessageRead(BaseModel):
    id: int
    message: str
    message_score: float
    person_id: int

    class Config:
        from_attributes = True


