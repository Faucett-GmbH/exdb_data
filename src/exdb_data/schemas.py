from __future__ import annotations
import enum
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Annotated, Literal, Optional

URIString = Annotated[
    str,
    Field(
        pattern=r"^[a-z][a-z0-9_-]*$", description="url safe unique resource identifier"
    ),
]

LocaleString = Literal["en", "de", "es"]

ExecutionType = Literal[
    "WEIGHT_REPS",
    "REPS_ONLY",
    "DURATION",
    "WEIGHT_DURATION",
    "DISTANCE_DURATION",
    "DISTANCE",
    "WEIGHT_DISTANCE",
]

ExecutionTypeChoices = [
    "WEIGHT_REPS",
    "REPS_ONLY",
    "DURATION",
    "WEIGHT_DURATION",
    "DISTANCE_DURATION",
    "DISTANCE",
    "WEIGHT_DISTANCE",
]


class Exercise(BaseModel):
    guid: UUID
    uri: URIString
    execution: ExecutionType
    image_url: Optional[HttpUrl]
    thumbnail_image_url: Optional[HttpUrl]
    translations: list[ExerciseTranslation]


class ExerciseTranslation(BaseModel):
    guid: UUID
    locale: LocaleString

    # naming
    uri: URIString
    name: str
    alternative_names: list[str] = []

    # metadata
    metadata_keywords: list[str] = Field(default=[])
    metadata_authors: list[str] = Field(default=[])

    # information
    video_url: HttpUrl | None = None
    description: str
    summary: str
    instructions: str
    tips: list[str] = []
