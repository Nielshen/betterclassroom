from typing import Dict
from pydantic import BaseModel, Field
from pydantic_mongo import AbstractRepository


class Student(BaseModel): #Problem für Zukunft, wenn zwei courses mit selben studenten existieren, überschreibt sich der ältere Student mit dem neuen
    id: str
    table: int
    course: str
    progress: Dict[str, bool] = Field(default_factory=dict) #str ist exercise_id?
    help_requested: bool = False


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "student"
