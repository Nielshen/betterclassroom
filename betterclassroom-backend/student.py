from typing import Dict, Optional
from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository


class Student(BaseModel):
    id: str
    table: int
    course: str
    progress: Dict[str, bool] = Field(default_factory=dict)
    help_requested: bool = False


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "student"
