from fastapi import FastAPI
from sqlmodel import SQLModel
from app.v1.api.movie import movie_router
from app.v1.core.db import engine
from app.v1.util.middleware import ValidationErrorMiddleware
from app.v1.model.movie import Movie

SQLModel.metadata.create_all(engine)


app = FastAPI()
# app.add_middleware(ValidationErrorMiddleware)

app.include_router(movie_router)
