from .errors import DuplicateIDError, InvalidYearError, InvalidRatingError, EmptyFieldError

MovieRecord = tuple[int, str, int, str, float]

class MovieTable:
    def __init__(self) -> None:
        self._movies: list[MovieRecord] = []

    def create_record(
        self,
        movie_id: int,
        title: str,
        year: int,
        genre: str,
        rating: float,
    ) -> MovieRecord:
        if year < 1900 or year > 2026:
            raise InvalidYearError("Год должен быть от 1900 до 2026.")
        if rating < 0 or rating > 10:
            raise InvalidRatingError("Рейтинг должен быть от 0 до 10.")
        if not title or not title.strip():
            raise EmptyFieldError("Название не может быть пустым.")
        if not genre or not genre.strip():
            raise EmptyFieldError("Жанр не может быть пустым.")
        if any(record[0] == movie_id for record in self._movies):
            raise DuplicateIDError(f"Запись с id={movie_id} уже существует.")

        new_record = (movie_id, title.strip(), year, genre.strip(), rating)
        self._movies.append(new_record)
        return new_record

    def select_record(
        self,
        movie_id: int | None = None,
        title: str | None = None,
        year: int | None = None,
        genre: str | None = None,
        rating_min: float | None = None,
    ) -> list[MovieRecord]:
        if all(v is None for v in [movie_id, title, year, genre, rating_min]):
            return self._movies.copy()

        result: list[MovieRecord] = []
        for record in self._movies:
            if movie_id is not None and record[0] != movie_id:
                continue
            if title is not None and record[1] != title:
                continue
            if year is not None and record[2] != year:
                continue
            if genre is not None and record[3] != genre:
                continue
            if rating_min is not None and record[4] < rating_min:
                continue
            result.append(record)
        return result
