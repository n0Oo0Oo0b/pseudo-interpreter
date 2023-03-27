from cambridgeScript.interpreter.programs import Program
import sys

help_message = """CLI
SUBCOMMANDS:
\trun - USAGE: run <file_name>
\t\texecute a file
\thelp - USAGE: help
\t\tprints this help message"""


def cli():
    sliced_argv = sys.argv[1:]
    assert len(sliced_argv) > 0, "requires one subcommand, try subcommand 'help'"
    subcommand = sliced_argv[0]
    if subcommand == "run":
        assert len(sliced_argv) > 1, "requires file name"
        with open(sliced_argv[1], "r") as f:
            p = Program.from_code(f.read())
            print(p)
            p.execute()
    elif subcommand == "help":
        print(help_message)
    else:
        assert False, "not a valid subcommand"


if __name__ == "__main__":
    cli()
    # p = Program.from_code(open(0).read())
    # print(p)
    # p.execute()
