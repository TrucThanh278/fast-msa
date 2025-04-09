import uuid
from fastapi import APIRouter, status, Query
from sqlmodel import select, Session
from typing import Optional
from pydantic import ValidationError
from app.v1.core.deps import SessionDep
from app.v1.model.movie import Movie
from app.v1.schema.response import MoviePublic as MovieResponse, CustomResponse
from app.v1.schema.request import MovieTitle
from app.v1.api.crud import (
    fetch_movies,
    remove_movie,
    create_movie as create_new_movie,
    update_movie as update_new_movie,
)

from app.v1.schema.request import MovieCreate

movie_router = APIRouter(prefix="/movies", tags=["movies"])


@movie_router.get("/", response_model=CustomResponse)
async def get_movies(
    *,
    session: SessionDep,
    movie_title: MovieTitle,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = None
):
    title = movie_title.title
    try:
        results = fetch_movies(session=session, title=title)
        return CustomResponse(
            status_code=status.HTTP_200_OK,
            status="Success",
            data=results,
            message="Movies retrieved successfully",
        )
    except Exception as e:
        return CustomResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status="Error",
            message="Internal Server Error",
            errors={"Error": str(e)},
        )


@movie_router.post("/", response_model=CustomResponse)
async def create_movie(*, session: SessionDep, movie_create: MovieCreate):
    try:
        rs = create_new_movie(session=session, movie_create=movie_create)
        results = [rs]
        return CustomResponse(
            status_code=status.HTTP_201_CREATED,
            status="Success",
            data=results,
            message="Movies created successfully",
        )
    except ValidationError as e:
        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            status="Error",
            message="Bad request",
            errors={"Error": str(e)},
        )
    except Exception as e:
        return CustomResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status="Error",
            message="Internal Server Error",
            errors={"Error": str(e)},
        )


@movie_router.put("/", response_model=CustomResponse)
async def update_movie(
    *, session: SessionDep, movie_create: MovieCreate, movie_id: uuid.UUID
):
    new_movie = update_new_movie(
        session=session, movie_id=movie_id, new_movie=movie_create
    )
    results = [new_movie]
    return CustomResponse(
        status_code=status.HTTP_200_OK,
        status="Success",
        data=results,
        message="Movies updated successfully",
    )


@movie_router.delete("/", response_model=CustomResponse)
async def delete_movie(*, session: SessionDep, movie_id: uuid.UUID):
    is_deleted = remove_movie(session=session, movie_id=movie_id)
    if is_deleted:
        return CustomResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            status="Success",
            data=[],
            message="Movie deleted successfully",
        )
