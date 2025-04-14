from __future__ import annotations
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

class Exercise(BaseModel):
    guid: UUID
    uri: URIString
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
    