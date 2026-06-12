from src.db.backend.memory import MemoryDatabase
from src.db.backend.file import FileDatabase


class TUI:
    def __init__(self) -> None:
        print("\n=== Выбор типа базы данных ===")
        print("1. In-memory (данные не сохраняются)")
        print("2. File database (данные сохраняются в папку data/)")
        choice = input("Ваш выбор: ").strip()
        if choice == "2":
            self.db = FileDatabase()
            print("Используется файловая БД")
        else:
            self.db = MemoryDatabase()
            print("Используется in-memory БД")
        self.current_table = None

    def _print_menu(self) -> None:
        print("\n=== Универсальная база данных ===")
        print("1. Создать таблицу")
        print("2. Выбрать таблицу")
        print("3. Добавить запись")
        print("4. Показать все записи")
        print("5. Поиск")
        print("0. Выход")

    def _create_table(self) -> None:
        name = input("Имя таблицы: ").strip()
        cols = input("Колонки через запятую: ").strip()
        columns = tuple(c.strip() for c in cols.split(","))
        try:
            self.db.create_table(name, columns)
            self.current_table = name
            print(f"Таблица '{name}' создана")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _select_table(self) -> None:
        name = input("Имя таблицы: ").strip()
        try:
            self.db._load_table(name)
            self.current_table = name
            print(f"Текущая таблица: {name}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _add_record(self) -> None:
        if not self.current_table:
            print("Сначала создайте или выберите таблицу")
            return
        try:
            table = self.db._load_table(self.current_table)
            print("Введите значения:")
            record = {}
            for col in table.columns:
                val = input(f"{col}: ").strip()
                record[col] = val
            self.db.insert_record(self.current_table, record)
            print("Запись добавлена")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _show_all(self) -> None:
        if not self.current_table:
            print("Сначала создайте или выберите таблицу")
            return
        try:
            records = self.db.select_records(self.current_table)
            if not records:
                print("Нет записей")
            else:
                for r in records:
                    print(r)
        except Exception as e:
            print(f"Ошибка: {e}")

    def _find_records(self) -> None:
        if not self.current_table:
            print("Сначала создайте или выберите таблицу")
            return
        print("Поиск (Enter - пропустить поле)")
        filters = {}
        try:
            table = self.db._load_table(self.current_table)
            for col in table.columns:
                val = input(f"{col}: ").strip()
                if val:
                    filters[col] = val
            if self.current_table == "movies" and "rating" in [
                col.lower() for col in table.columns
            ]:
                rating_min = input("rating_min (минимальный рейтинг): ").strip()
                if rating_min:
                    try:
                        filters["rating_min"] = float(rating_min)
                    except ValueError:
                        print("Ошибка: рейтинг должен быть числом")
                        return

            records = self.db.select_records(self.current_table, **filters)
            if not records:
                print("Ничего не найдено")
            else:
                for r in records:
                    print(r)
        except Exception as e:
            print(f"Ошибка: {e}")

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self._create_table()
            elif choice == "2":
                self._select_table()
            elif choice == "3":
                self._add_record()
            elif choice == "4":
                self._show_all()
            elif choice == "5":
                self._find_records()
            elif choice == "0":
                print("Выход.")
                break
            else:
                print("Неизвестная команда")


def main():
    app = TUI()
    app.run()


if __name__ == "__main__":
    main()
