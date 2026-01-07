from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import RepoCreate, RepoResponse
from services.github_service import fetch_repo
from crud import create_repo, get_repo, delete_repo
from core.logging_config import logger

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/repos", response_model=RepoResponse, status_code=201)
async def create(payload: RepoCreate, db: Session = Depends(get_db)):
    logger.info("Creating repository entry")
    data = await fetch_repo(payload.owner, payload.repo_name)
    return create_repo(db, {
        "owner": payload.owner,
        "repo_name": payload.repo_name,
        "stars": data["stargazers_count"]
    })

@router.get("/repos/{repo_id}", response_model=RepoResponse)
def read(repo_id, db: Session = Depends(get_db)):
    repo = get_repo(db, repo_id)
    if not repo:
        raise HTTPException(404, "Repository not found")
    return repo

@router.put("/repos/{repo_id}", response_model=RepoResponse)
def update(repo_id, db: Session = Depends(get_db)):
    repo = get_repo(db, repo_id)
    if not repo:
        raise HTTPException(404, "Repository not found")
    repo.stars += 1
    db.commit()
    return repo

@router.delete("/repos/{repo_id}", status_code=204)
def delete(repo_id, db: Session = Depends(get_db)):
    repo = get_repo(db, repo_id)
    if not repo:
        raise HTTPException(404, "Repository not found")
    delete_repo(db, repo)