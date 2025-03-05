class MyClass:
    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        print("Exiting the context")
        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
            return True

    def test_raise_error(self):
        raise ValueError("hihihihihahaha")

with MyClass() as myclass:
    myclass.test_raise_error()