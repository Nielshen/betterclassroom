from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Professor(BaseModel):
    _id: str
    name: str


class ProfessorRepository(AbstractRepository[Professor]):
    class Meta:
        collection_name = 'professor'
