class PyException(Exception):
    def __init__(self, msg: object) -> None:
        self.msg = msg

    def print(self) -> None:
        print(
            f"\n\u001b[36;1m{self.__class__.__name__}\u001b[0m: \"{self.msg}\"\n")


class ParseError(PyException):
    pass


class InterpretError(PyException):
    pass


class TokenizeError(PyException):
    pass


class VarExistsError(PyException):
    pass


class RuntimeError(PyException):
    pass
