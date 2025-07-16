import click
import uuid

from exdb_data.schemas import ExecutionType, ExecutionTypeChoices
from exdb_data.services import (
    create_exercise_yaml,
    get_exercise,
    export_exercises_to_json,
    pp_short_exercise,
    read_all_exercises,
    read_exported_exercises_json,
)
from rich import get_console

console = get_console()


@click.group(name="exercises")
@click.pass_context
def exercises_group(ctx: click.Context):
    pass


@exercises_group.command(name="generate-uuid")
def generate_uuid():
    # ensures uuid is unique across major classes (right now just exercises, evt. muscles, equipment, etc.)
    exercises = read_all_exercises()
    current_uuids = [str(ex.guid) for ex in exercises]
    collisions = 0
    while collisions < 5:
        new_uuid = uuid.uuid4()
        if str(new_uuid) not in current_uuids:
            break
        else:
            console.print("UUID collision: {new_uuid} already taken.")
            collisions += 1
    console.print(new_uuid)


@exercises_group.command(name="validate")
@click.argument("filepath")
def validate_cmd(filepath: str) -> None:
    ex = get_exercise(filepath)
    console.print(ex)


@exercises_group.command(name="create")
@click.option("--uri", type=str, required=True)
@click.option("--name", type=str, required=True)
@click.option(
    "--execution-type",
    type=click.Choice(ExecutionTypeChoices),
    default="WEIGHT_REPS",
    required=False,
)
@click.option("--test", type=bool, required=False, default=False)
def create_new_exercise_cmd(
    uri: str, name: str, execution_type: ExecutionType, test
) -> None:
    output_path = create_exercise_yaml(uri, name, execution_type, test)
    console.print(f"created at: {output_path}")


@exercises_group.command(name="search")
@click.argument("name")
def search_cmd(name: str) -> None:
    v = name.strip().lower()
    exercises = read_all_exercises()

    if v == "*":
        filtered = exercises
    else:
        filtered = []
        for ex in exercises:
            search_values = [ex.uri]
            for e in ex.translations:
                search_values.append(e.uri.lower())
                search_values.append(e.name.lower())
                for an in e.alternative_names:
                    search_values.append(an.strip().lower())
            for sv in search_values:
                if v in sv:
                    filtered.append(ex)
                    break

    for ex in filtered:
        console.print(pp_short_exercise(ex))


@exercises_group.command(name="export-json")
@click.argument("output_filepath", required=False)
def export_json(output_filepath: str | None) -> None:
    if not output_filepath:
        output_filepath = "exercises.json"
    exercises = read_all_exercises()
    export_exercises_to_json(exercises, output_filepath)

    # check for validity
    exported_exercises = read_exported_exercises_json(output_filepath)

    assert len(exported_exercises) == len(exercises)

    console.print(f"Exported {len(exercises)} exercises to {output_filepath}")
