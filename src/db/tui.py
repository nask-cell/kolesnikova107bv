from .backend.memory import create_record, select_record

current_table = None
current_columns = []


def _print_menu():
    print("\n=== Универсальная база данных ===")
    print("1. Создать таблицу")
    print("2. Выбрать таблицу")
    print("3. Добавить запись")
    print("4. Показать все записи")
    print("5. Поиск")
    print("0. Выход")


def _create_table():
    global current_table, current_columns
    name = input("Имя таблицы: ").strip()
    cols = input("Колонки через запятую: ").strip()
    current_columns = [c.strip() for c in cols.split(",")]
    current_table = name
    print(f"Таблица '{name}' создана")


def _select_table():
    global current_table, current_columns
    name = input("Имя таблицы: ").strip()
    current_table = name
    records = select_record(name)
    if records:
        first_record = records[0][1:]
        current_columns = [f"col{i}" for i in range(len(first_record))]
    print(f"Текущая таблица: {name}")


def _is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def _is_float(val):
    try:
        float(val)
        return True
    except ValueError:
        return False


def _add_record():
    if not current_table:
        print("Сначала создайте или выберите таблицу")
        return
    if not current_columns:
        print("Сначала создайте таблицу с колонками (пункт 1)")
        return

    print("\nВведите значения:")
    values = []
    ok = True
    for col in current_columns:
        val = input(f"{col}: ").strip()
        if col == "year":
            if not _is_int(val):
                print(
                    f"Ошибка: '{val}' не является годом (нужно целое число). Запись не добавлена."
                )
                ok = False
                break
        elif col == "rating":
            if not _is_float(val):
                print(
                    f"Ошибка: '{val}' не является рейтингом (нужно число). Запись не добавлена."
                )
                ok = False
                break
        values.append(val)

    if ok:
        record = create_record(current_table, *values)
        print("Запись добавлена:", record)
    else:
        print("Запись не добавлена из‑за ошибок ввода.")


def _show_all():
    if not current_table:
        print("Сначала создайте или выберите таблицу")
        return
    records = select_record(current_table)
    if not records:
        print("Нет записей")
    else:
        for r in records:
            print(r)


def _find_records():
    if not current_table:
        print("Сначала создайте или выберите таблицу")
        return
    print("Поиск (Enter - пропустить поле)")
    filters = {}
    for col in current_columns:
        val = input(f"{col}: ").strip()
        if val:
            filters[col] = val
    result = select_record(current_table, **filters)
    if not result:
        print("Ничего не найдено")
    else:
        for r in result:
            print(r)


def run():
    while True:
        _print_menu()
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            _create_table()
        elif choice == "2":
            _select_table()
        elif choice == "3":
            _add_record()
        elif choice == "4":
            _show_all()
        elif choice == "5":
            _find_records()
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неизвестная команда")
