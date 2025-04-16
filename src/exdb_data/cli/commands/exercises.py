import asyncio
import click

from exdb_data.services import get_exercise, export_exercises_to_json, read_all_exercises, read_exported_exercises_json
from rich import get_console

console = get_console()


@click.group(name="exercises")
@click.pass_context
def exercises_group(ctx: click.Context):
    pass


@exercises_group.command(name="validate")
@click.argument('filepath')
def validate_cmd(filepath: str) -> None:
    ex = get_exercise(filepath)
    console.print(ex)


@exercises_group.command(name="export-json")
@click.argument('output_filepath', required=False)
def export_ts(output_filepath: str | None) -> None:
    if not output_filepath:
       output_filepath = "exercises.json"
    exercises = read_all_exercises()
    export_exercises_to_json(exercises, output_filepath)

    # check for validity
    exported_exercises = read_exported_exercises_json(output_filepath)
    print(exported_exercises)

    assert len(exported_exercises) == len(exercises)

    console.print(f"Exported {len(exercises)} exercises to {output_filepath}")

