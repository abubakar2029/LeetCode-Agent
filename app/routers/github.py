import json
import re
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from requests import Session
from app import models
from app.services import repo_analyzer
from app.database import SessionLocal
from app.services.github_service import get_user_repos
from app.deps.auth_deps import get_current_user, get_db
from app.services.recommendation_service import query_aiml
from app.utils.security import decrypt_token
from app.utils.update_readme import update_readme_file


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


@router.post("/update_readme")
def update_readme(current_user: models.User = Depends(get_current_user)):
    raw_token = decrypt_token(current_user.github_token)
    user_repo_analysis = repo_analyzer.get_repo_tree(owner=current_user.username, repo=current_user.repo_name, token=raw_token, save=False)
    
    prompt = f"""
    Here are the LeetCode problems the user has solved:
    {json.dumps(user_repo_analysis, indent=2)}

    Task:
    - From this analysis tell me on which category how much problems the user has solved.
    - Respond STRICTLY in JSON format like:
      {{
        "Arrays": 10,
        "Strings": 5,
        "Dynamic Programming": 3,
        ...
      }}
    """
    
    ai_response = query_aiml(prompt)
    
    try:
        # If AI returns dict with "message" key
        if isinstance(ai_response, dict) and "message" in ai_response:
            ai_response = ai_response["message"]

        # Strip code fences if present
        match = re.search(r"\{[\s\S]*\}", ai_response)
        if not match:
            return {"error": "No JSON found in AI response"}, 400

        stats_dict = json.loads(match.group(0))

        update_readme_file(stats_dict, current_user.username, current_user.repo_name, raw_token)
        return {"message": "README updated successfully"}

    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response"}, 400


@router.post("/select_repo")
def select_repo(repo_name: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.repo_name = repo_name
    db.commit()
    return {"message": "Repo selected", "repo_name": repo_name}
