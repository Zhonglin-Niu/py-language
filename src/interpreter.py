from .environment import Environment
from .lexer import TokenType
from .colored_text import gr
from .values import *
from .ast_ import *
from .exceptions import *


def eval_program(prog: Program, env: Environment) -> RuntimeVal:
    lastEvaluated: RuntimeVal = NullVal()

    for stmt in prog.body:
        lastEvaluated = evaluate(stmt, env)

    return lastEvaluated


def eval_numeric_binary_expr(lhs: NumberVal, rhs: NumberVal, operator: str) -> NumberVal:
    if operator in TokenType.BinaryOperator.value:
        rst = eval(f"{lhs.value}{operator}{rhs.value}")
        return NumberVal(rst)
    raise InterpretError(f"Unrecognized operator \"{gr(operator)}\"")


def eval_binary_expr(binop: BinaryExpr, env: Environment) -> RuntimeVal:
    lhs = evaluate(binop.left, env)
    rhs = evaluate(binop.right, env)
    assert isinstance(lhs, NumberVal)
    assert isinstance(rhs, NumberVal)
    if lhs.type == "number" and rhs.type == "number":
        return eval_numeric_binary_expr(lhs, rhs, binop.operator)
    return NullVal()

def eval_identifier(ident: Identifier, env: Environment) -> RuntimeVal:
    return env.lookup_var(ident.symbol)


def evaluate(astNode: Stmt, env: Environment) -> RuntimeVal:
    match astNode.kind:
        case "NumericLiteral":
            assert isinstance(astNode, NumericLiteral)
            return NumberVal(astNode.value)
        case "Identifier":
            assert isinstance(astNode, Identifier)
            return eval_identifier(astNode, env)
        case "BinaryExpr":
            assert isinstance(astNode, BinaryExpr)
            return eval_binary_expr(astNode, env)
        case "Program":
            assert isinstance(astNode, Program)
            return eval_program(astNode, env)
        case _:
            raise InterpretError(
                f"This AST Node has not yet been setup for interpretation: <{gr(astNode.kind)}>")
