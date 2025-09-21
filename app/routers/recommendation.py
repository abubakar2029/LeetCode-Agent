from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json

from app.database import get_db
from app import models
from app.services.leet_agent_service import generate_email_suggestion
from app.utils.user import get_current_user  # <-- helper to decode JWT + fetch user
from app.services.recommendation_service import generate_suggestion


router = APIRouter(prefix="/problem", tags=["Recommendation"])


class RepoRequest(BaseModel):
    user_repo: dict


@router.get("/today")
def today_problem(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Return today's problem for the authenticated user.
    If none is assigned yet, pick one, store it in DB, and return it.
    """
    
    try:
        if user.today_problem:
            return {
                "today_problem": user.today_problem,
            }

        # Example: pick from reference repo
        # Later this can use your recommendation logic
        problem = {
            "name": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum/",
            "message": "Great starter problem for arrays and hashing."
        }


        return {
            "today_problem": generate_suggestion(user,db),
        }

    except Exception as e:
        print("Error in today_problem: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/suggest-email")
def suggest_email(payload: RepoRequest):
    try:
        email = generate_email_suggestion(payload.user_repo, reference_repo)
        return {"email": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
