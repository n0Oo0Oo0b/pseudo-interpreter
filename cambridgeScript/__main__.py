import click

from .interpreter.programs import Program


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context):
    if ctx.invoked_subcommand:
        return

    click.echo("REPL is under construction")


@cli.command()
@click.argument("file", type=click.File())
def run(file):
    code = file.read()
    code += "\n"
    program = Program.from_code(code)
    program.execute()


if __name__ == "__main__":
    cli()
