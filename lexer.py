from enum import Enum
import string


class TokenType(Enum):
    Number = "0123456789"
    Identifier = string.ascii_letters + "_"
    Equals = "="
    OpenParen = "("
    CloseParen = ")"
    BinaryOperator = "+-*/"
    Let = "let"


KEYWORDS: dict[str, TokenType] = {
    "let": TokenType.Let
}


class Token:
    def __init__(self, value: str, type_: TokenType) -> None:
        self.value = value
        self.type = type_

    def __repr__(self) -> str:
        return f"<{self.type.name}: {self.value}>"

    def __format__(self, spec: str = "short") -> str:
        spec = "short" if not spec else spec
        if spec == "short":
            return f"<{self.type.name}>"
        else:
            return self.__repr__()


def token(value: str, type_: TokenType) -> Token:
    return Token(value=value, type_=type_)


def tokenize(sourceCode: str) -> list[Token]:
    tokens: list[Token] = []
    src: list[str] = [i for i in sourceCode]

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
                    tokens.append(Token(identifier, reserved))
                else:
                    tokens.append(Token(identifier, TokenType.Identifier))

            elif src[0] in " \n\t":  # skippable
                src.pop(0)

            else:
                raise RuntimeError(
                    f"Unrecognized character found in source: {src[0]}")

    return tokens


print(tokenize("let x = 1 * (4 +6)"))
