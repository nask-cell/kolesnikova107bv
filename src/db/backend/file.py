import json
from pathlib import Path

from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table


class FileDatabase(Database):
    """База данных, которая хранит таблицы в JSON-файлах."""

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        table_path = self._get_table_path(table_name)
        if not table_path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")

        try:
            with table_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise InvalidStorageDataError(
                "Файл таблицы содержит некорректный JSON."
            ) from error
        except (OSError, IOError) as error:
            raise InvalidStorageDataError(
                f"Ошибка доступа к файлу таблицы '{table_name}': {error}"
            ) from error
        if not isinstance(data, dict):
            raise InvalidStorageDataError(
                f"Файл таблицы '{table_name}' должен содержать JSON-объект."
            )
        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError(
                f"Файл таблицы '{table_name}' имеет некорректную структуру: отсутствуют 'columns' или 'records'."
            )
        if not isinstance(data["columns"], list):
            raise InvalidStorageDataError(
                f"Поле 'columns' в таблице '{table_name}' должно быть списком."
            )
        if not isinstance(data["records"], list):
            raise InvalidStorageDataError(
                f"Поле 'records' в таблице '{table_name}' должно быть списком."
            )

        columns = tuple(data["columns"])
        records = data.get("records", [])
        return Table(columns, records)

    def _save_table(self, table_name: str, table: Table) -> None:
        table_path = self._get_table_path(table_name)

        with table_path.open("w", encoding="utf-8") as file:
            json.dump(
                self._serialize_table(table),
                file,
                ensure_ascii=False,
                indent=2,
            )

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _serialize_table(self, table: Table) -> dict:
        return {
            "columns": list(table.columns),
            "records": [record.copy() for record in table.records],
        }

    def _deserialize_table(self, data: dict) -> Table:
        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError("Файл таблицы имеет некорректную структуру.")

        columns = tuple(data["columns"])
        records = data.get("records", [])
        return Table(columns, records)
