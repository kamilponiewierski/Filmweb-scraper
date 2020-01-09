import re


class WantToSee(object):
    regex = re.compile(r'(?:.*)(.* \d{4})\s'  # tytuł i rok
                       r'(?:.*)?\s?'  # tytuł oryginalny
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
