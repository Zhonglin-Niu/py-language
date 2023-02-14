from enum import Enum
from typing import Literal


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
    def __init__(self, body: list[Stmt]) -> None:
        super().__init__(kind="Program")
        self.body = body


class Expr(Stmt):
    pass


class BinaryExpr(Stmt):
    def __init__(self, leftExpr: Expr, rightExpr: Expr, operator: str) -> None:
        super().__init__(kind="BinaryExpr")
        self.left = leftExpr
        self.right = rightExpr
        self.operator = operator


class Identifier(Expr):
    def __init__(self, symbol: str) -> None:
        super().__init__(kind="Identifier")
        self.symbol = symbol


class NumericLiteral(Expr):
    def __init__(self, value: int) -> None:
        super().__init__("NumericLiteral")
        self.value = value
