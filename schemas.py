from pydantic import BaseModel, Field
from uuid import UUID

class RepoCreate(BaseModel):
    owner: str = Field(..., min_length=1, max_length=100)
    repo_name: str = Field(..., min_length=1, max_length=100)

class RepoResponse(BaseModel):
    id: UUID
    owner: str
    repo_name: str
    stars: int

    class Config:
        from_attributes = True