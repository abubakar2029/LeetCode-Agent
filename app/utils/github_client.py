import requests
import os
from dotenv import load_dotenv
from app.utils.security import decrypt_token  # for user tokens

# Load environment variables
load_dotenv()

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # fallback token for public repos


def run_query(query: str, variables: dict = None, token: str = None):
    """
    Run a GitHub GraphQL query.
    - If token is provided (user token), it will be used.
    - Else falls back to GITHUB_TOKEN from .env.
    """
    auth_token = token or GITHUB_TOKEN
    if not auth_token:
        raise Exception("❌ No GitHub token available")

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(
        GITHUB_API_URL,
        json={"query": query, "variables": variables},
        headers=headers,
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"❌ Query failed: {response.status_code}, {response.text}")
