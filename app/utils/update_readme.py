import base64
import requests


def dict_to_markdown_table(stats_dict, sort=True):
    # Sort by count (descending) if enabled
    items = sorted(stats_dict.items(), key=lambda x: x[1], reverse=True) if sort else stats_dict.items()

    # Create header
    table = "| 📊Topic | Problems Solved |\n"
    table += "|-------|----------------|\n"
    # Fill rows
    for topic, count in items:
        table += f"| {topic} | {count} |\n"
    return table


def update_readme_file(stats_dict,username,repo,token):

    url = f"https://api.github.com/repos/{username}/{repo}/contents/README.md"
    headers = {"Authorization": f"token {token}"}

    # 1. Get current README
    res = requests.get(url, headers=headers).json()
    sha = res["sha"]
    decoded = base64.b64decode(res["content"]).decode("utf-8")

    stats_text = dict_to_markdown_table(stats_dict)
    
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
