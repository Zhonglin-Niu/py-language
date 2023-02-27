from typing import Literal


ValueType = Literal[
    "null",
    "number",
    "string",
    "boolean",
    "object"
]


class RuntimeVal:
    def __init__(self, type_: ValueType) -> None:
        self.type = type_

    def __repr__(self) -> str:
        return str(self.__dict__)


class NullVal(RuntimeVal):
    def __init__(self) -> None:
        super().__init__("null")
        self.value = None


class NumberVal(RuntimeVal):
    def __init__(self, value: float) -> None:
        super().__init__("number")
        self.value = value


class StringVal(RuntimeVal):
    def __init__(self, value: str) -> None:
        super().__init__("string")
        self.value = value


class BooleanVal(RuntimeVal):
    def __init__(self, value: bool = True) -> None:
        super().__init__("boolean")
        self.value = value


class ObjectVal(RuntimeVal):
    def __init__(self) -> None:
        super().__init__("object")
        self.properties: dict[str, RuntimeVal] = {}
