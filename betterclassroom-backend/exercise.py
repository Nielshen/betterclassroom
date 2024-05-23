from typing import List

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class SubExercise(BaseModel):
    id: str
    description: str


class Exercise(BaseModel):
    id: str
    description: str
    exercises: List[SubExercise]
