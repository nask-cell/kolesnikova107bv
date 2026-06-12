from abc import ABC, abstractmethod
from typing import Any

from .errors import TableAlreadyExistsError
from .table import Table


class Database(ABC):
    """Общий интерфейс базы данных."""

    def create_table(self, table_name: str, columns: tuple[str, ...]) -> None:
        if self._table_exists(table_name):
            raise TableAlreadyExistsError(f"Таблица '{table_name}' уже существует.")

        self._save_table(table_name, Table(columns))

    def insert_record(self, table_name: str, record: dict[str, Any]) -> None:
        # Проверки бизнес-правил только для таблицы movies
        if table_name == "movies":
            # Год
            if "year" in record:
                try:
                    year = int(record["year"])
                    if year < 1900 or year > 2026:
                        raise ValueError("Год должен быть от 1900 до 2026")
                    record["year"] = year
                except (ValueError, TypeError):
                    raise ValueError("Год должен быть целым числом")

            # Рейтинг
            if "rating" in record:
                try:
                    rating = float(record["rating"])
                    if rating < 0 or rating > 10:
                        raise ValueError("Рейтинг должен быть от 0 до 10")
                    record["rating"] = rating
                except (ValueError, TypeError):
                    raise ValueError("Рейтинг должен быть числом")

            # Пустые поля
            if "title" in record and not str(record["title"]).strip():
                raise ValueError("Название не может быть пустым")
            if "genre" in record and not str(record["genre"]).strip():
                raise ValueError("Жанр не может быть пустым")

            # Дубликат movie_id
            if "movie_id" in record:
                existing = self.select_records(table_name, movie_id=record["movie_id"])
                if existing:
                    raise ValueError(f"Запись с id={record['movie_id']} уже существует")

        # Основная логика (без изменений)
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
