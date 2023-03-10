from .values import NullVal, NumberVal, RuntimeVal, BooleanVal, NativeFnValue, FunctionValue
from typing import TypeVar
from .exceptions import *
from .colored_text import *

EnvironmentType = TypeVar('EnvironmentType', bound='Environment')


class Funcs:
    def print(self, args, env: EnvironmentType) -> NullVal:
        print(args)
        return NullVal()

    def max(self, args: list[NumberVal], env: EnvironmentType) -> NumberVal:
        nums = [number.value for number in args]
        return NumberVal(max(nums))


class Environment:
    def __init__(self, parent: EnvironmentType | None = None) -> None:
        self.parent = parent
        self.__variables: dict[str, RuntimeVal] = {}
        self.__constants: set[str] = set()
        self.set_globals_if_needed()

    def set_globals_if_needed(self) -> None:
        if not self.parent:
            f = Funcs()
            self.declare_var("true", BooleanVal(), True)
            self.declare_var("false", BooleanVal(False), True)
            self.declare_var("null", NullVal(), True)
            self.declare_var("print", NativeFnValue(f.print), True)
            self.declare_var("max", NativeFnValue(f.max), True)

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
                f"Can't reassign constant variable {gr(var_name)}")

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

        if not self.parent:
            raise RuntimeError(
                f"Can't resolve {gr(var_name)} as it is undefined.")

        return self.parent.resolve(var_name)
