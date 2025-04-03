from sqlmodel import Field
from movie_service.app.v1.model.base import CustomBaseModel

class Movie(CustomBaseModel, table=True):
    title: str = Field(max_length=255)
    description: str
    release_date: str
    genre: str
    director: str
    cast: str | None = Field(default=None)