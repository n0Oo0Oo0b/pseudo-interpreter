# import click
#
# from .interpreter.programs import Program
#
#
# @click.group(invoke_without_command=True)
# @click.pass_context
# def cli(ctx: click.Context):
#     if ctx.invoked_subcommand:
#         return
#
#     click.echo("REPL is under construction")
#
#
# @cli.command()
# @click.argument("file", type=click.File())
# def run(file):
#     code = file.read()
#     code += "\n"
#     program = Program.from_code(code)
#     program.execute()


if __name__ == "__main__":
    # cli()
    from cambridgeScript.parser.lexer import parse_tokens
    from cambridgeScript.parser.parser import Parser
    from cambridgeScript.interpreter.variables import VariableState
    from cambridgeScript.interpreter.interpreter import Interpreter

    tokens = parse_tokens(open(0).read())
    for token in tokens:
        print(token)
    parsed = Parser.parse_program(tokens)
    print(parsed)
    interpreter = Interpreter(VariableState())
    interpreter.visit(parsed)
