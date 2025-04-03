from sqlmodel import Session
from typing import Annotated
from fastapi import Depends
from movie_service.app.v1.core.db import engine

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]