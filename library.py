from datetime import datetime, timedelta


class Library:
    def __init__(self):
        self.__books = {}
        self.__users = {}
        self.__issue_history = []

    def add_book(self, book):
        self.__books[book.isbn] = book

    def delete_book(self, isbn):
        if isbn in self.__books:
            del self.__books[isbn]
            return True

        return False

    def get_book(self, isbn):
        return self.__books.get(isbn)

    def get_books(self):
        return self.__books.copy()

    def add_user(self, user):
        self.__users[user.id] = user

    def get_user(self, user_id):
        return self.__users.get(user_id)

    def get_users(self):
        return self.__users.copy()

    def issue_book(self, user, book):
        return_date = datetime.now() + user.issue_period
        book.issue(user, return_date)
        self.__issue_history.append({
            "book": book,
            "user": user,
            "issue_date": datetime.now(),
            "return_date": None
        })

    def return_book(self, book):
        book.return_book()
        for record in reversed(self.__issue_history):
            if record["book"] == book and record["return_date"] is None:
                record["return_date"] = datetime.now()
                break

    def get_issue_history(self):
        return self.__issue_history.copy()

    def find_by_title(self, title):
        return [
            book
            for book in self.__books.values()
            if title.lower() in book.title.lower()
        ]

    def find_by_author(self, author):
        return [
            book
            for book in self.__books.values()
            if author.lower() in book.author.lower()
        ]

    def find_by_isbn(self, isbn):
        return self.__books.get(isbn)

    def get_authors(self):
        return {
            book.author
            for book in self.__books.values()
        }

    def overdue_books(self):
        return [
            book
            for book in self.__books.values()
            if book.status == "Issued"
            and book.return_date < datetime.now()
        ]


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.__books = []

    def take_book(self, book, library):

        if book is None:
            print(f'{self.name} не может взять книгу: книга не найдена')
            return

        if len(self.__books) >= self.max_books:
            print(
                f'{self.name} не может взять больше '
                f'{self.max_books} книг'
            )
            return

        if book.status != "Available":
            print(
                f'{self.name} не может взять книгу, '
                f'так как она занята пользователем {book.user.name}'
            )
            return

        self.__books.append(book)

        library.issue_book(self, book)

        print(
            f'{self.name} взял книгу: '
            f'{book.title}'
        )
        return True

    def return_book(self, book, library):

        if book not in self.__books:
            print(
                f'{self.name} не брал книгу: '
                f'{book.title}'
            )
            return

        self.__books.remove(book)

        library.return_book(book)

        print(
            f'{self.name} вернул книгу: '
            f'{book.title}'
        )
        return True

    def get_books(self):
        return self.__books.copy()


class Student(User):
    max_books = 3
    issue_period = timedelta(days=14)


class Teacher(User):
    max_books = 10
    issue_period = timedelta(days=30)


class Guest(User):
    max_books = 1
    issue_period = timedelta(days=7)


class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author

        self.__status = "Available"
        self.__user = None
        self.__return_date = None

    @property
    def status(self):
        return self.__status

    @property
    def user(self):
        return self.__user

    @property
    def return_date(self):
        return self.__return_date

    def issue(self, user, return_date):
        self.__status = "Issued"
        self.__user = user
        self.__return_date = return_date

    def return_book(self):
        self.__status = "Available"
        self.__user = None
        self.__return_date = None

    def __str__(self):
        return (
            f"{self.title} — {self.author} "
            f"(ISBN: {self.isbn})"
        )
