from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import settings
from repository.movie_repository import MovieRepository
from typing import List, Optional

from schemas.movie import MovieCreate, MovieRead
from utils.parser.parser_factory import get_parser


class MovieService:
    def __init__(self, session: AsyncSession):
        self.repository = MovieRepository(session)
        self.parser = get_parser(settings.parser.parser_class, settings.parser.url)

    async def create(self, data: MovieCreate) -> MovieRead:
        return await self.repository.create(data)

    async def get_all(self) -> List[Optional[MovieRead]]:
        return await self.repository.get_all()

    async def get_by_id(self, movie_id: int) -> MovieRead:
        movie = await self.repository.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return MovieRead.from_orm(movie)

    async def update(self, movie_id: int, data: MovieCreate) -> MovieRead:
        movie = await self.repository.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        updated_movie = await self.repository.update(movie, data)
        return MovieRead.from_orm(updated_movie)

    async def delete(self, movie_id: int) -> bool:
        movie = await self.repository.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=404, detail="Movie not found")
        return await self.repository.delete(movie)

    async def parse_and_save_movies(self) -> List[MovieRead]:
        """Метод для парсинга и сохранения фильмов."""
        movies_data = await self.parser.parse_movies()  # Парсинг фильмов
        for movie_data in movies_data:
            await self.repository.create(movie_data)  # Сохранение в базу
        return await self.get_all()
