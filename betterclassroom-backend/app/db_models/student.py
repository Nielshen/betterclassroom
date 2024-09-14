from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Student(BaseModel):
    id: str
    table: str
    course: str
    exercise: str
    current_exercise: int = 0
    help_requested: bool = False


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "student"
