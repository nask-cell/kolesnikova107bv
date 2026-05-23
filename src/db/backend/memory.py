type MovieRecord = tuple[int, str, int, str, float]

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
        new_record: MovieRecord = (
            movie_id,
            title.strip(),
            year,
            genre.strip(),
            rating,
        )
        self._movies.append(new_record)
        return new_record
