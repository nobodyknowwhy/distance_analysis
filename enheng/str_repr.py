class BOOK:
    def __init__(self):
        self.p = 1
        self.d = 2

    def __str__(self):
        return f"{self.d} + {self.p}"

    def __repr__(self):
        return f"BOOK('{self.d}, {self.p}')"


book = BOOK()

print(book)