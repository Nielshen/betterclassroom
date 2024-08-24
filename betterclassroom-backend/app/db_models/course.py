from pydantic import BaseModel, Field, model_validator
from pydantic_mongo import AbstractRepository
from app.utils.helpers import get_hash
from typing_extensions import Self
from typing import List


class SubExercise(BaseModel):
    id: str = None
    name: str
    description: str

    @model_validator(mode="after")
    def generate_id(self) -> Self:
        if self.id is None:
            self.id = get_hash(self.name)
        return self

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}


class Exercise(BaseModel):
    id: str = None
    name: str
    description: str
    exercises: List[SubExercise] = Field(default_factory=list)
    participants: List[str] = Field(default_factory=list)
    is_active: bool = False

    @model_validator(mode="after")
    def generate_id(self) -> Self:
        if self.id is None:
            self.id = get_hash(self.name)
        return self


class Course(BaseModel):
    id: str = None
    name: str
    description: str
    exercises: List[Exercise] = Field(default_factory=list)
    classroom: str
    professor: str

    @model_validator(mode="after")
    def generate_id(self) -> Self:
        if self.id is None:
            self.id = get_hash(self.name)
        return self


class CourseRepository(AbstractRepository[Course]):
    class Meta:
        collection_name = "course"
