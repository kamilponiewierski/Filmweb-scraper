from unittest import TestCase
import Rating
from Movie import Movie


class TestRating(TestCase):
    def test_create_rating_from_match(self):
        with open("sample_page", encoding='utf-8') as test_page:
            text = test_page.read()
            matches = Rating.Rating.regex.finditer(text)
            for match in matches:
                movie = Rating.Rating.create_rating_from_match(match)
                if movie.movie.title == "Han Solo: Gwiezdne wojny - historie":
                    self.assertEqual(movie.personal_rating, 7, "Rating is int")
                    self.assertEqual(movie.date_rated, "22 września 2018")
                    self.assertEqual(movie.ratings_average, "6,8", "Average is str")

    def test_to_csv(self):
        test = Rating.Rating(Movie("Niebo i piekło", "1963"), "8,0", "2 241", "17 września 2018", 9)
        self.assertEqual(test.to_csv(), "\"Niebo i piekło\", 1963, 8.0, 2 241, 17 września 2018, 9")
