from typing import List

from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository

from exercise import Exercise


class Course(BaseModel):
    id: str
    description: str
    exercises: List[Exercise] = Field(default_factory=list)
    participants: List[str] = Field(default_factory=list) #str ist student id
    classroom: str
    professor: int


class CourseRepository(AbstractRepository[Course]):
    class Meta:
        collection_name = "course"
