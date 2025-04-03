import uuid
from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class CustomResponse(BaseModel):
    status: str
    status_code: int
    message: str | None = None
    data: list | None = None
    errors: dict | None = None

class MoviePublic(SQLModel):
    id: uuid.UUID

    title: str = Field(max_length=255)
    description: str
    release_date: str
    genre: str
    director: str