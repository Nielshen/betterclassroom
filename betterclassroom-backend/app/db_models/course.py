from typing import List
from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository


class SubExercise(BaseModel):
    id: str
    description: str

    def to_dict(self):
        return {"id": self.id, "description": self.description}


class Exercise(BaseModel):
    id: str
    description: str
    exercises: List[SubExercise] = Field(
        default_factory=list
    )  # in sub_exercises umbenennen für übersicht?
    participants: List[str] = Field(default_factory=list)  # str ist student id
    is_active: bool = False


class Course(BaseModel):
    id: str
    description: str
    exercises: List[Exercise] = Field(default_factory=list)
    classroom: str
    professor: str


class CourseRepository(AbstractRepository[Course]):
    class Meta:
        collection_name = "course"
