import uuid
from sqlmodel import Session, select
from typing import Optional
from pydantic import ValidationError
from app.v1.model.movie import Movie
from app.v1.schema.request import MovieCreate


def get_movie_by_id(session: Session, movie_id: uuid):
    stmt = select(Movie).where(Movie.id == movie_id)
    result = session.exec(stmt).first()
    return result


def fetch_movies(session: Session, title: Optional[str] = None):
    stmt = select(Movie)

    if title:
        stmt = stmt.where(Movie.title.like(f"%{title}%"))

    results = session.exec(stmt).all()
    return results


def create_movie(session: Session, new_movies: MovieCreate):
    movie = Movie.model_validate(new_movies)

    session.add(movie)
    session.commit()
    session.refresh(movie)

    return movie


def update_movie(session: Session, new_movie: MovieCreate, movie_id: uuid):
    current_movie = get_movie_by_id(session=session, movie_id=movie_id)
    movie_data = current_movie.model_dump()
    update_movie_data = new_movie.model_dump(exclude_unset=True)
    for f in movie_data:
        if f in update_movie_data:
            setattr(current_movie, f, update_movie_data[f])
    session.add(current_movie)
    session.commit()
    session.refresh(current_movie)
    return current_movie


def remove_movie(session: Session, movie_id: uuid):
    stmt = select(Movie).where(Movie.id == movie_id)
    movie = session.exec(stmt).first()
    session.delete(movie)
    session.commit()
    return True
