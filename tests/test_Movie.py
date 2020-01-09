from unittest import TestCase
from Movie import Movie


class TestMovie(TestCase):
    def test_Movie_eq(self):
        movie_1 = Movie("Rudobrody", "1965")
        movie_2 = Movie("Rudobrody", "1965")
        self.assertEqual(movie_1, movie_2)

    def test_Movie_same_title_different_year_not_eq(self):
        movie_1 = Movie("Westworld", "1973")
        movie_2 = Movie("Westworld", "2016")
        self.assertNotEqual(movie_1, movie_2)
