import os, time, jwt

import urllib
import code
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.services.github_service import (
    get_github_login_url,
    exchange_code_for_token,
    get_user_email,
    get_user_info,
)
from app.services.db_service import create_or_update_user
from app.database import SessionLocal, get_db
from app import models
from app.utils.security import encrypt_token
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_SECONDS = 60 * 60 * 24 * 365  # 365 days
router = APIRouter(prefix="/auth", tags=["Auth"])

EXTENSION_REDIRECT=os.getenv("EXTENSION_REDIRECT")


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@router.get("/github")
def auth_github():
    return RedirectResponse(get_github_login_url())


@router.get("/callback")
def auth_callback(code: str, db: Session = Depends(get_db)):
    token_json = exchange_code_for_token(code)
    print("🔑 Token Response:", token_json)

    access_token = token_json.get("access_token")

    if not access_token:
        return HTMLResponse("<h1>Auth failed</h1>", status_code=400)

    # user ka token sa os ki info get kr lo
    user_info = get_user_info(access_token)
    username = user_info.get("login")
    avatar_url = user_info.get("avatar_url")
    email = get_user_email(access_token)

    # 🔐 Encrypt before saving
    encrypted_token = encrypt_token(access_token)
    
    # Save in DB
    try:
        user = create_or_update_user(db, username, email, avatar_url, encrypted_token)
        payload = {
        "sub": str(user.id),
        "username": username,
        "iat": int(time.time()),
        "exp": int(time.time()) + JWT_EXPIRES_SECONDS,
    }
        jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        redirect_uri = f"https://{EXTENSION_REDIRECT}.chromiumapp.org/provider_cb"
        final_url = (
            f"{redirect_uri}"
            f"?username={username}"
            f"&email={email}"
            f"&avatar_url={avatar_url}"
            f"&token={jwt_token}"
        )
        return RedirectResponse(final_url)

    except Exception as e:
        print("❌ DB save failed:", str(e))
        return HTMLResponse("<h1>Database error</h1>", status_code=500)



@router.get("/me")
def get_user(username: str, db: Session = Depends(get_db)):
    """Check if user is authenticated"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return JSONResponse({"authenticated": False}, status_code=401)

    return JSONResponse({
        "authenticated": True,
        "username": user.username,
        "email": user.email,
        "repo_name": user.repo_name
    })


