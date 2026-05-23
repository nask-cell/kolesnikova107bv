import unittest
from src.db.backend.memory import MovieTable

class TestMemory(unittest.TestCase):
    def test_movie_table_allocation(self):
        movie_table = MovieTable()
        self.assertIsInstance(movie_table, MovieTable)

    def test_create_record(self):
        test_data = (1, "Inception", 2010, "Sci-Fi", 8.8)
        movie_table = MovieTable()
        record = movie_table.create_record(*test_data)
        self.assertEqual(record, test_data)
