from sqlalchemy.orm import Session
from app import models

def create_or_update_user(db: Session, username: str, email: str, avatar_url: str, token: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.email = email
        user.avatar_url = avatar_url
        user.github_token = token
    else:
        user = models.User(
            username=username,
            email=email,
            avatar_url=avatar_url,
            github_token=token
        )
        db.add(user)
    db.commit()
    db.refresh(user)
    return user

def set_user_repo(db: Session, username: str, repo_name: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        user.repo_name = repo_name
        db.commit()
        db.refresh(user)
    return user
