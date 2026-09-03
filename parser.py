from library import Book

def load_books(filename):
    books = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            isbn, title, author = line.split(";")

            books.append(Book(isbn, title, author))

    return books