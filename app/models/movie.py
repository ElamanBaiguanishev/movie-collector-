from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Movie(IntIdPkMixin, Base):
    __tablename__ = "movies"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    director: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    image_id: Mapped[str] = mapped_column(String(255), nullable=False)
