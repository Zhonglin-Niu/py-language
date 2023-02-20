from enum import Enum
import string

from .exceptions import TokenizeError
from .colored_text import gr


class TokenType(Enum):
    Number = "0123456789"
    Identifier = string.ascii_letters + "_"
    Equals = "="
    OpenParen = "("
    CloseParen = ")"
    BinaryOperator = "+-*/%"
    EOF = "EOF"
    Let = "let"
    Const = "const"
    Semicolon = ";"


KEYWORDS: dict[str, TokenType] = {
    "let": TokenType.Let,
    "const": TokenType.Const
}


class Token:
    def __init__(self, value: str, type_: TokenType) -> None:
        self.value = value
        self.type = type_

    def __repr__(self) -> str:
        return f"<{self.type.name}>"

    def __str__(self) -> str:
        return f"<{self.type.name}: {self.value}>"

    def __format__(self, spec: str = "short") -> str:
        spec = "long" if not spec else spec
        if spec == "long":
            return f"<{self.type.name}: {self.value}>"
        else:
            return self.__repr__()


def tokenize(source_code: str) -> list[Token]:
    tokens: list[Token] = []
    src: list[str] = [i for i in source_code]

    # Build each token until the end of file
    while (len(src) > 0):
        if src[0] == TokenType.OpenParen.value:
            tokens.append(Token(src.pop(0), TokenType.OpenParen))

        elif src[0] == TokenType.CloseParen.value:
            tokens.append(Token(src.pop(0), TokenType.CloseParen))

        elif src[0] in TokenType.BinaryOperator.value:
            tokens.append(Token(src.pop(0), TokenType.BinaryOperator))

        elif src[0] == TokenType.Equals.value:
            tokens.append(Token(src.pop(0), TokenType.Equals))

        elif src[0] == TokenType.Semicolon.value:
            tokens.append(Token(src.pop(0), TokenType.Semicolon))

        else:
            # Handle multicharacter tokens

            # Build number token
            if src[0].isdigit():
                num = ""
                while (len(src) > 0 and src[0].isdigit()):
                    num += src.pop(0)

                tokens.append(Token(num, TokenType.Number))

            elif src[0].isalpha():
                identifier = ""
                while (len(src) > 0 and src[0].isalpha()):
                    identifier += src.pop(0)

                # check for reserved keywords
                reserved = KEYWORDS.get(identifier)
                if reserved:
                    # print(reserved)
                    tokens.append(Token(identifier, reserved))
                else:
                    tokens.append(Token(identifier, TokenType.Identifier))

            elif src[0] in " \n\t":  # skippable
                src.pop(0)

            else:
                raise TokenizeError(
                    f"Unrecognized character found in source: \"{gr(src[0])}\""
                )

    tokens.append(Token(TokenType.EOF.value, TokenType.EOF))
    return tokens


if __name__ == "__main__":
    [print(i) for i in tokenize("let x = 1 * (4 +6)")]
