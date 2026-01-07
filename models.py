from sqlalchemy import Column, Integer, String, Index
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner = Column(String(100), nullable=False)
    repo_name = Column(String(100), nullable=False)
    stars = Column(Integer, nullable=False)

    __table_args__ = (
        Index("idx_owner_repo", "owner", "repo_name"),
    )