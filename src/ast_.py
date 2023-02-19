from enum import Enum
import json
from typing import Literal, TypedDict


NodeType = Literal[
    "Program",
    "NumericLiteral",
    "Identifier",
    "BinaryExpr",
]


class Stmt:
    def __init__(self, kind: NodeType) -> None:
        self.kind: NodeType = kind


class Program(Stmt):
    def __init__(self) -> None:
        super().__init__(kind="Program")
        self.body: list[Stmt] = []

    def __repr__(self) -> str:
        info_dict = {
            "kind": self.kind,
            "body": self.body
        }
        return str(info_dict)
    
    def print(self) -> None:
        a = json.loads(self.__repr__().replace("'", "\""))
        print(json.dumps(a, indent=2, ensure_ascii=False))


class Expr(Stmt):
    pass


class BinaryExpr(Expr):
    def __init__(self, leftExpr: Expr, rightExpr: Expr, operator: str) -> None:
        super().__init__(kind="BinaryExpr")
        self.left = leftExpr
        self.right = rightExpr
        self.operator = operator

    def __repr__(self) -> str:
        info_dict = {
            "kind": self.kind,
            "left": self.left,
            "right": self.right,
            "operator": self.operator
        }
        return str(info_dict)


class Identifier(Expr):
    def __init__(self, symbol: str) -> None:
        super().__init__(kind="Identifier")
        self.symbol = symbol

    def __repr__(self) -> str:
        info_dict = {
            "kind": self.kind,
            "symbol": self.symbol
        }
        return str(info_dict)


class NumericLiteral(Expr):
    def __init__(self, value: str) -> None:
        super().__init__("NumericLiteral")
        self.value = float(value)

    def __repr__(self) -> str:
        info_dict = {
            "kind": self.kind,
            "value": self.value
        }
        return str(info_dict)

