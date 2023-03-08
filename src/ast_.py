from enum import Enum
import json
from typing import Literal, TypedDict


NodeType = Literal[
    # STMT
    "Program",
    "VarDeclaration",

    # EXPR
    "Identifier",
    "Property",
    "NumericLiteral",
    "StringLiteral",
    "AssignmentExpr",
    "MemberExpr",
    "CallExpr",
    "BinaryExpr",
    "ObjectLiteral",
    "ListLiteral"
]


class Stmt:
    def __init__(self, kind: NodeType) -> None:
        self.kind: NodeType = kind

    def __repr__(self) -> str:
        return str(self.__dict__)

    def print(self) -> None:
        repr = self.__repr__()
        replaced_dict = {
            "\'": "\"",
            "True": "\"True\"",
            "False": "\"False\"",
            "None": "\"None\""
        }
        for key, item in replaced_dict.items():
            repr = repr.replace(key, item)

        # print(repr)
        print(json.dumps(json.loads(repr), indent=2))
        # print(self.__dict__)


class Expr(Stmt):
    pass


class Program(Stmt):
    def __init__(self) -> None:
        super().__init__(kind="Program")
        self.body: list[Stmt] = []


class VarDeclaration(Stmt):
    def __init__(
        self, is_const: bool, identifier: str, value: Expr | None = None
    ) -> None:
        super().__init__("VarDeclaration")
        self.is_const = is_const
        self.identifier = identifier
        self.value = value


class Identifier(Expr):
    def __init__(self, symbol: str) -> None:
        super().__init__(kind="Identifier")
        self.symbol = symbol


class NumericLiteral(Expr):
    def __init__(self, value: str) -> None:
        super().__init__("NumericLiteral")
        self.value = float(value)


class StringLiteral(Expr):
    def __init__(self, value: str) -> None:
        super().__init__("StringLiteral")
        self.value = value


class BinaryExpr(Expr):
    def __init__(self, leftExpr: Expr, rightExpr: Expr, operator: str) -> None:
        super().__init__(kind="BinaryExpr")
        self.left = leftExpr
        self.right = rightExpr
        self.operator = operator


class AssignmentExpr(Expr):
    """
    x = { "name": "Jason" }

    x.name = "Taylor"
    """

    def __init__(self, assign: Expr, value: Expr) -> None:
        super().__init__("AssignmentExpr")
        self.assign = assign
        self.value = value


class CallExpr(Expr):
    def __init__(self, args: list[Expr], caller: Expr) -> None:
        super().__init__("CallExpr")
        self.args: list[Expr] = args
        self.caller: Expr = caller


class MemberExpr(Expr):
    def __init__(self, obj: Expr, prop: Expr, computed: bool) -> None:
        super().__init__("MemberExpr")
        self.obj: Expr = obj
        self.prop: Expr = prop
        self.computed: bool = computed


class Property(Expr):
    def __init__(self, key: str, value: Expr | None = None) -> None:
        super().__init__("Property")
        self.key = key
        self.value = value


class ObjectLiteral(Expr):
    def __init__(self, properties: list[Property]) -> None:
        super().__init__("ObjectLiteral")
        self.properties = properties


class ListLiteral(Expr):
    def __init__(self) -> None:
        super().__init__("ListLiteral")
        self.body: list[Expr] = []
