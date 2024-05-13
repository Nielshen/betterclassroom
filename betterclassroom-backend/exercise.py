from typing import List

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class SubExercise(BaseModel):
    _id: str
    description: str


class Exercise(BaseModel):
    _id: str
    description: str
    exercises: List[SubExercise]


class ExerciseRepository(AbstractRepository[Exercise]):
    class Meta:
        collection_name = 'exercise'
