from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import requests
from app.database import get_db, SessionLocal
from app import models
from app.services.db_service import set_user_repo

router = APIRouter(prefix="/repos", tags=["Repos"])

@router.get("/list")
def list_repos(username: str, db: Session = Depends(get_db)):
    """List user repos"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    headers = {"Authorization": f"Bearer {user.github_token}"}
    response = requests.get("https://api.github.com/user/repos", headers=headers)

    if response.status_code != 200:
        return JSONResponse({"error": "Failed to fetch repos"}, status_code=400)

    return response.json()

@router.post("/create")
def create_repo(username: str, repo_name: str, db: Session = Depends(get_db)):
    """Create a new repo"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    headers = {"Authorization": f"Bearer {user.github_token}"}
    data = {"name": repo_name, "private": False}
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

    if response.status_code != 201:
        return JSONResponse({"error": "Failed to create repo"}, status_code=400)

    # Save repo in DB
    set_user_repo(db, username, repo_name)

    return {"message": "Repo created successfully", "repo_name": repo_name}

@router.post("/select")
def select_repo(username: str, repo_name: str, db: Session = Depends(get_db)):
    """Select an existing repo for LeetAgent"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    set_user_repo(db, username, repo_name)

    return {"message": "Repo selected successfully", "repo_name": repo_name}
