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
    if lhs.type == "number" and rhs.type == "number":
        assert isinstance(lhs, NumberVal)
        assert isinstance(rhs, NumberVal)
        return eval_numeric_binary_expr(lhs, rhs, binop.operator)
    return NullVal()

def eval_identifier(ident: Identifier, env: Environment) -> RuntimeVal:
    return env.lookup_var(ident.symbol)


def eval_var_declaration(declaration: VarDeclaration, env: Environment) -> RuntimeVal:
    if env.has_var(declaration.identifier):
        raise VarExistsError(f"Can't declare variable {gr(declaration.identifier)}. As it is already defined.")
    if declaration.value:
        return env.declare_var(declaration.identifier, evaluate(declaration.value, env), declaration.is_const)
    else:
        return NullVal()


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
        case "VarDeclaration":
            assert isinstance(astNode, VarDeclaration)
            return eval_var_declaration(astNode, env)
        case _:
            raise InterpretError(
                f"This AST Node has not yet been setup for interpretation: <{gr(astNode.kind)}>")
