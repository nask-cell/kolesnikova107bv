from src.db.backend.memory import MovieTable
from src.db.backend.errors import (
    InvalidYearError,
    InvalidRatingError,
    DuplicateIDError,
    EmptyFieldError,
)


class TUI:
    def __init__(self) -> None:
        self.db = MovieTable()

    def _print_menu(self) -> None:
        print("\n=== База данных фильмов ===")
        print("1. Добавить фильм")
        print("2. Показать все фильмы")
        print("3. Найти фильмы по фильтру")
        print("0. Выход")

    def _read_int(self, prompt: str, allow_empty: bool = False) -> int | None:
        while True:
            try:
                raw = input(prompt).strip()
                if allow_empty and raw == "":
                    return None
                return int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")

    def _read_float(self, prompt: str, allow_empty: bool = False) -> float | None:
        while True:
            try:
                raw = input(prompt).strip()
                if allow_empty and raw == "":
                    return None
                return float(raw)
            except ValueError:
                print("Ошибка: введите число.")

    def _read_non_empty_str(self, prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Ошибка: поле не может быть пустым.")

    def _add_movie(self) -> None:
        print("\nДобавление фильма")
        movie_id = self._read_int("id: ")
        title = self._read_non_empty_str("название: ")
        year = self._read_int("год: ")
        genre = input("жанр: ").strip() or None
        rating = self._read_float("рейтинг: ")

        try:
            record = self.db.create_record(
                movie_id=movie_id,
                title=title,
                year=year,
                genre=genre,
                rating=rating,
            )
            print(f"Фильм добавлен: {record}")
        except (InvalidYearError, InvalidRatingError, DuplicateIDError, EmptyFieldError) as e:
            print(f"Ошибка: {e}")

    def _print_records(self, records: list) -> None:
        if not records:
            print("Фильмы не найдены.")
        else:
            for record in records:
                print(record)

    def _show_all_movies(self) -> None:
        print("\nВсе фильмы:")
        records = self.db.select_record()
        self._print_records(records)

    def _find_movies(self) -> None:
        print("\nПоиск по фильтру (Enter чтобы пропустить)")
        movie_id = self._read_int("id: ", allow_empty=True)
        title = input("название: ").strip() or None
        year = self._read_int("год: ", allow_empty=True)
        genre = input("жанр: ").strip() or None
        rating_min = self._read_float("минимальный рейтинг: ", allow_empty=True)

        records = self.db.select_record(
            movie_id=movie_id,
            title=title,
            year=year,
            genre=genre,
            rating_min=rating_min,
        )
        self._print_records(records)

    def run(self) -> None:
        actions = {
            "1": self._add_movie,
            "2": self._show_all_movies,
            "3": self._find_movies,
        }

        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()

            if choice == "0":
                print("До свидания!")
                break

            action = actions.get(choice)
            if action:
                action()
            else:
                print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    TUI().run()
    