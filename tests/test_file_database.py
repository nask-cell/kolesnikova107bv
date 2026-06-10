import tempfile
import unittest

from src.db.backend.errors import TableNotFoundError
from src.db.backend.file import FileDatabase


class TestFileDatabase(unittest.TestCase):
    def test_data_is_saved_between_instances(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)
            first_db.create_table(
                "movies", ("movie_id", "title", "year", "genre", "rating")
            )
            first_db.insert_record(
                "movies",
                {
                    "movie_id": 1,
                    "title": "Матрица",
                    "year": 1999,
                    "genre": "фантастика",
                    "rating": 9.5,
                },
            )

            second_db = FileDatabase(directory)
            records = second_db.select_records("movies")

            self.assertEqual(
                records,
                [
                    {
                        "movie_id": 1,
                        "title": "Матрица",
                        "year": 1999,
                        "genre": "фантастика",
                        "rating": 9.5,
                    }
                ],
            )

    def test_select_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("movies", ("movie_id", "title", "year", "genre", "rating"))
            db.insert_record(
                "movies",
                {
                    "movie_id": 1,
                    "title": "Матрица",
                    "year": 1999,
                    "genre": "фантастика",
                    "rating": 9.5,
                },
            )
            db.insert_record(
                "movies",
                {
                    "movie_id": 2,
                    "title": "Интерстеллар",
                    "year": 2014,
                    "genre": "фантастика",
                    "rating": 9.0,
                },
            )

            records = db.select_records("movies", title="Интерстеллар")

            self.assertEqual(
                records,
                [
                    {
                        "movie_id": 2,
                        "title": "Интерстеллар",
                        "year": 2014,
                        "genre": "фантастика",
                        "rating": 9.0,
                    }
                ],
            )

    def test_select_from_missing_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)

            with self.assertRaises(TableNotFoundError):
                db.select_records("movies")
