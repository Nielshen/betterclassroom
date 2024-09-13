from pydantic import BaseModel
from pydantic_mongo import AbstractRepository
from typing import Optional


class Professor(BaseModel):
    id: str # email
    password: Optional[str]
    lastName: Optional[str]
    firstName : Optional[str]


class ProfessorRepository(AbstractRepository[Professor]):
    class Meta:
        collection_name = "professor"
