#!/home/loya/py-language/venv/bin/python
from src.exceptions import *
from src.parser_ import Parser
from src.interpreter import *
from src.environment import Environment
from src.interpreter import BooleanVal

import sys


def repl():
    parser = Parser()
    print("\nRepl v0.1")

    while True:
        try:
            code = input(">>>")
        except (EOFError, KeyboardInterrupt):
            print("\n\nexiting......\n")
            break

        code = code.strip()
        if not code:
            continue
        if code == "exit":
            print("\nexiting......\n")
            break

        try:
            program = parser.produce_ast(code)
            # program.print()

            rst = evaluate(program, env)
            print(rst)
        except PyException as e:
            e.print()


if __name__ == "__main__":
    env = Environment()
    d = Environment(env)
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        codes = f.read()
        f.close()

        try:
            parser = Parser()
            program = parser.produce_ast(codes)
            program.print()

            rst = evaluate(program, env)
            print(rst)
        except PyException as e:
            e.print()
    else:
        repl()
