from __future__ import annotations
from pathlib import Path
from typing import Any
from uuid import UUID
import uuid
import yaml
from exdb_data.schemas import Exercise

def get_file_contents(file: Path | str) -> dict[str, Any]:
    with open(str(file), "r") as fp:
        data = yaml.load(fp, Loader=yaml.SafeLoader)
    return data

def generate_guid() -> UUID:
    return uuid.uuid4()

def get_exercise(filepath: str) -> Exercise:
    raw_data = get_file_contents(filepath)
    print(raw_data)
    return Exercise.model_validate(raw_data)