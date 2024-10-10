from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.movie import Movie
from typing import List, Optional

from schemas.movie import MovieCreate, MovieRead


class MovieRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: MovieCreate) -> MovieRead:
        movie = Movie(**data.dict())
        self.session.add(movie)
        await self.session.commit()
        await self.session.refresh(movie)
        return MovieRead.from_orm(movie)

    async def get_all(self) -> List[Optional[MovieRead]]:
        result = await self.session.execute(select(Movie).order_by(Movie.rating.desc()))
        movies = result.scalars().all()
        return [MovieRead.from_orm(movie) for movie in movies]

    async def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return await self.session.get(Movie, movie_id)

    async def movie_exists_by_id(self, movie_id: int) -> bool:
        movie = await self.get_by_id(movie_id)
        return movie is not None

    async def update(self, movie: Movie, data: MovieCreate) -> Movie:
        for key, value in data.dict().items():
            setattr(movie, key, value)
        await self.session.commit()
        await self.session.refresh(movie)
        return movie

    async def delete(self, movie: Movie) -> bool:
        await self.session.delete(movie)
        await self.session.commit()
        return True
