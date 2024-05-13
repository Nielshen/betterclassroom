from typing import Dict
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository

from exercise import Exercise
from classroom import Table


class Student(BaseModel):
    _id: str
    table: Table
    progress: Dict[Exercise, bool]


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = 'student'
