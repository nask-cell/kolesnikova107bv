import unittest
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import (
    InvalidYearError,
    InvalidRatingError,
    EmptyFieldError,
    DuplicateIDError,
)


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDatabase()
        self.db.create_table("movies", ("movie_id", "title", "year", "genre", "rating"))

    def test_insert_record(self):
        cases = [
            {
                "movie_id": 1,
                "title": "Avatar",
                "year": 2009,
                "genre": "Sci-Fi",
                "rating": 7.9,
            },
            {
                "movie_id": 2,
                "title": "Interstellar",
                "year": 2014,
                "genre": "Sci-Fi",
                "rating": 8.6,
            },
            {
                "movie_id": 3,
                "title": "Star Wars",
                "year": 1977,
                "genre": "Sci-Fi",
                "rating": 8.6,
            },
            {
                "movie_id": 4,
                "title": "Titanic",
                "year": 1997,
                "genre": "Romance",
                "rating": 7.9,
            },
            {
                "movie_id": 5,
                "title": "The Matrix",
                "year": 1999,
                "genre": "Sci-Fi",
                "rating": 8.7,
            },
            {
                "movie_id": 6,
                "title": "The Wolf of Wall Street",
                "year": 2013,
                "genre": "Drama",
                "rating": 8.2,
            },
            {
                "movie_id": 7,
                "title": "Terminator",
                "year": 1984,
                "genre": "Sci-Fi",
                "rating": 8.1,
            },
            {
                "movie_id": 8,
                "title": "The Walking Dead",
                "year": 2010,
                "genre": "Horror",
                "rating": 8.1,
            },
            {
                "movie_id": 9,
                "title": "2012",
                "year": 2009,
                "genre": "Disaster",
                "rating": 5.8,
            },
            {
                "movie_id": 10,
                "title": "Spider-Man",
                "year": 2002,
                "genre": "Sci-Fi",
                "rating": 7.4,
            },
            {
                "movie_id": 11,
                "title": "The Avengers",
                "year": 2012,
                "genre": "Sci-Fi",
                "rating": 8.0,
            },
            {
                "movie_id": 12,
                "title": "Ice",
                "year": 2018,
                "genre": "Drama",
                "rating": 6.5,
            },
        ]
        for record in cases:
            with self.subTest(record=record):
                self.db.insert_record("movies", record)
                found = self.db.select_records("movies", movie_id=record["movie_id"])
                self.assertEqual(len(found), 1)
                self.assertEqual(found[0]["title"], record["title"])

    def test_insert_invalid_year(self):
        cases = [
            {
                "movie_id": 1,
                "title": "Old",
                "year": 1899,
                "genre": "Drama",
                "rating": 5.0,
            },
            {
                "movie_id": 2,
                "title": "Future",
                "year": 2027,
                "genre": "Sci-Fi",
                "rating": 5.0,
            },
        ]
        error_message = "Год должен быть от 1900 до 2026."
        for record in cases:
            with self.subTest(record=record):
                with self.assertRaises(InvalidYearError) as ctx:
                    self.db.insert_record("movies", record)
                self.assertEqual(str(ctx.exception), error_message)

    def test_insert_invalid_rating(self):
        cases = [
            {
                "movie_id": 1,
                "title": "High",
                "year": 2000,
                "genre": "Drama",
                "rating": 11,
            },
            {
                "movie_id": 2,
                "title": "Negative",
                "year": 2000,
                "genre": "Drama",
                "rating": -1,
            },
        ]
        error_message = "Рейтинг должен быть от 0 до 10."
        for record in cases:
            with self.subTest(record=record):
                with self.assertRaises(InvalidRatingError) as ctx:
                    self.db.insert_record("movies", record)
                self.assertEqual(str(ctx.exception), error_message)

    def test_insert_empty_fields(self):
        cases = [
            {"movie_id": 1, "title": "", "year": 2000, "genre": "Drama", "rating": 5.0},
            {"movie_id": 2, "title": "Title", "year": 2000, "genre": "", "rating": 5.0},
        ]
        expected_messages = {
            1: "Название не может быть пустым",
            2: "Жанр не может быть пустым",
        }
        for record in cases:
            with self.subTest(record=record):
                with self.assertRaises(EmptyFieldError) as ctx:
                    self.db.insert_record("movies", record)
                self.assertEqual(
                    str(ctx.exception), expected_messages[record["movie_id"]]
                )

    def test_insert_duplicate_id(self):
        record1 = {
            "movie_id": 1,
            "title": "Avatar",
            "year": 2009,
            "genre": "Sci-Fi",
            "rating": 7.9,
        }
        record2 = {
            "movie_id": 1,
            "title": "Interstellar",
            "year": 2014,
            "genre": "Sci-Fi",
            "rating": 8.6,
        }
        self.db.insert_record("movies", record1)
        with self.assertRaises(DuplicateIDError) as ctx:
            self.db.insert_record("movies", record2)
        self.assertEqual(str(ctx.exception), "Запись с id=1 уже существует")

    def test_select_records(self):
        test_data = [
            {
                "movie_id": 1,
                "title": "Avatar",
                "year": 2009,
                "genre": "Sci-Fi",
                "rating": 7.9,
            },
            {
                "movie_id": 2,
                "title": "Interstellar",
                "year": 2014,
                "genre": "Sci-Fi",
                "rating": 8.6,
            },
            {
                "movie_id": 3,
                "title": "Star Wars",
                "year": 1977,
                "genre": "Sci-Fi",
                "rating": 8.6,
            },
            {
                "movie_id": 4,
                "title": "Titanic",
                "year": 1997,
                "genre": "Romance",
                "rating": 7.9,
            },
            {
                "movie_id": 5,
                "title": "The Matrix",
                "year": 1999,
                "genre": "Sci-Fi",
                "rating": 8.7,
            },
            {
                "movie_id": 6,
                "title": "The Wolf of Wall Street",
                "year": 2013,
                "genre": "Drama",
                "rating": 8.2,
            },
            {
                "movie_id": 7,
                "title": "Terminator",
                "year": 1984,
                "genre": "Sci-Fi",
                "rating": 8.1,
            },
            {
                "movie_id": 8,
                "title": "The Walking Dead",
                "year": 2010,
                "genre": "Horror",
                "rating": 8.1,
            },
            {
                "movie_id": 9,
                "title": "2012",
                "year": 2009,
                "genre": "Disaster",
                "rating": 5.8,
            },
            {
                "movie_id": 10,
                "title": "Spider-Man",
                "year": 2002,
                "genre": "Sci-Fi",
                "rating": 7.4,
            },
        ]
        for record in test_data:
            self.db.insert_record("movies", record)

        cases = [
            {"filters": {}, "expected": test_data},
            {"filters": {"movie_id": 1}, "expected": [test_data[0]]},
            {"filters": {"title": "Interstellar"}, "expected": [test_data[1]]},
            {"filters": {"year": 2009}, "expected": [test_data[0], test_data[8]]},
            {
                "filters": {"genre": "Sci-Fi"},
                "expected": [
                    test_data[0],
                    test_data[1],
                    test_data[2],
                    test_data[4],
                    test_data[6],
                    test_data[9],
                ],
            },
            {
                "filters": {"rating_min": 8.5},
                "expected": [test_data[1], test_data[2], test_data[4]],
            },
        ]
        for case in cases:
            with self.subTest(filters=case["filters"]):
                result = self.db.select_records("movies", **case["filters"])
                self.assertEqual(result, case["expected"])


if __name__ == "__main__":
    unittest.main()
