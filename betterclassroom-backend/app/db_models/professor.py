from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Professor(BaseModel):
    id: int
    name: str
    password: str
    firstName : str
    lastName : str


class ProfessorRepository(AbstractRepository[Professor]):
    class Meta:
        collection_name = "professor"
