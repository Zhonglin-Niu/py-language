import sys
import traceback

from .colored_text import gr


class PyException(Exception):
    def __init__(self, msg: object) -> None:
        self.msg = msg

    def print(self) -> None:
        _, _, exc_traceback = sys.exc_info()  # exc_type, exc_value, exc_traceback
        tb = traceback.extract_tb(exc_traceback)[-1]  # Get the last traceback item
        f_name, lino, func_name, _ = tb
        print(f"\n{f_name} line: {gr(lino)} func: {gr(func_name)}")
        print(
            f"\n\t\u001b[36;1m{self.__class__.__name__}\u001b[0m: \"{self.msg}\"\n"
        )


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
