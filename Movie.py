class Movie:
    def __init__(self, title: str, release_year: str):
        self.title = title
        self.release_year = release_year

    def __str__(self):
        return self.title + ", " + self.release_year

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.release_year == self.release_year and other.title == self.title

    def to_csv(self):
        # quoted in case of commas in the title
        return "\"" + self.title + "\", " + self.release_year
