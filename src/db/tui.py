from .backend.memory import create_record, select_record


def _print_menu() -> None:
    print("\n=== Фильмы ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("0. Выход")


def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")


def _add_film() -> None:
    print("\nДобавление записи")

    film_id = _read_int("id: ")
    title = input("title: ").strip()
    year = _read_int("year: ")
    genre = input("genre: ").strip()
    rating = float(input("rating: "))

    try:
        record = create_record(film_id, title, year, genre, rating)
        print(f"Запись добавлена: {record}")
    except ValueError as exc:
        print(f"Ошибка: {exc}")


def _print_records(records: list[tuple[int, str, int, str, float]]) -> None:
    if not records:
        print("Записи не найдены.")
        return
    for record in records:
        print(record)


def _show_all_films() -> None:
    print("\nСписок записей")
    _print_records(select_record())


def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число или оставьте поле пустым.")


def _find_films_by_filter() -> None:
    print("\nПоиск по фильтру (Enter = пропустить поле)")

    film_id = _read_optional_int("id: ")
    title = input("title: ").strip() or None
    genre = input("genre: ").strip() or None
    year = _read_optional_int("year: ")

    try:
        rating = input("Rating from (0-10): ").strip()
        rating = float(rating) if rating else None
    except ValueError:
        print("The rating should be a number.")
        rating = None

    records = select_record(
        id=film_id,
        title=title,
        year=year,
        genre=genre,
        rating=rating,
    )
    _print_records(records)


def run():
    while True:
        _print_menu()
        action = input("Выберите действие: ").strip()

        if action == "1":
            _add_film()
        elif action == "2":
            _show_all_films()
        elif action == "3":
            _find_films_by_filter()
        elif action == "0":
            print("Выход из программы.")
            break
        else:
            print("Неизвестная команда.")
