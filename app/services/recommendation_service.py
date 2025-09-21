import requests
import json
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.services.repo_analyzer import get_repo_tree
# Load environment variables
load_dotenv()

AIML_API_KEY = os.getenv("AIML_API_KEY")

def query_aiml(prompt: str) -> str:
    """Send prompt to AIML API and return response text."""
    url = "https://api.aimlapi.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]
    return f"❌ API Error: {r.text}"


def compare_repos(user_repo: dict, reference_repo: dict) -> list:
    """Find missing problems by comparing user and reference repo."""
    solved = set(user_repo.get("Solved", []))
    reference_solved = set(reference_repo.get("Solved", []))
    return list(reference_solved - solved)


def generate_email_suggestion(user_repo: dict, reference_repo: dict) -> str:
    """Generate short motivational email suggestion."""
    missing_problems = compare_repos(user_repo, reference_repo)

    prompt = f"""
    You are a coding mentor.

    Here is the reference "75 Days DSA Challenge" repo:
    {json.dumps(reference_repo, indent=2)}

    Here is the user's current repo analysis:
    {json.dumps(user_repo, indent=2)}

    Based on the comparison:
    - The user is missing these topics/problems: {missing_problems}

    Please write a SHORT motivational and professional email with:
    - Subject
    - Greeting (use 'Hi Developer')
    - Body (1 short paragraph with suggestions only 2 problem on what to solve next but it should be short from the 75-day repo)
    - Closing signed 'Your LeetAgent'
    """
    return query_aiml(prompt)

import json
from app.services.repo_analyzer import get_repo_tree
from app.utils.github_client import run_query
from app.utils.security import decrypt_token
from app import models


def compare_repos(user_repo: dict, reference_repo: dict) -> list:
    """Find missing problems by comparing user and reference repo."""
    solved = set(user_repo.get("Solved", []))
    reference_solved = set(reference_repo.get("Solved", []))
    return list(reference_solved - solved)


def generate_suggestion(user: models.User, db:Session) -> dict:
    """
    Generate today's problem suggestion for the given user.
    """
    # Decrypt token for private repo analysis
    raw_token = decrypt_token(user.github_token)

    # Analyze user repo
    user_repo = get_repo_tree(owner=user.username, repo=user.repo_name, token=raw_token, save=False)

    print("User repo analysis: ", user_repo)
    prompt = f"""
    You are a coding mentor for a competitive programmer.

    Here are the LeetCode problems the user has solved:
    {json.dumps(user_repo, indent=2)}

    Task:
    - Recommend a next problem to solve from the problems available on LeetCode that builds on the user's existing knowledge for today's challenge.
    - Respond STRICTLY in JSON format with these fields:
      {{
        "name": "<problem name>",
        "url": "<leetcode problem url>",
        "message": "<inspiring message for the problem (5-8 words)>",
        "context": "<short context like: You have solved arrays basics and stacks, now try this>"
      }}
    """

    response = query_aiml(prompt)

    try:
        suggestion = json.loads(response)
    except Exception:
        suggestion = {
            "name": "Error while generating suggestion",
            "message": response,
            "context": "Fallback response from AI."
        }

    # Save to DB
    user.today_problem = suggestion
    db.add(user)
    db.commit()
    db.refresh(user)

    return suggestion
