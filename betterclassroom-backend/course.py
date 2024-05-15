from typing import List

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository

from exercise import Exercise


class Course(BaseModel):
    id: str
    description: str
    exercises: List[Exercise]
    participants: List[str]
    classroom: str
    professor: str


class CourseRepository(AbstractRepository[Course]):
    class Meta:
        collection_name = "course"
