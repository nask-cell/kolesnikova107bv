type FilmRecord = tuple[int, str, int, str, float]
Film: list[FilmRecord] = []
def create_record(
    id: int,
    title: str,
    year: int,
    genre: str,
    rating: float,
) -> FilmRecord:
    
    if year < 1900 or year > 2026:
        raise ValueError("Поле year должно быть от 1900 до 2026.")


    if rating < 0 or rating > 10:
        raise ValueError("Поле rating не может быть меньше 0 или больше 10.")


    if any(record[0] == id for record in Film):
        raise ValueError(f"Запись с id={id} уже существует.")
    
    new_record: FilmRecord = (
        id,
        title.strip(),
        year,
        genre.strip(),
        rating,
    )
    Film.append(new_record)
    return new_record

def select_record(
    id: int | None = None,
    title: str | None = None,
    year: int | None = None,
    genre: str | None = None,
    rating: float | None = None,
) -> list[FilmRecord]:

    if (
        id is None
        and title is None
        and year is None
        and genre is None
        and rating is None
    ):
        return Film.copy()

    result: list[FilmRecord] = []


    for record in Film:

        if id is not None and record[0] != id:
            continue

        if title is not None and record[1] != title:
            continue

        if year is not None and record[2] != year:
            continue

        if genre is not None and record[3] != genre:
            continue

        if rating is not None and record[4] != rating:
            continue

        result.append(record)


    return result

