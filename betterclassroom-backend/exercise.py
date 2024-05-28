from typing import List

from pydantic import BaseModel


class SubExercise(BaseModel):
    id: str
    description: str


class Exercise(BaseModel):
    id: str
    description: str
    exercises: List[SubExercise] #in sub_exercises umbenennen für übersicht?
