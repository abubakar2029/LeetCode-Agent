import base64
import requests

def update_readme(stats_text):
    username = "abubakar2029"  # GitHub username of repo owner
    repo = "leetcode-data-structures-and-algorithms"  # Repository name
    token = "YOUR_PERSONAL_ACCESS_TOKEN"  # replace with your GitHub PAT

    url = f"https://api.github.com/repos/abubakar2029/leetcode-data-structures-and-algorithms/contents/README.md"
    headers = {"Authorization": f"token {token}"}

    # 1. Get current README
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    decoded = base64.b64decode(res["content"]).decode("utf-8")

    # 2. Replace content between markers
    start = "<!-- LEETCODE-AGENT:START -->"
    end = "<!-- LEETCODE-AGENT:END -->"

    if start in decoded and end in decoded:
        before = decoded.split(start)[0]
        after = decoded.split(end)[1]
        updated = before + start + "\n" + stats_text + "\n" + end + after
    else:
        # First time → append stats section
        updated = decoded + f"\n\n{start}\n{stats_text}\n{end}\n"

    # 3. Commit update
    data = {
        "message": "📊 Update LeetCode progress",
        "content": base64.b64encode(updated.encode()).decode(),
        "sha": sha
    }
    r = requests.put(url, headers=headers, json=data)
    return r.json()


if __name__ == "__main__":
    # Example stats text (replace with real LeetCode stats output)
    stats = "✅ Solved 10 problems\n🔥 Streak: 5 days\n🏆 Ranking: Top 20%"
    response = update_readme(stats)
    print(response)

