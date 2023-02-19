from typing import Literal


ValueType = Literal[
    "null",
    "number",
    "boolean"
]


class RuntimeVal:
    def __init__(self, type_: ValueType) -> None:
        self.type = type_
        self.value: object = ""

    def __repr__(self) -> str:
        return str(self.__dict__)
        return str(self.type) + str(self.value)


class NullVal(RuntimeVal):
    def __init__(self) -> None:
        super().__init__("null")
        self.value = None


class NumberVal(RuntimeVal):
    def __init__(self, value: float) -> None:
        super().__init__("number")
        self.value = value

class BooleanVal(RuntimeVal):
    def __init__(self, value: bool = True) -> None:
        super().__init__("boolean")
        self.value = value
