from typing import List

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository

from classroom import Classroom
from professor import Professor
from student import Student
from exercise import Exercise


class Course(BaseModel):
    _id: str
    description: str
    exercises: List[Exercise]
    participants: List[Student]
    classroom: Classroom
    professor: Professor


class CourseRepository(AbstractRepository[Course]):
    class Meta:
        collectionName = 'course'
