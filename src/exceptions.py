class PyException(Exception):
    def __init__(self, msg: object) -> None:
        self.msg = msg

    def print(self) -> None:
        print(f"\n{self.__class__.__name__}: \"{self.msg}\"\n")


class ParseError(PyException):
    def __init__(self, msg: object) -> None:
        super().__init__(msg)
