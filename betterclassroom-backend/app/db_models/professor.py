from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Professor(BaseModel):
    id: str


class ProfessorRepository(AbstractRepository[Professor]):
    class Meta:
        collection_name = "professor"
