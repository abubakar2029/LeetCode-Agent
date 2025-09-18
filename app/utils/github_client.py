import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def run_query(query: str, variables: dict = None):
    if not GITHUB_TOKEN:
        raise Exception("GitHub token not found. Make sure it's in your .env file.")

    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(GITHUB_API_URL, json={"query": query, "variables": variables}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed: {response.status_code}, {response.text}")
