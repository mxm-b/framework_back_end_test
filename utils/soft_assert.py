class SoftAssert:
    def __init__(self):
        self.errors_list = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            return False

        if self.errors_list:
            raise AssertionError("\n".join(self.errors_list))

        return False

    def check(self, condition, message):
        if not condition:
            self.errors_list.append(message)

