import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback"



def get_github_login_url():
    print("======================")
    """Return GitHub OAuth login URL"""
    return (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=public_repo,user:email"
    )


def exchange_code_for_token(code: str):
    """Exchange authorization code for GitHub token"""
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(token_url, headers=headers, data=data)
    return response.json()


def get_user_info(token: str):
    """Fetch user info using access token"""
    response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()

def get_user_email(token: str):
    """Fetch user email using access token"""
    response = requests.get(
        "https://api.github.com/user/emails",
        headers={"Authorization": f"Bearer {token}"},
    )
    emails = response.json()
    # Find primary, verified email
    primary_email = next((e["email"] for e in emails if e.get("primary") and e.get("verified")), None)
    return primary_email

def get_user_repos(token: str):
    """Fetch user repos using GitHub API"""
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch repos")
    repos = response.json()
    return [r["name"] for r in repos]  