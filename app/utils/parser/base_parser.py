import requests
from abc import ABC, abstractmethod


class BaseParser(ABC):
    def __init__(self, url: str):
        self.url = url

    def fetch_html(self) -> str:
        """Метод для отправки запроса к сайту и получения HTML."""
        response = requests.get(self.url)
        response.raise_for_status()  # Проверка успешности запроса
        return response.text  # Возвращаем HTML как строку

    @abstractmethod
    async def parse_movies(self) -> list:
        """Абстрактный метод для разбора HTML и получения данных фильмов.
        Каждый парсер будет реализовывать этот метод по-своему.
        """
        pass
