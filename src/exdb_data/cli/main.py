import click
from exdb_data.cli.commands.exercises import exercises_group

@click.group()
@click.pass_context
def cli(ctx: click.Context):
    ctx.obj = {}


cli.add_command(exercises_group)


def main() -> None:
    cli()