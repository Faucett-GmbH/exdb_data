from __future__ import annotations
import os
from pathlib import Path
import re
from typing import Any
from uuid import UUID
import uuid
import yaml
import json
from exdb_data.paths import EXERCISES_DIR
from exdb_data.schemas import ExecutionType, Exercise, ExerciseTranslation


def get_yaml_file_contents(file: Path | str) -> dict[str, Any]:
    with open(str(file), "r") as fp:
        data = yaml.load(fp, Loader=yaml.SafeLoader)
    return data


def get_json_file_contents(file: Path | str) -> dict[str, Any]:
    with open(str(file), "r") as fp:
        data = json.load(fp)
    return data


def get_yaml_files(directory: str):
    path = Path(directory)
    # Matches files like 00001_high_bar_squat.yml
    return sorted(path.glob("[0-9][0-9][0-9][0-9][0-9]_*.yml"))


def generate_guid() -> UUID:
    return uuid.uuid4()


def get_exercise(filepath: str) -> Exercise:
    raw_data = get_yaml_file_contents(filepath)
    return Exercise.model_validate(raw_data)


def pp_short_exercise(ex: Exercise) -> str:
    t = []
    for tr in ex.translations:
        v = f"({tr.locale})({tr.uri})({tr.name})({tr.alternative_names})"
        t.append(v)
    return f"<({ex.guid})({ex.uri}) : {' '.join(t)}>"


def read_all_exercises() -> list[Exercise]:
    exercise_files = get_yaml_files("data/exercises")  # todo add config for this.
    results = []
    for exercise_file in exercise_files:
        ex = get_exercise(exercise_file)
        results.append(ex)
    return results


def read_exported_exercises_json(exported_file_path: str) -> list[Exercise]:
    exercises_raw = get_json_file_contents(exported_file_path)
    exercises = [Exercise.model_validate(ex) for ex in exercises_raw]
    return exercises


def export_exercises_to_json(
    exercises: list[Exercise], output_file: str = "exercises.json"
) -> None:
    data = [exercise.model_dump(mode="json") for exercise in exercises]
    Path(output_file).write_text(json.dumps(data), encoding="utf-8")


def get_next_exercise_filename(exercise_name: str) -> str:
    number_pattern = re.compile(r"^(\d+)_.*\.yml$")
    max_number = 0

    for file_name in os.listdir(EXERCISES_DIR):
        match = number_pattern.match(file_name)
        if match:
            number = int(match.group(1))
            if number > max_number:
                max_number = number

    next_number = max_number + 1
    next_number_str = f"{next_number:05}"  # zero-padded to 5 digits
    sanitized_name = exercise_name.lower().replace(" ", "_")

    return f"{next_number_str}_{sanitized_name}"


def create_exercise_yaml(
    uri: str,
    name: str,
    execution_type: ExecutionType = "WEIGHT_REPS",
    test: bool = False,
) -> Path:
    ex = Exercise(
        guid=uuid.uuid4(),
        image_url=None,
        thumbnail_image_url=None,
        uri=uri,
        execution=execution_type,
        translations=[
            ExerciseTranslation(
                guid=uuid.uuid4(),
                locale="en",
                uri=uri,
                name=name,
                video_url=None,
                description="",
                summary="",
                instructions="",
            )
        ],
    )

    # get current number
    exercise_filename = get_next_exercise_filename(uri)
    yaml_output = yaml.dump(
        ex.model_dump(mode="json"), sort_keys=False, default_flow_style=False
    )

    output_path = Path(EXERCISES_DIR) / f"{exercise_filename}.yml"

    if os.path.exists(output_path):
        raise FileExistsError(f"file: {output_path} already exists.")

    if not test:
        output_path.write_text(yaml_output, encoding="utf-8")
    else:
        print(output_path)
        print(yaml_output)

    return output_path
