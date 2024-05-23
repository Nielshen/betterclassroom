from typing import Dict, Optional
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository

from exercise import Exercise


class Student(BaseModel):
    id: str
    table: str
    course: str
    progress: Optional[Dict[str, bool]]
    help_requested: bool


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "student"
