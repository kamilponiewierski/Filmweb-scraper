import datetime
import html
import re
import typing


class Movie:
    def __init__(self, title: str, release_year: str):
        self.title = title
        self.release_year = release_year

    def __str__(self):
        return self.title + ", " + self.release_year

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.release_year == self.release_year and other.title == self.title
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.release_year))

    def to_csv(self):
        # quoted in case of commas in the title
        return "\"" + self.title + "\", " + self.release_year

    @staticmethod
    def intersection(list_1: list, list_2: list):
        return set(list_1).intersection(list_2)

    @staticmethod
    def intersection_of_many(list_of_lists: list):
        if len(list_of_lists) == 0:
            return set()
        else:
            acc = set(list_of_lists[0])
            list_of_lists.pop(0)
            while len(list_of_lists) != 0:
                acc = acc.intersection(list_of_lists[0])
                list_of_lists.pop(0)

            return acc


class WantToSee(object):
    regex = re.compile(r'(.*)(.* \d{4})\s'  # tytuł i rok
                       r'(?:.*\s)?'  # tytuł oryginalny
                       r'((\d{1,2} godz.)* ?(\d{1,2} min.)*)\s'  # czas trwania
                       r'(?:Oglądaj.*\s)?'  # reklama
                       r'(\d,\d) ([\d ]*)oceny?')  # średnia, liczba ocen

    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return str(self.title) + ' ' + str(self.year)

    @staticmethod
    def create_from_match(match):
        return WantToSee(match.group(1), match.group(2))


class Rating:
    """Class used for storing information about filmweb.pl rating"""

    regex = re.compile(r'(.*) (\d{4}).*\s'  # tytuł i rok produkcji
                       r'(?:Oglądaj .*\s)?'  # opcjonalna reklama Filmwebu
                       r'(\d,\d) '  # średnia
                       r'(.*) oceny? społeczności\s'  # liczba ocen
                       r'(dzisiaj|wczoraj|\d{1,2} \w*(?: \d{4})?)\s'  # dzień i miesiąc oceny
                       r'(\d{1,2})', flags=re.U)  # ocena
    """Pattern object, used for finding the movies"""

    def __init__(self, movie: Movie, ratings_average, ratings_count: str, date_rated: str, rating: int):
        self.movie = movie
        self.ratings_average = ratings_average
        self.ratings_count = ratings_count

        if date_rated == "dzisiaj":
            today = datetime.datetime.now()
            self.date_rated = Rating.datetime_into_date(today)
        else:
            if date_rated == "wczoraj":
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                self.date_rated = Rating.datetime_into_date(yesterday)
            else:
                self.date_rated = date_rated
                if re.search(r'\d{4}', self.date_rated) is None:
                    self.date_rated += ' ' + str(datetime.datetime.now().year)

        self.personal_rating = rating

    def __str__(self):
        line_1 = ' '.join((str(self.movie)))
        line_2 = ' '.join(("oceniono", self.ratings_count, "razy,", "średnia", self.ratings_average))
        line_3 = ' '.join(("ocena:", self.personal_rating))
        line_4 = ' '.join(("data oceny:", self.date_rated))

        return '\n'.join((line_1, line_2, line_3, line_4, ''))

    def to_csv(self):
        return ', '.join((self.movie.to_csv(),
                          self.ratings_average.replace(',', '.'),
                          self.ratings_count,
                          self.date_rated,
                          str(self.personal_rating)))

    @staticmethod
    def datetime_into_date(date: datetime.datetime):
        return str(date.day) + ' ' + int_into_polish_month(date.month) + ' ' + str(date.year)

    @staticmethod
    def create_rating_from_match(match: typing.Match):
        title = html.unescape(match.group(1))
        release_year = match.group(2)
        movie = Movie(title, release_year)

        ratings_average = match.group(3)
        ratings_count = match.group(4)
        date_rated = match.group(5)
        personal_rating = int(match.group(6))

        return Rating(movie, ratings_average, ratings_count, date_rated, personal_rating)


def int_into_polish_month(month: int):
    months = {
        1: "stycznia",
        2: "lutego",
        3: "marca",
        4: "kwietnia",
        5: "maja",
        6: "czerwca",
        7: "lipca",
        8: "sierpnia",
        9: "września",
        10: "października",
        11: "listopada",
        12: "grudnia"
    }
    return months[month]
