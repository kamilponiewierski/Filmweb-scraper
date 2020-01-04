import re
import html
import datetime


def int_into_polish_month(month_int):
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
    return months[month_int]


class Rating:
    regex = re.compile(r'(.*) (\d{4}).*\s'                                                     # tytuł i rok produkcji
                       r'(?:Oglądaj .*\s)?'
                       r'(\d,\d) '                                                             # średnia
                       r'(.*) oceny?\b\s'                                                      # liczba ocen
                       r'(dzisiaj|wczoraj|\d{1,2} \w*(?: \d{4})?)\s'                           # dzień i miesiąc oceny
                       r'(\d{1,2})', flags=re.U)                                               # ocena

    @staticmethod
    def datetime_into_date(date):
        return str(date.day) + ' ' + int_into_polish_month(date.month) + ' ' + str(date.year)

    def __init__(self, title, release_year, ratings_average, ratings_count, date_rated, rating):
        self.title = title
        self.release_year = release_year
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
        line_1 = ' '.join((self.title, self.release_year))
        line_2 = ' '.join(("oceniono", self.ratings_count, "razy,", "średnia", self.ratings_average))
        line_3 = ' '.join(("ocena:", self.personal_rating))
        line_4 = ' '.join(("data oceny:", self.date_rated))

        return '\n'.join((line_1, line_2, line_3, line_4, ''))

    def to_csv(self):
        return ', '.join(('\"' + self.title + '\"',
                          self.release_year,
                          self.ratings_average.replace(',', '.'), self.ratings_count,
                          self.date_rated, self.personal_rating))

    @staticmethod
    def create_rating_from_match(match):
        title = html.unescape(match.group(1))
        release_year = match.group(2)
        ratings_average = match.group(3)
        ratings_count = match.group(4)
        date_rated = match.group(5)
        personal_rating = match.group(6)

        return Rating(title, release_year, ratings_average, ratings_count, date_rated, personal_rating)


class WantToSee:
    regex = re.compile(r'(?:.*\n)(.* \d{4})\s')

    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return str(self.title) + ' ' + str(self.year)

    @staticmethod
    def create_from_match(match):
        return WantToSee(match.group(1), match.group(2))


def main():
    count_pages = re.compile("filmweb.pl")

    try:
        with open("in.txt", 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print("Plik \"in.txt\" nie został znaleziony")
        exit(1)

    matches = Rating.regex.finditer(text)
    page_count = len(count_pages.findall(text))

    counter = 0

    with open("out.txt", 'w+', encoding='utf-8') as out:
        for match in matches:
            counter += 1
            r = Rating.create_rating_from_match(match)
            out.write(r.to_csv() + '\n')

    print("Znaleziono " + str(counter) + " filmów na " + str(page_count) + " stronach")
    wait = input("Wciśnij ENTER aby zakończyć")


if __name__ == "__main__":
    main()
