import re


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
