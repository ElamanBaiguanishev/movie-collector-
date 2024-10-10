from pydantic import BaseModel
from pydantic import ConfigDict


# Базовая схема для фильмов
class MovieBase(BaseModel):
    title: str
    director: str
    year: int
    genre: str
    rating: float
    image_id: str


# Схема для создания фильма
class MovieCreate(MovieBase):
    pass


# Схема для чтения данных о фильме
class MovieRead(MovieBase):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: int
