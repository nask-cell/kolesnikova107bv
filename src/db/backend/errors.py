class MovieTableError(Exception):
    """Базовый класс для ошибок, связанных с таблицей Movie."""
    pass


class InvalidYearError(MovieTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным годом."""
    pass


class InvalidRatingError(MovieTableError):
    """Ошибка, возникающая при попытке создать запись с некорректным рейтингом."""
    pass


class DuplicateIDError(MovieTableError):
    """Ошибка, возникающая при попытке создать запись с уже существующим идентификатором."""
    pass


class EmptyFieldError(MovieTableError):
    """Ошибка, возникающая при попытке создать запись с пустым названием или жанром."""
    pass
