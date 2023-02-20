from .values import *
from typing import TypeVar
from .exceptions import *
from .colored_text import *
from .values import RuntimeVal

EnvironmentType = TypeVar('EnvironmentType', bound='Environment')


class Environment:
    def __init__(self, parent: EnvironmentType | None = None) -> None:
        self.__parent = parent
        self.__variables: dict[str, RuntimeVal] = {}
        self.__constants: set[str] = set()

    def declare_var(
        self, var_name: str, value: RuntimeVal, is_const: bool = False
    ) -> RuntimeVal:
        if self.__variables.get(var_name):
            raise VarExistsError(
                f"Can't declare variable {gr(var_name)}. As it is already defined.")

        self.__variables.update({var_name: value})

        if is_const:
            self.__constants.add(var_name)

        return value

    def assign_var(self, var_name: str, value: RuntimeVal) -> RuntimeVal:
        env = self.resolve(var_name)

        if var_name in env.__constants:
            raise VarExistsError(
                f"Can't reassign constan variable {gr(var_name)}")

        env.__variables.update({var_name: value})
        return value

    def lookup_var(self, var_name: str) -> RuntimeVal:
        env = self.resolve(var_name)
        return env.__variables.get(var_name, NullVal())

    def has_var(self, var_name: str) -> bool:
        if self.__variables.get(var_name):
            return True
        else:
            return False

    def resolve(self: EnvironmentType, var_name: str) -> EnvironmentType:
        if self.__variables.get(var_name):
            return self

        if not self.__parent:
            raise RuntimeError(
                f"Can't resolve {gr(var_name)} as it is undefined.")

        return self.__parent.resolve(var_name)
