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
