from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class MovieTitle(BaseModel):
    title: str

class MovieCreate(SQLModel):
    title: str = Field(max_length=255)
    description: str
    release_date: str
    genre: str
    director: str