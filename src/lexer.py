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
    OpenBrace = "{"
    CloseBrace = "}"
    OpenBracket = "["
    CloseBracket = "]"
    BinaryOperator = "+-*/%"
    EOF = "EOF"
    Let = "let"
    Const = "const"
    Semicolon = ";"
    Comma = ","
    Colon = ":"
    Quotation = "\""
    String = ""


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


def is_valid_ident_char(char: str, is_first_ident_char=False) -> bool:
    if is_first_ident_char:
        return char in TokenType.Identifier.value
    return char in TokenType.Identifier.value + string.digits


def tokenize(source_code: str) -> list[Token]:
    tokens: list[Token] = []
    src: list[str] = [i for i in source_code]

    # Build each token until the end of file
    while (len(src) > 0):
        if src[0] == TokenType.OpenParen.value:
            tokens.append(Token(src.pop(0), TokenType.OpenParen))

        elif src[0] == TokenType.CloseParen.value:
            tokens.append(Token(src.pop(0), TokenType.CloseParen))

        elif src[0] == TokenType.OpenBrace.value:
            tokens.append(Token(src.pop(0), TokenType.OpenBrace))

        elif src[0] == TokenType.CloseBrace.value:
            tokens.append(Token(src.pop(0), TokenType.CloseBrace))

        elif src[0] == TokenType.OpenBracket.value:
            tokens.append(Token(src.pop(0), TokenType.OpenBracket))

        elif src[0] == TokenType.CloseBracket.value:
            tokens.append(Token(src.pop(0), TokenType.CloseBracket))

        elif src[0] == TokenType.Colon.value:
            tokens.append(Token(src.pop(0), TokenType.Colon))

        elif src[0] == TokenType.Comma.value:
            tokens.append(Token(src.pop(0), TokenType.Comma))

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

            elif is_valid_ident_char(src[0], True):
                identifier = ""
                while (len(src) > 0 and is_valid_ident_char(src[0])):
                    identifier += src.pop(0)

                # check for reserved keywords
                reserved = KEYWORDS.get(identifier)
                if reserved:
                    # print(reserved)
                    tokens.append(Token(identifier, reserved))
                else:
                    tokens.append(Token(identifier, TokenType.Identifier))

            elif src[0] == TokenType.Quotation.value:
                text = ""
                src.pop(0)
                while (len(src) > 0 and src[0] != TokenType.Quotation.value):
                    text += src.pop(0)
                try:
                    src.pop(0)
                except:
                    raise TokenizeError(
                        f"Expected \"{gr(TokenType.Quotation.value)}\" on the both end of a string")
                tokens.append(Token(text, TokenType.String))

            elif src[0] in " \n\t\r":  # skippable
                src.pop(0)

            else:
                raise TokenizeError(
                    f"Unrecognized character found in source: \"{gr(src[0])}\""
                )

    tokens.append(Token(TokenType.EOF.value, TokenType.EOF))
    return tokens


if __name__ == "__main__":
    [print(i) for i in tokenize("let x = 1 * (4 +6)")]
