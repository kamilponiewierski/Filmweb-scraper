import re
import html


class Rating:
    def __init__(self, title, release_year, avg_rating, cnt_rating, date_rated, rating):
        self.title = title
        self.release_year = release_year
        self.avg_rating = avg_rating
        self.cnt_rating = cnt_rating
        self.date_rated = date_rated
        self.rating = rating

    def __str__(self):
        line_1 = " ".join((self.title, self.release_year))
        line_2 = " ".join(("oceniono", self.cnt_rating, "razy,", "średnia", self.avg_rating))
        line_3 = " ".join(("ocena:", self.rating,))
        line_4 = " ".join(("data oceny:", self.date_rated))

        return "\n".join((line_1, line_2, line_3, line_4, ""))


# regex nie działa dla filmów bez plakatu
rating = re.compile(r'plakat filmu (.*)\s'                          # tytuł
                    r'.* (\d{4}).*\s'                               # rok produkcji
                    r'(?:Oglądaj .*\s)?'
                    r'(\d,\d) '                                     # średnia
                    r'(.*) oce(?:n|ny)\s'                           # liczba ocen
                    r'(\d{1,2} [A-Za-zzżźćńółęąśŻŹĆĄŚĘŁÓŃ]*)\s'     # dzień i miesiąc oceny
                    r'(\d{1,2})')                                   # ocena

count_pages = re.compile("filmweb.pl")

file = open("in", 'r', encoding='utf-8')
text = file.read()
file.close()

matches = rating.finditer(text)
page_count = len(count_pages.findall(text))

counter = 0

for match in matches:
    counter += 1

    title = html.unescape(match.group(1))
    release_year = match.group(2)
    avg_rating = match.group(3)
    cnt_rating = match.group(4)
    date_rated = match.group(5)
    rating = match.group(6)

    r = Rating(title, release_year, avg_rating, cnt_rating, date_rated, rating)
    print(str(r))

print("Znaleziono " + str(counter) + " filmów na " + str(page_count) + " stronach")
