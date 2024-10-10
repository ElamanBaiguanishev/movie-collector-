from typing import Type
from utils.parser.kinorium_movie_parser import KinoriumMovieParser
from utils.parser.base_parser import BaseParser
from utils.parser.example_movie_parser import AnotherSiteMovieParser


def get_parser(parser_class_name: str, url: str) -> BaseParser:
    """Фабрика для создания объекта парсера на основе его имени."""
    parsers: dict[str, Type[BaseParser]] = {
        "KinoriumMovieParser": KinoriumMovieParser,
        "AnotherSiteMovieParser": AnotherSiteMovieParser,
    }
    parser_class = parsers.get(parser_class_name)

    if not parser_class:
        raise ValueError(f"Parser class '{parser_class_name}' not found")

    return parser_class(url)  # Возвращаем экземпляр класса
