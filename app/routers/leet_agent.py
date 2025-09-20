from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from app.services.leet_agent_service import generate_email_suggestion

router = APIRouter(prefix="/leet-agent", tags=["LeetAgent"])

# Load reference repo once (can also be cached or stored in DB)
with open("75days_repo.json", "r") as f:
    reference_repo = json.load(f)

class RepoRequest(BaseModel):
    user_repo: dict

@router.post("/suggest-email")
def suggest_email(payload: RepoRequest):
    try:
        email = generate_email_suggestion(payload.user_repo, reference_repo)
        return {"email": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
