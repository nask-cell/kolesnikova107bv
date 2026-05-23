import unittest
from src.db.backend.memory import MovieTable
from src.db.backend.errors import (
    InvalidYearError,
    InvalidRatingError,
    DuplicateIDError,
    EmptyFieldError,
)


class TestMemory(unittest.TestCase):
    def test_movie_table_allocation(self):
        movie_table = MovieTable()
        self.assertIsInstance(movie_table, MovieTable)

    def test_create_record(self):
        test_data = (1, "Inception", 2010, "Sci-Fi", 8.8)
        movie_table = MovieTable()
        record = movie_table.create_record(*test_data)
        self.assertEqual(record, test_data)

    def test_create_record_invalid_year(self):
        test_data = (1, "Inception", 1899, "Sci-Fi", 8.8)
        error_message = "Год должен быть от 1900 до 2026."
        movie_table = MovieTable()
        with self.assertRaises(InvalidYearError) as context:
            movie_table.create_record(*test_data)
        self.assertEqual(str(context.exception), error_message)

    def test_create_record_invalid_rating(self):
        test_data = (1, "Inception", 2010, "Sci-Fi", 11)
        error_message = "Рейтинг должен быть от 0 до 10."
        movie_table = MovieTable()
        with self.assertRaises(InvalidRatingError) as context:
            movie_table.create_record(*test_data)
        self.assertEqual(str(context.exception), error_message)

    def test_create_record_empty_title(self):
        test_data = (1, "", 2010, "Sci-Fi", 8.8)
        error_message = "Название не может быть пустым."
        movie_table = MovieTable()
        with self.assertRaises(EmptyFieldError) as context:
            movie_table.create_record(*test_data)
        self.assertEqual(str(context.exception), error_message)

    def test_create_record_duplicate_id(self):
        test_data_1 = (1, "Inception", 2010, "Sci-Fi", 8.8)
        test_data_2 = (1, "Interstellar", 2014, "Sci-Fi", 9.0)
        error_message = "Запись с id=1 уже существует."
        movie_table = MovieTable()
        movie_table.create_record(*test_data_1)
        with self.assertRaises(DuplicateIDError) as context:
            movie_table.create_record(*test_data_2)
        self.assertEqual(str(context.exception), error_message)
