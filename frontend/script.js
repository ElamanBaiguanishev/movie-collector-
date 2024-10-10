$(document).ready(function() {
    // Функция для загрузки данных фильмов с сервера
    function loadMovies() {
        $.ajax({
            url: 'http://localhost:8000/api/movies',
            method: 'GET',
            success: function(data) {
                $('#movie-table-body').empty();
                data.forEach(function(movie) {
                    $('#movie-table-body').append(
                        `<tr>
                            <td>${movie.title}</td>
                            <td>${movie.director}</td>
                            <td>${movie.year}</td>
                            <td>${movie.genre}</td>
                            <td>${movie.rating}</td>
                        </tr>`
                    );
                });
            },
            error: function(error) {
                console.error("Ошибка при загрузке данных:", error);
            }
        });
    }

    // Обработчик нажатия на кнопку "Загрузить фильмы"
    $('#load-movies').click(function() {
        $.ajax({
            url: 'http://localhost:8000/api/movies/parse',
            method: 'POST',
            success: function(data) {
                loadMovies();  // Загружаем обновленные данные
            },
            error: function(error) {
                console.error("Ошибка при загрузке фильмов:", error);
            }
        });
    });

    // Загружаем данные фильмов при загрузке страницы
    loadMovies();
});
