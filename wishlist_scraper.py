from WantToSee import WantToSee


def main():
    try:
        with open("wishlist.txt", encoding='utf-8') as file:
            text = file.read()
            matches = WantToSee.regex.finditer(text)

            with open("wishlistout.txt", 'w+', encoding='utf-8') as out:
                for match in matches:
                    wish = WantToSee.create_from_match(match)
                    out.write(str(wish) + "\n")

    except FileNotFoundError:
        print("File \"wishlist.txt\" was not found")


if __name__ == '__main__':
    main()
