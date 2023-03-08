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
        raise VarExistsError(
            f"Can't declare variable {gr(declaration.identifier)}. As it is already defined.")

    value = evaluate(
        declaration.value, env
    ) if declaration.value else NullVal()
    return env.declare_var(declaration.identifier, value, declaration.is_const)


def eval_assignment(assignment: AssignmentExpr, env: Environment) -> RuntimeVal:
    if assignment.assign.kind != "Identifier":
        raise InterpretError(f"Invalid assigned object")

    assert isinstance(assignment.assign, Identifier)
    return env.assign_var(assignment.assign.symbol, evaluate(assignment.value, env))

def eval_object_expr(obj: ObjectLiteral, env: Environment) -> RuntimeVal:
    object = ObjectVal()
    
    for item in obj.properties:
        value = env.lookup_var(item.key) if not item.value else evaluate(item.value, env)
        object.properties.update({item.key: value})

    return object

def eval_list_expr(arr: ListLiteral, env: Environment) -> RuntimeVal:
    array = ListVal()

    for item in arr.body:
        if item.kind == "Identifier":
            assert isinstance(item, Identifier)
            value = env.lookup_var(item.symbol)
        else:
            value = evaluate(item, env)

        array.items.append(value)
    
    return array

def eval_call_expr(expr: CallExpr, env: Environment) -> RuntimeVal:
    fn = evaluate(expr.caller, env)

    if fn.type != "native-fn":
        raise InterpretError(f"Function {fn} is not implemented")
    
    args: list[RuntimeVal] = []
    for arg in expr.args:
        args.append(evaluate(arg, env))

    assert isinstance(fn, NativeFnValue)
    rst = fn.call(args, env)
    return rst

def evaluate(astNode: Stmt, env: Environment) -> RuntimeVal:
    match astNode.kind:
        case "NumericLiteral":
            assert isinstance(astNode, NumericLiteral)
            return NumberVal(astNode.value)
        case "StringLiteral":
            assert isinstance(astNode, StringLiteral)
            return StringVal(astNode.value)
        case "Identifier":
            assert isinstance(astNode, Identifier)
            return eval_identifier(astNode, env)
        case "ObjectLiteral":
            assert isinstance(astNode, ObjectLiteral)
            return eval_object_expr(astNode, env)
        case "CallExpr":
            assert isinstance(astNode, CallExpr)
            return eval_call_expr(astNode, env)
        case "ListLiteral":
            assert isinstance(astNode, ListLiteral)
            return eval_list_expr(astNode, env)
        case "BinaryExpr":
            assert isinstance(astNode, BinaryExpr)
            return eval_binary_expr(astNode, env)
        case "Program":
            assert isinstance(astNode, Program)
            return eval_program(astNode, env)
        case "VarDeclaration":
            assert isinstance(astNode, VarDeclaration)
            return eval_var_declaration(astNode, env)
        case "AssignmentExpr":
            assert isinstance(astNode, AssignmentExpr)
            return eval_assignment(astNode, env)
        case _:
            raise InterpretError(
                f"This AST Node has not yet been setup for interpretation: <{gr(astNode.kind)}>")
