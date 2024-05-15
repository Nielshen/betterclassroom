from typing import Dict
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository

from exercise import Exercise
from classroom import Table
from course import Course


class Student(BaseModel):
    id: str
    table: Table
    course: str
    progress: Dict[Exercise, bool]


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "student"
