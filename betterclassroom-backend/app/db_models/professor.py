from pydantic import BaseModel
from pydantic_mongo import AbstractRepository


class Professor(BaseModel):
    id: int
    email: str
    password: str
    lastName: str
    firstName : str


class ProfessorRepository(AbstractRepository[Professor]):
    class Meta:
        collection_name = "professor"
