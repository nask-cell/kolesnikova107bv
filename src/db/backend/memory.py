_tables = {}
_next_ids = {}


def create_record(table_name: str, *values) -> tuple:
    if table_name not in _tables:
        _tables[table_name] = []
        _next_ids[table_name] = 1
    record_id = _next_ids[table_name]
    record = (record_id,) + tuple(values)
    _tables[table_name].append(record)
    _next_ids[table_name] += 1
    return record


def select_record(table_name: str, **filters) -> list:
    if table_name not in _tables:
        return []
    records = _tables[table_name]
    if not filters:
        return records.copy()
    result = []
    for rec in records:
        ok = True
        for key, val in filters.items():
            if key == "id":
                if rec[0] != val:
                    ok = False
                    break
            else:
                pass
        if ok:
            result.append(rec)
    return result
