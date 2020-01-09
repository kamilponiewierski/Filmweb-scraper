import typing

import filmweb


def main():
    try:
        with open("wishlist1.txt", encoding='utf-8') as file:
            text = file.read()
            matches = filmweb.WantToSee.regex.finditer(text)

            with open("wishlistout.txt", 'w+', encoding='utf-8') as out:
                for match in matches:
                    movie = filmweb.Movie(match.group(1), match.group(2))
                    out.write(movie.to_csv() + "\n")

    except FileNotFoundError:
        print("File \"wishlist1.txt\" was not found")

    try:
        with open("wishlist1.txt", encoding='utf-8') as first:
            with open("wishlist2.txt", encoding='utf-8') as second:
                l1 = text_to_movie_list(first)
                l2 = text_to_movie_list(second)
                result = filmweb.Movie.intersection(l1, l2)
                for movie in result:
                    print(str(movie))

    except FileNotFoundError:
        print("Some file was not found")


def text_to_movie_list(file: typing.TextIO):
    movie_list = []
    first_text = file.read()
    first_iter = filmweb.WantToSee.regex.finditer(first_text)

    for match in first_iter:
        movie_list.append(filmweb.Movie(match.group(1), match.group(2)))

    return movie_list


if __name__ == '__main__':
    main()
