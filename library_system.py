import functools


class LendingError(Exception):
    pass


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("LOG: running", func.__name__)
        result = func(*args, **kwargs)
        print("LOG: finished", func.__name__)
        return result
    return wrapper


class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.__available = True

    def is_available(self):
        return self.__available

    def set_available(self, value):
        self.__available = value

    def display_details(self):
        if self.__available:
            status = "Available"
        else:
            status = "Borrowed"
        return self.title + " | " + self.author + " | " + self.isbn + " | " + status


class PrintedBook(Book):
    def __init__(self, title, author, isbn, pages):
        super().__init__(title, author, isbn)
        self.pages = pages
        self.type = "printed"

    def display_details(self):
        return "Printed: " + super().display_details() + " | Pages: " + str(self.pages)


class EBook(Book):
    def __init__(self, title, author, isbn, size):
        super().__init__(title, author, isbn)
        self.size = size
        self.type = "ebook"

    def display_details(self):
        return "EBook: " + super().display_details() + " | Size: " + str(self.size) + " MB"


class Library:
    def __init__(self):
        self.books = []

    @log
    def add_resources(self, *books):
        for book in books:
            self.books.append(book)
        print(len(books), "resource(s) added")

    def display_all(self):
        if len(self.books) == 0:
            print("No resources in library")
        for book in self.books:
            print(book.display_details())

    def search(self, **kwargs):
        results = []
        for book in self.books:
            match = True
            if "title" in kwargs and kwargs["title"].lower() not in book.title.lower():
                match = False
            if "author" in kwargs and kwargs["author"].lower() not in book.author.lower():
                match = False
            if "type" in kwargs and kwargs["type"] != book.type:
                match = False
            if match:
                results.append(book)
        return results

    def find(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def get_by_author(self, author):
        for book in self.books:
            if author.lower() in book.author.lower():
                yield book

    @log
    def lend(self, isbn):
        book = self.find(isbn)
        if book is None:
            print("Resource not found")
        elif not book.is_available():
            raise LendingError("This resource is already borrowed")
        else:
            book.set_available(False)
            print(book.title, "lent successfully")

    @log
    def return_book(self, isbn):
        book = self.find(isbn)
        if book is None:
            print("Resource not found")
        else:
            book.set_available(True)
            print(book.title, "returned successfully")


def add_book(library):
    kind = input("1. Printed book  2. EBook: ")
    title = input("Title: ")
    author = input("Author: ")
    isbn = input("ISBN: ")
    if title == "" or author == "" or isbn == "":
        print("Fields cannot be empty")
        return
    if kind == "1":
        pages = int(input("Pages: "))
        library.add_resources(PrintedBook(title, author, isbn, pages))
    elif kind == "2":
        size = float(input("Size in MB: "))
        library.add_resources(EBook(title, author, isbn, size))
    else:
        print("Invalid type")


def search_books(library):
    title = input("Title (enter to skip): ")
    author = input("Author (enter to skip): ")
    kind = input("Type printed/ebook (enter to skip): ")
    filters = {}
    if title != "":
        filters["title"] = title
    if author != "":
        filters["author"] = author
    if kind != "":
        filters["type"] = kind
    if len(filters) == 0:
        print("Enter at least one search value")
        return
    results = library.search(**filters)
    if len(results) == 0:
        print("No resource found")
    for book in results:
        print(book.display_details())


def show_by_author(library):
    author = input("Author: ")
    if author == "":
        print("Author cannot be empty")
        return
    for book in library.get_by_author(author):
        print(book.display_details())


def main():
    library = Library()
    library.add_resources(
        PrintedBook("Clean Code", "Robert Martin", "111", 464),
        EBook("Clean Architecture", "Robert Martin", "222", 8.2),
        PrintedBook("Python Crash Course", "Eric Matthes", "333", 544),
    )
    while True:
        print("\n1. Add resource")
        print("2. Display all")
        print("3. Search")
        print("4. Lend")
        print("5. Return")
        print("6. Show by author (generator)")
        print("0. Exit")
        choice = input("Enter choice: ")
        try:
            if choice == "1":
                add_book(library)
            elif choice == "2":
                library.display_all()
            elif choice == "3":
                search_books(library)
            elif choice == "4":
                library.lend(input("ISBN: "))
            elif choice == "5":
                library.return_book(input("ISBN: "))
            elif choice == "6":
                show_by_author(library)
            elif choice == "0":
                break
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid number entered")
        except LendingError as e:
            print("Error:", e)


main()
