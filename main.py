from src.exceptions import *
from src.parser_ import Parser
from src.interpreter import *
from src.environment import Environment
from src.interpreter import BooleanVal


def repl():
    parser = Parser()
    env = Environment()
    env.declare_var("x", NumberVal(10))
    env.declare_var("true", BooleanVal())
    env.declare_var("false", BooleanVal(False))
    env.declare_var("null", NullVal())
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
    repl()
