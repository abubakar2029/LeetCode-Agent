# DEPRECATED: The Coral integration has been removed from the main application.
from coral_mcp import MCPServer
import requests

server = MCPServer("leetcode-agent")

@server.tool()
def analyze_repo(repo_url: str):
    resp = requests.post(
        "https://leetcode-agent-production.up.railway.app/analyze_repo",
        json={"repo_url": repo_url}
    )
    return resp.json()

@server.tool()
def recommend_problem():
    resp = requests.get("https://leetcode-agent-production.up.railway.app/recommend_problem")
    return resp.json()

@server.tool()
def push_to_github(problem_name: str, solution_code: str):
    resp = requests.post(
        "https://leetcode-agent-production.up.railway.app/push_to_github",
        json={"problem_name": problem_name, "solution_code": solution_code}
    )
    return resp.json()

if __name__ == "__main__":
    server.run("0.0.0.0", 5555)   # important: run on Railway port
