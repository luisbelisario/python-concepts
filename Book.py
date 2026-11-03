class Book:

    _catalog : list = []

    @classmethod
    def add_to_catalog(cls, book):
        cls._catalog.append(book)

    @classmethod
    def from_isbn(cls, isbn: str):
        for book in cls._catalog:
            if book.isbn == isbn:
                return book
        return None

    @staticmethod
    def validate_isbn(isbn: str) -> bool:
        return len(isbn) == 13 and isbn.isascii() and isbn.isdecimal()

    def __init__(self, title, author, isbn):
        if not type(self).validate_isbn(isbn):
            raise ValueError("Invalid ISBN. It must be a 13-digit number.")
        self.title = title
        self.author = author
        self.isbn = isbn
        type(self)  .add_to_catalog(self)
    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}"


def main():
    correctIsbn = Book.validate_isbn("9783161484100")
    wrongIsbn = Book.validate_isbn("978-3-16-148410-0")
    print(f"Is the ISBN 9783161484100 valid? {correctIsbn}")
    print(f"Is the ISBN 978-3-16-148410-0 valid? {wrongIsbn}")
    Book("1984", "Orwell", "9780451524935")
    try:
        Book("1984", "Orwell", "invalid")
    except ValueError as e:
        print(e)
    bookFound = Book.from_isbn("9780451524935")
    print(bookFound)
    bookNotFound = Book.from_isbn("00000000000000")
    print(bookNotFound)


if __name__ == "__main__":
    main()