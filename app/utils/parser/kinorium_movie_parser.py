from bs4 import BeautifulSoup
from schemas.movie import MovieCreate
from utils.parser.base_parser import BaseParser


class KinoriumMovieParser(BaseParser):
    async def parse_movies(self) -> list[MovieCreate]:
        """Метод для парсинга HTML и получения списка фильмов."""
        html = self.fetch_html()
        soup = BeautifulSoup(html, "html.parser")

        film_list_div = soup.find("div", class_="filmList filmList_with-menu-filter")

        if film_list_div:
            movie_elements = film_list_div.find_all("div", recursive=False)

            movies = []

            for movie_element in movie_elements:
                # Название
                title_span = movie_element.find("span", class_="title")
                title = title_span.text.strip() if title_span else "Unknown"

                # Год
                small_text_span = movie_element.find(
                    "span", class_="filmList__small-text"
                )
                if small_text_span:
                    small_text = small_text_span.text.strip()
                    if "," in small_text:
                        _, year_str = small_text.rsplit(
                            ",", 1
                        )  # Берем только год после запятой
                        year = year_str.strip()
                    else:
                        year = small_text.strip()
                else:
                    year = "Unknown"

                # Жанр
                extra_info_p = movie_element.find("p", class_="filmList__extra-info")
                if extra_info_p:
                    genre_text = extra_info_p.text.split(",")[
                        0
                    ].strip()  # Берем жанры до первого разделителя (запятая)
                else:
                    genre_text = "Unknown"

                # Режиссер
                director_a = movie_element.find(
                    "a",
                    class_="filmList__extra-info-link link-info-persona-type-persona",
                )
                director = director_a.text.strip() if director_a else "Unknown"

                # imdb рейтинг
                imdb_rating_li = movie_element.find("li", class_="rating_imdb")
                imdb_rating_span = (
                    imdb_rating_li.find("span", class_="value green")
                    if imdb_rating_li
                    else None
                )
                imdb_rating = (
                    imdb_rating_span.text.strip() if imdb_rating_span else "Unknown"
                )

                image_url = movie_element.find("img", class_="movie-list-poster")["src"]

                movies.append(
                    MovieCreate(
                        title=title,
                        director=director,
                        year=int(year),
                        genre=genre_text,
                        rating=float(imdb_rating),
                        image_id=str(image_url),
                    )
                )

            return movies
        else:
            return []
