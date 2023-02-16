from .ast_ import Program, Stmt, Expr, BinaryExpr, NumericLiteral, Identifier
from .lexer import tokenize, Token, TokenType
from .exceptions import ParseError


class Parser:
    def __init__(self) -> None:
        self.tokens: list[Token] = []

    def not_eof(self) -> bool:
        return self.tokens[0].type != TokenType.EOF

    def at(self) -> Token:
        return self.tokens[0]

    def eat(self) -> Token:
        return self.tokens.pop(0)

    def produce_ast(self, source_code: str) -> Program:
        self.tokens = tokenize(source_code)
        program = Program()

        # Parse until the end of the file
        while self.not_eof():
            program.body.append(self.parse_stmt())
        return program

    def parse_stmt(self) -> Stmt:
        # skip to parse expression
        return self.parse_expr()

    def parse_expr(self) -> Expr:
        return self.parse_primary_expr()

    def parse_primary_expr(self) -> Expr:
        match self.at().type:
            case TokenType.Identifier:
                return Identifier(self.eat().value)
            case TokenType.Number:
                return NumericLiteral(self.eat().value)
            case _:
                raise ParseError(
                    f"Unexpected token found during parsing! -> {self.at().value}"
                )


if __name__ == "__main__":
    parser = Parser()
    try:
        print(parser.produce_ast("1 + 1 = 2"))
    except ParseError as e:
        e.print()
