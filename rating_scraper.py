import re
import os

from filmweb import Rating


def main():
    count_pages_regex = re.compile("filmweb.pl")
    path = "./"

    counter = 0
    page_count = 0

    for f in os.listdir(path):
        if re.match(r'in.*\.txt', f):
            with open(f, 'r', encoding='utf-8') as file:
                text = file.read()

            matches = Rating.regex.finditer(text)
            page_count += len(count_pages_regex.findall(text))

            with open("out" + f[2:], 'w+', encoding='utf-8') as out:
                for match in matches:
                    counter += 1
                    r = Rating.create_rating_from_match(match)
                    out.write(r.to_csv() + '\n')

    print("Znaleziono " + str(counter) + " filmów na " + str(page_count) + " stronach")
    input("Wciśnij ENTER aby zakończyć")


if __name__ == "__main__":
    main()
