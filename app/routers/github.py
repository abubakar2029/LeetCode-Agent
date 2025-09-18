from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from requests import Session
from app import models
from app.services import repo_analyzer
from app.database import SessionLocal
from app.services.github_service import get_user_repos
from app.deps.auth_deps import get_current_user, get_db
from app.utils.security import decrypt_token


router = APIRouter(prefix="/github", tags=["GitHub"])

@router.get("/tree")
def repo_tree(owner: str="abubakar2029", repo: str="leetcode-data-structures-and-algorithms", branch: str = "main", save:bool = True):
    return repo_analyzer.get_repo_tree(owner, repo, branch)

@router.get("/commits")
def repo_commits(owner: str, repo: str, path: str, branch: str = "main", last: int = 5):
    return repo_analyzer.get_commit_history(owner, repo, path, branch, last)


@router.get("/repos")
def list_repos(current_user: models.User = Depends(get_current_user)):
    try:
        token = decrypt_token(current_user.github_token)
        print("Decrypted token:", token)  
        repos = get_user_repos(token)
        return {"repos": repos}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@router.post("/select_repo")
def select_repo(repo_name: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.repo_name = repo_name
    db.commit()
    return {"message": "Repo selected", "repo_name": repo_name}
