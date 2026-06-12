from abc import ABC, abstractmethod
from typing import Any

from .errors import (
    TableAlreadyExistsError,
    InvalidYearError,
    InvalidRatingError,
    EmptyFieldError,
    DuplicateIDError,
)
from .table import Table


class Database(ABC):
    """Общий интерфейс базы данных."""

    def create_table(self, table_name: str, columns: tuple[str, ...]) -> None:
        if self._table_exists(table_name):
            raise TableAlreadyExistsError(f"Таблица '{table_name}' уже существует.")

        self._save_table(table_name, Table(columns))

    def insert_record(self, table_name: str, record: dict[str, Any]) -> None:
        if table_name == "movies":
            if "year" in record:
                try:
                    year = int(record["year"])
                    if year < 1900 or year > 2026:
                        raise InvalidYearError("Год должен быть от 1900 до 2026.")
                    record["year"] = year
                except (ValueError, TypeError):
                    raise InvalidYearError("Год должен быть целым числом")
            if "rating" in record:
                try:
                    rating = float(record["rating"])
                    if rating < 0 or rating > 10:
                        raise InvalidRatingError("Рейтинг должен быть от 0 до 10.")
                    record["rating"] = rating
                except (ValueError, TypeError):
                    raise InvalidRatingError("Рейтинг должен быть числом")
            if "title" in record and not str(record["title"]).strip():
                raise EmptyFieldError("Название не может быть пустым")
            if "genre" in record and not str(record["genre"]).strip():
                raise EmptyFieldError("Жанр не может быть пустым")
            if "movie_id" in record:
                existing = self.select_records(table_name, movie_id=record["movie_id"])
                if existing:
                    raise DuplicateIDError(
                        f"Запись с id={record['movie_id']} уже существует"
                    )

        table = self._load_table(table_name)
        table.insert_record(record)
        self._save_table(table_name, table)

    def select_records(self, table_name: str, **filters: Any) -> list[dict[str, Any]]:
        table = self._load_table(table_name)
        return table.select_records(**filters)

    @abstractmethod
    def _table_exists(self, table_name: str) -> bool:
        """Проверяет наличие таблицы."""

    @abstractmethod
    def _load_table(self, table_name: str) -> Table:
        """Загружает таблицу."""

    @abstractmethod
    def _save_table(self, table_name: str, table: Table) -> None:
        """Сохраняет таблицу."""
