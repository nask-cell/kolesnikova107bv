import unittest
from src.db.backend.memory import MovieTable
from src.db.backend.errors import (
    InvalidYearError,
    InvalidRatingError,
    DuplicateIDError,
    EmptyFieldError,
)


class TestMemory(unittest.TestCase):
    def setUp(self):
        self.movie_table = MovieTable()
        self.assertIsInstance(self.movie_table, MovieTable)

    def test_create_record(self):
        cases = [
            (1, "Avatar", 2009, "Sci-Fi", 7.9),
            (2, "Interstellar", 2014, "Sci-Fi", 8.6),
            (3, "Star Wars", 1977, "Sci-Fi", 8.6),
            (4, "Titanic", 1997, "Romance", 7.9),
            (5, "The Matrix", 1999, "Sci-Fi", 8.7),
            (6, "The Wolf of Wall Street", 2013, "Drama", 8.2),
            (7, "Terminator", 1984, "Sci-Fi", 8.1),
            (8, "The Walking Dead", 2010, "Horror", 8.1),
            (9, "2012", 2009, "Disaster", 5.8),
            (10, "Spider-Man", 2002, "Sci-Fi", 7.4),
            (11, "The Avengers", 2012, "Sci-Fi", 8.0),
            (12, "Ice", 2018, "Drama", 6.5),
        ]
        for test_data in cases:
            with self.subTest(test_data=test_data):
                record = self.movie_table.create_record(*test_data)
                self.assertEqual(record, test_data)

    def test_create_record_invalid_year(self):
        cases = [
            (1, "Old Movie", 1899, "Drama", 5.0),
            (2, "Future Movie", 2027, "Sci-Fi", 5.0),
        ]
        error_message = "Год должен быть от 1900 до 2026."
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidYearError) as context:
                    self.movie_table.create_record(*test_data)
                self.assertEqual(str(context.exception), error_message)

    def test_create_record_invalid_rating(self):
        cases = [
            (1, "High Rating", 2000, "Drama", 11),
            (2, "Negative Rating", 2000, "Drama", -1),
        ]
        error_message = "Рейтинг должен быть от 0 до 10."
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(InvalidRatingError) as context:
                    self.movie_table.create_record(*test_data)
                self.assertEqual(str(context.exception), error_message)

    def test_create_record_empty_fields(self):
        cases = [
            (1, "", 2000, "Drama", 5.0),
            (2, "Title", 2000, "", 5.0),
        ]
        expected_messages = {
            1: "Название не может быть пустым.",
            2: "Жанр не может быть пустым.",
        }
        for test_data in cases:
            with self.subTest(test_data=test_data):
                with self.assertRaises(EmptyFieldError) as context:
                    self.movie_table.create_record(*test_data)
                self.assertEqual(
                    str(context.exception), expected_messages[test_data[0]]
                )

    def test_create_record_duplicate_id(self):
        test_data_1 = (1, "Avatar", 2009, "Sci-Fi", 7.9)
        test_data_2 = (1, "Interstellar", 2014, "Sci-Fi", 8.6)
        error_message = "Запись с id=1 уже существует."
        self.movie_table.create_record(*test_data_1)
        with self.assertRaises(DuplicateIDError) as context:
            self.movie_table.create_record(*test_data_2)
        self.assertEqual(str(context.exception), error_message)

    def test_select_record(self):
        test_datas = [
            (1, "Avatar", 2009, "Sci-Fi", 7.9),
            (2, "Interstellar", 2014, "Sci-Fi", 8.6),
            (3, "Star Wars", 1977, "Sci-Fi", 8.6),
            (4, "Titanic", 1997, "Romance", 7.9),
            (5, "The Matrix", 1999, "Sci-Fi", 8.7),
            (6, "The Wolf of Wall Street", 2013, "Drama", 8.2),
            (7, "Terminator", 1984, "Sci-Fi", 8.1),
            (8, "The Walking Dead", 2010, "Horror", 8.1),
            (9, "2012", 2009, "Disaster", 5.8),
            (10, "Spider-Man", 2002, "Sci-Fi", 7.4),
        ]
        for test_data in test_datas:
            self.movie_table.create_record(*test_data)

        cases = [
            {
                "name": "Select without filters",
                "filters": {},
                "expected": test_datas,
            },
            {
                "name": "Filter by ID",
                "filters": {"movie_id": 1},
                "expected": [test_datas[0]],
            },
            {
                "name": "Filter by title",
                "filters": {"title": "Interstellar"},
                "expected": [test_datas[1]],
            },
            {
                "name": "Filter by year",
                "filters": {"year": 2009},
                "expected": [test_datas[0], test_datas[8]],
            },
            {
                "name": "Filter by genre",
                "filters": {"genre": "Sci-Fi"},
                "expected": [
                    test_datas[0],
                    test_datas[1],
                    test_datas[2],
                    test_datas[4],
                    test_datas[6],
                    test_datas[9],
                ],
            },
            {
                "name": "Filter by rating (minimum)",
                "filters": {"rating_min": 8.5},
                "expected": [test_datas[1], test_datas[2], test_datas[4]],
            },
        ]
        for case in cases:
            with self.subTest(
                case=case["name"], filters=case["filters"], expected=case["expected"]
            ):
                records = self.movie_table.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])
