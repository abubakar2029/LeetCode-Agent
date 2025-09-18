import os, jwt
from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)) -> models.User:
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    print("user* :", user.__dict__)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
