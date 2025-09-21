from sqlalchemy import Column, Integer, String, JSON
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    repo_name = Column(String, nullable=True)
    github_token = Column(String, nullable=False)  
    today_problem = Column(JSON, nullable=True)