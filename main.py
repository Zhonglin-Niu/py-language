from src.exceptions import ParseError
from src.parser_ import Parser


def repl():
    parser = Parser()
    print("\nRepl v0.1")

    while True:
        code = input("> ")

        if not code:
            continue
        if code == "exit":
            break

        program = parser.produce_ast(code)
        program.print()


if __name__ == "__main__":
    try:
        repl()
    except ParseError as e:
        e.print()
