import re
import html


class Rating:
    regex = re.compile(r'(.*) (\d{4}).*\s'                                                     # tytuł i rok produkcji
                       r'(?:Oglądaj .*\s)?'
                       r'(\d,\d) '                                                             # średnia
                       r'(.*) oceny?\b\s'                                                      # liczba ocen
                       r'(dzisiaj|wczoraj|\d{1,2} \w*(?: \d{4})?)\s'                           # dzień i miesiąc oceny
                       r'(\d{1,2})', flags=re.U)                                               # ocena

    def __init__(self, title, release_year, ratings_average, ratings_count, date_rated, rating):
        self.title = title
        self.release_year = release_year
        self.ratings_average = ratings_average
        self.ratings_count = ratings_count
        self.date_rated = date_rated
        self.personal_rating = rating

    def __str__(self):
        line_1 = " ".join((self.title, self.release_year))
        line_2 = " ".join(("oceniono", self.ratings_count, "razy,", "średnia", self.ratings_average))
        line_3 = " ".join(("ocena:", self.personal_rating))
        line_4 = " ".join(("data oceny:", self.date_rated))

        return "\n".join((line_1, line_2, line_3, line_4, ""))

    @staticmethod
    def create_rating_from_match(match):
        title = html.unescape(match.group(1))
        release_year = match.group(2)
        ratings_average = match.group(3)
        ratings_count = match.group(4)
        date_rated = match.group(5)
        personal_rating = match.group(6)

        r = Rating(title, release_year, ratings_average, ratings_count, date_rated, personal_rating)
        return r


class WantToSee:
    regex = re.compile(r'(?:.*\n)(.* \d{4})\s')

    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return str(self.title) + " " + str(self.year)

    @staticmethod
    def create_from_match(match):
        r = WantToSee(match.group(1), match(2))
        return r




def main():
    count_pages = re.compile("filmweb.pl")

    file = open("in", 'r', encoding='utf-8')
    text = file.read()
    file.close()

    matches = Rating.regex.finditer(text)
    page_count = len(count_pages.findall(text))

    counter = 0

    for match in matches:
        counter += 1
        r = Rating.create_rating_from_match(match)
        print(str(r))

    print("Znaleziono " + str(counter) + " filmów na " + str(page_count) + " stronach")


if __name__ == '__main__':
    main()
