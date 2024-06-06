from typing import Dict
from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository


class Student(BaseModel):
    id: str
    table: int
    course: str
    progress: Dict[str, bool] = Field(default_factory=dict)  # str ist exercise_id
    current_exercise: int = 0
    help_requested: bool = False


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "student"
