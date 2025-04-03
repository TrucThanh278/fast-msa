from fastapi import FastAPI
from sqlmodel import create_engine
from movie_service.app.v1.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI()), echo=True)