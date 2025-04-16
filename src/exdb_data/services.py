from __future__ import annotations
from pathlib import Path
from typing import Any
from uuid import UUID
import uuid
import yaml
import json
from exdb_data.schemas import Exercise

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

def read_all_exercises() -> list[Exercise]:
    exercise_files = get_yaml_files("data/exercises") # todo add config for this.
    results = []
    for exercise_file in exercise_files:
        ex = get_exercise(exercise_file)
        results.append(ex)
    return results

def read_exported_exercises_json(exported_file_path: str) -> list[Exercise]:
    exercises_raw = get_json_file_contents(exported_file_path)
    exercises = [Exercise.model_validate(ex) for ex in exercises_raw]
    return exercises


def export_exercises_to_json(exercises: list[Exercise], output_file: str = "exercises.json") -> None:
    data = [exercise.model_dump(mode="json") for exercise in exercises]
    Path(output_file).write_text(json.dumps(data), encoding="utf-8")


