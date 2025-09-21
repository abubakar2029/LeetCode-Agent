# DEPRECATED: Use services/recommendation_service.py instead

import requests
import json
import os
from dotenv import load_dotenv

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
        "model": "openai/gpt-5-chat-latest",
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
