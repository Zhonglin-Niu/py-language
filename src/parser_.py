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

    def expect(self, type_: TokenType) -> Token:
        prev = self.eat()
        if prev.type != type_:
            raise ParseError(
                f"Unexpected token found during parsing, expected \"{gr(type_.value)}\""
            )
        return prev

    def produce_ast(self, source_code: str) -> Program:
        self.tokens = tokenize(source_code)
        # print(self.tokens)
        program = Program()

        # Parse until the end of the file
        while self.not_eof():
            program.body.append(self.parse_stmt())
        return program

    def parse_stmt(self) -> Stmt:
        # skip to parse expression
        return self.parse_expr()

    def parse_expr(self) -> Expr:
        return self.parse_additive_expr()

    def parse_additive_expr(self) -> Expr:
        left = self.parse_multiplicative_expr()

        while self.at().value in "+-":
            operator = self.eat().value
            right = self.parse_multiplicative_expr()
            left = BinaryExpr(left, right, operator)

        return left

    def parse_multiplicative_expr(self) -> Expr:
        left = self.parse_primary_expr()

        while self.at().value in "*/%":
            operator = self.eat().value
            right = self.parse_primary_expr()
            left = BinaryExpr(left, right, operator)

        return left

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
            case _:
                raise ParseError(
                    f"Unexpected token found during parsing! -> {gr(self.at().value)}"
                )


if __name__ == "__main__":
    parser = Parser()
    try:
        print(parser.produce_ast("1 + 1 = 2"))
    except ParseError as e:
        e.print()
