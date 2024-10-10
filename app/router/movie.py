from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import db_helper
from schemas.movie import MovieRead, MovieCreate
from service.movie_service import MovieService

router = APIRouter(tags=["Movies"], prefix="/movies")  # Добавьте префикс здесь


@router.post("", response_model=MovieRead, status_code=201)
async def create_movie(
    movie_create: MovieCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = MovieService(session)
    return await service.create(movie_create)


@router.get("", response_model=List[MovieRead], status_code=200)
async def get_movies(session: AsyncSession = Depends(db_helper.session_getter)):
    service = MovieService(session)
    return await service.get_all()


@router.get("/{movie_id}", response_model=MovieRead, status_code=200)
async def get_movie(
    movie_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    service = MovieService(session)
    return await service.get_by_id(movie_id)


@router.put("/{movie_id}", response_model=MovieRead, status_code=200)
async def update_movie(
    movie_id: int,
    movie_update: MovieCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = MovieService(session)
    return await service.update(movie_id, movie_update)


@router.delete("/{movie_id}", status_code=204)
async def delete_movie(
    movie_id: int, session: AsyncSession = Depends(db_helper.session_getter)
):
    service = MovieService(session)
    await service.delete(movie_id)
    return


@router.post("/parse", response_model=List[MovieRead], status_code=201)
async def parse_and_save_movies(
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = MovieService(session)
    return (
        await service.parse_and_save_movies()
    )  # Добавляем маршрут для парсинга и сохранения фильмов
