from .ast_ import *
from .lexer import tokenize, Token, TokenType
from .exceptions import ParseError
from .colored_text import *


class Parser:
    def __init__(self) -> None:
        self.tokens: list[Token] = []

    def not_eof(self) -> bool:
        return self.tokens[0].type != TokenType.EOF

    def at(self) -> Token:
        return self.tokens[0]

    def eat(self) -> Token:
        return self.tokens.pop(0)

    def expect(self, type_: TokenType, expect: str | None = None) -> Token:
        prev = self.eat()
        expect = type_.value if expect is None else expect
        if prev.type != type_:
            raise ParseError(
                f"Unexpected token found during parsing, expected \"{gr(expect)}\""
            )
        return prev

    def produce_ast(self, source_code: str) -> Program:
        self.tokens = tokenize(source_code)
        program = Program()

        # Parse until the end of the file
        while self.not_eof():
            program.body.append(self.parse_stmt())
        return program

    def parse_stmt(self) -> Stmt:
        # skip to parse expression
        match self.at().type:
            case TokenType.Let | TokenType.Const:
                return self.parse_var_declaration()
            case TokenType.Fn:
                return self.parse_fn_declaration()
            case _:
                return self.parse_expr()

    def parse_var_declaration(self) -> Stmt:
        # let ident;
        # (let | const) ident = expr;
        is_const = self.eat().type == TokenType.Const
        identifier = self.expect(TokenType.Identifier, "an identifier").value

        if self.at().type == TokenType.Semicolon:
            self.eat()
            if is_const:
                raise ParseError(
                    f"Constant variables must have an initialized value")
            return VarDeclaration(is_const, identifier)

        self.expect(TokenType.Equals)
        decalaration = VarDeclaration(is_const, identifier, self.parse_expr())
        self.expect(TokenType.Semicolon)

        return decalaration

    def parse_fn_declaration(self) -> Stmt:
        self.eat()
        name = self.expect(TokenType.Identifier, "function name after fn keyword").value
        args = self.parse_args()
        params: list[str] = []

        for arg in args:
            if arg.kind != "Identifier":
                raise ParseError("Inside function declaration expected parameters to be a type of string")
            assert isinstance(arg, Identifier)
            params.append(arg.symbol)

        self.expect(TokenType.OpenBrace)
        body: list[Stmt] = []

        while self.at().type not in [TokenType.EOF, TokenType.CloseBrace]:
            body.append(self.parse_stmt())

        self.expect(TokenType.CloseBrace)

        fn = FunctionDeclaration(params, name, body)
        return fn

    def parse_expr(self) -> Expr:
        return self.parse_assignment_expr()

    def parse_assignment_expr(self) -> Expr:
        left = self.parse_obj_expr()

        if self.at().type == TokenType.Equals:
            self.eat()
            value = self.parse_assignment_expr()
            return AssignmentExpr(left, value)

        return left

    def parse_obj_expr(self) -> Expr:
        if self.at().type not in [TokenType.OpenBrace, TokenType.OpenBracket]:
            return self.parse_additive_expr()

        if self.eat().type == TokenType.OpenBrace:
            properties: list[Property] = []

            # parse each key-value pairs
            while self.not_eof() and self.at().type != TokenType.CloseBrace:
                key = self.expect(TokenType.Identifier,
                                  "an identifier as key of an object").value
                if self.at().type == TokenType.Comma:
                    self.eat()
                    properties.append(Property(key))
                    continue
                elif self.at().type == TokenType.CloseBrace:
                    properties.append(Property(key))
                    continue

                self.expect(TokenType.Colon)
                value = self.parse_expr()
                properties.append(Property(key, value))

                if self.at().type != TokenType.CloseBrace:
                    self.expect(TokenType.Comma)
            self.expect(TokenType.CloseBrace)
            return ObjectLiteral(properties)

        # must be self.eat().type == TokenType.OpenBracket
        else:
            listLiteral = ListLiteral()

            while self.not_eof() and self.at().type != TokenType.CloseBracket:
                item = self.parse_expr()
                listLiteral.body.append(item)

                if self.at().type != TokenType.CloseBracket:
                    self.expect(TokenType.Comma)

            self.expect(TokenType.CloseBracket)
            return listLiteral

    def parse_additive_expr(self) -> Expr:
        left = self.parse_multiplicative_expr()

        while self.at().value in "+-":
            operator = self.eat().value
            right = self.parse_multiplicative_expr()
            left = BinaryExpr(left, right, operator)

        return left

    def parse_multiplicative_expr(self) -> Expr:
        left = self.parse_call_member_expr()

        while self.at().value in "*/%":
            operator = self.eat().value
            right = self.parse_call_member_expr()
            left = BinaryExpr(left, right, operator)

        return left

    def parse_call_member_expr(self) -> Expr:
        member = self.parse_member_expr()

        if self.at().type == TokenType.OpenParen:
            return self.parse_call_expr(member)

        return member

    def parse_call_expr(self, caller: Expr) -> Expr:
        args = self.parse_args()
        call_expr: Expr = CallExpr(args, caller)

        if self.at().type == TokenType.OpenParen:
            call_expr = self.parse_call_expr(call_expr)

        return call_expr

    def parse_args(self) -> list[Expr]:
        self.expect(TokenType.OpenParen)

        if self.at().type == TokenType.CloseParen:
            args = []
        else:
            args = self.parse_arguments_list()

        self.expect(TokenType.CloseParen)

        return args

    def parse_arguments_list(self) -> list[Expr]:
        args = [self.parse_assignment_expr()]

        while self.at().type == TokenType.Comma and self.eat():
            args.append(self.parse_assignment_expr())

        return args

    def parse_member_expr(self) -> Expr:
        obj = self.parse_primary_expr()

        while self.at().type in [TokenType.Dot, TokenType.CloseBracket]:
            operator = self.eat()

            if operator.type == TokenType.Dot:
                computed = False
                prop = self.parse_primary_expr()

                if prop.kind != "Identifier":
                    raise ParseError(
                        "Can't use dot operator without right hand side being an identifier")

            else:
                computed = True
                prop = self.parse_expr()
                self.expect(TokenType.CloseBracket)

            obj = MemberExpr(obj, prop, computed)

        return obj

    def parse_primary_expr(self) -> Expr:
        match self.at().type:
            case TokenType.Identifier:
                return Identifier(self.eat().value)
            case TokenType.Number:
                return NumericLiteral(self.eat().value)
            case TokenType.OpenParen:
                self.eat()
                value = self.parse_expr()
                self.expect(TokenType.CloseParen)
                return value
            case TokenType.String:
                return StringLiteral(self.eat().value)
            case _:
                raise ParseError(
                    f"Unexpected token found during parsing expr! -> {gr(self.at().value)}"
                )


if __name__ == "__main__":
    parser = Parser()
    try:
        print(parser.produce_ast("1 + 1 = 2"))
    except ParseError as e:
        e.print()
