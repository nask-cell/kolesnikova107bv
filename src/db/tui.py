from src.db.backend.file import FileDatabase
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import (
    TableNotFoundError,
    TableAlreadyExistsError,
    MissingColumnError,
    UnknownColumnError,
)


class TUI:
    def __init__(self) -> None:
        print("\n=== Выбор типа базы данных ===")
        print("1. In-memory (данные не сохраняются)")
        print("2. File database (данные сохраняются в файл)")

        choice = input("Введите номер: ").strip()
        if choice == "2":
            self.db = FileDatabase("data")
            print("Используется файловая БД (папка 'data/')")
        else:
            self.db = MemoryDatabase()
            print("Используется in-memory БД (данные не сохранятся)")

        self._init_movies_table()

    def _init_movies_table(self) -> None:
        """Создаёт таблицу movies, если её ещё нет."""
        try:
            self.db.create_table(
                "movies", ("movie_id", "title", "year", "genre", "rating")
            )
        except TableAlreadyExistsError:
            pass

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

    def _add_movie(self) -> None:
        print("\nДобавление фильма")
        movie_id = self._read_int("id: ")
        title = input("название: ").strip()
        year = self._read_int("год: ")
        genre = input("жанр: ").strip()
        rating = self._read_float("рейтинг: ")

        try:
            self.db.insert_record(
                "movies",
                {
                    "movie_id": movie_id,
                    "title": title,
                    "year": year,
                    "genre": genre,
                    "rating": rating,
                },
            )
            print("Фильм добавлен.")
        except (MissingColumnError, UnknownColumnError) as e:
            print(f"Ошибка структуры данных: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _show_all_movies(self) -> None:
        print("\nВсе фильмы:")
        try:
            records = self.db.select_records("movies")
            if not records:
                print("Фильмы не найдены.")
            else:
                for record in records:
                    print(
                        f"{record['movie_id']}: {record['title']} ({record['year']}) — {record['genre']}, ★ {record['rating']}"
                    )
        except TableNotFoundError:
            print("Таблица фильмов не найдена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _find_movies(self) -> None:
        print("\nПоиск по фильтру (Enter чтобы пропустить)")
        movie_id = self._read_int("id: ", allow_empty=True)
        title = input("название: ").strip() or None
        year = self._read_int("год: ", allow_empty=True)
        genre = input("жанр: ").strip() or None
        rating_min = self._read_float("минимальный рейтинг: ", allow_empty=True)

        filters = {}
        if movie_id is not None:
            filters["movie_id"] = movie_id
        if title is not None:
            filters["title"] = title
        if year is not None:
            filters["year"] = year
        if genre is not None:
            filters["genre"] = genre
        if rating_min is not None:
            filters["rating"] = rating_min

        try:
            records = self.db.select_records("movies", **filters)
            if not records:
                print("Фильмы не найдены.")
            else:
                for record in records:
                    print(
                        f"{record['movie_id']}: {record['title']} ({record['year']}) — {record['genre']}, ★ {record['rating']}"
                    )
        except TableNotFoundError:
            print("Таблица фильмов не найдена.")
        except Exception as e:
            print(f"Ошибка: {e}")

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._add_movie()
            elif choice == "2":
                self._show_all_movies()
            elif choice == "3":
                self._find_movies()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор, попробуйте снова.")


def main():
    app = TUI()
    app.run()


if __name__ == "__main__":
    main()
