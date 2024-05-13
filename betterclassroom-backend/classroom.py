from typing import List

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Table(BaseModel):
    _id: int
    occupied: bool


class Classroom(BaseModel):
    _id: str
    tablesPerRow: int
    rows: int
    tables: List[Table]


class ClassroomRepository(AbstractRepository[Classroom]):
    class Meta:
        collectionName = 'classroom'
