from typing import List
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Table(BaseModel):
    id: int
    occupied: bool


class Classroom(BaseModel):
    id: str
    tablesPerRow: int
    rows: int
    tables: List[Table]


class ClassroomRepository(AbstractRepository[Classroom]):
    class Meta:
        collection_name = 'classroom'
