import re

from Rating import Rating


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
    input("Wciśnij ENTER aby zakończyć")


if __name__ == "__main__":
    main()
