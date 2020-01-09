import unittest
from filmweb import Movie, Rating


class TestMovie(unittest.TestCase):
    def test_Movie_eq(self):
        movie_1 = Movie("Rudobrody", "1965")
        movie_2 = Movie("Rudobrody", "1965")
        self.assertEqual(movie_1, movie_2)

    def test_Movie_same_title_different_year_not_eq(self):
        movie_1 = Movie("Westworld", "1973")
        movie_2 = Movie("Westworld", "2016")
        self.assertNotEqual(movie_1, movie_2)

    def test_intersection(self):
        mv_1 = Movie("Rudobrody", "1965")
        mv_2 = Movie("Tenet", "2020")
        mv_3 = Movie("Parasite", "2019")
        mv_4 = Movie("Lighthouse", "2019")

        list_1 = [mv_1, mv_2, mv_3, mv_4]

        mv_5 = Movie("Irishman", "2019")
        mv_6 = Movie("Na noże", "2019")
        mv_7 = Movie("Parasite", "2019")
        mv_8 = Movie("Rudobrody", "1965")

        list_2 = [mv_5, mv_6, mv_7, mv_8]

        expected_list = [Movie("Parasite", "2019"), Movie("Rudobrody", "1965")]
        self.assertEqual(Movie.intersection(list_1, list_2), set(expected_list))

    def test_intersection_of_many(self):
        mv_1 = Movie("Rudobrody", "1965")
        mv_2 = Movie("Tenet", "2020")
        mv_3 = Movie("Parasite", "2019")
        mv_4 = Movie("Lighthouse", "2019")

        list_1 = [mv_1, mv_2, mv_3, mv_4]

        mv_5 = Movie("Irishman", "2019")
        mv_6 = Movie("Na noże", "2019")
        mv_7 = Movie("Parasite", "2019")
        mv_8 = Movie("Rudobrody", "1965")

        list_2 = [mv_5, mv_6, mv_7, mv_8]

        mv_9 = Movie("Parasite", "2019")
        mv_10 = Movie("Barbarzyńska nimfomanka w piekle dinozaurów", "1990")

        list_3 = [mv_9, mv_10]

        all_lists = [list_1, list_2, list_3]

        result = {Movie("Parasite", "2019")}

        self.assertEqual(Movie.intersection_of_many(all_lists), result)

    def test_intersection_of_many_with_empty_list(self):
        mv_1 = Movie("Rudobrody", "1965")
        mv_2 = Movie("Tenet", "2020")
        mv_3 = Movie("Parasite", "2019")
        mv_4 = Movie("Lighthouse", "2019")

        list_1 = [mv_1, mv_2, mv_3, mv_4]
        list_2 = []
        list_3 = [mv_3]

        ll = [list_1, list_2, list_3]

        self.assertEqual(Movie.intersection_of_many(ll), set())

    def test_intersection_of_many_empty(self):
        self.assertEqual(Movie.intersection_of_many([]), set())


class TestRating(unittest.TestCase):
    def test_create_rating_from_match(self):
        with open("sample_page", encoding='utf-8') as test_page:
            text = test_page.read()
            matches = Rating.regex.finditer(text)
            for match in matches:
                movie = Rating.create_rating_from_match(match)
                if movie.movie.title == "Han Solo: Gwiezdne wojny - historie":
                    self.assertEqual(movie.personal_rating, 7, "Rating is int")
                    self.assertEqual(movie.date_rated, "22 września 2018")
                    self.assertEqual(movie.ratings_average, "6,8", "Average is str")

    def test_to_csv(self):
        test = Rating(Movie("Niebo i piekło", "1963"), "8,0", "2 241", "17 września 2018", 9)
        self.assertEqual(test.to_csv(), "\"Niebo i piekło\", 1963, 8.0, 2 241, 17 września 2018, 9")


if __name__ == '__main__':
    unittest.main()
