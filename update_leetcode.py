import requests
from datetime import datetime

USERNAME = "omarelmaru"  # غيره باسمك بالظبط على LeetCode

query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    username
    submitStats: submitStatsGlobal {
      acSubmissionNum {
        difficulty
        count
        submissions
      }
    }
  }
}
"""
variables = {"username": USERNAME}
url = "https://leetcode.com/graphql"
resp = requests.post(url, json={"query": query, "variables": variables})

if resp.status_code != 200:
    raise Exception(f"Failed: {resp.text}")

data = resp.json()["data"]["matchedUser"]["submitStats"]["acSubmissionNum"]
easy = data[1]["count"]
medium = data[2]["count"]
hard = data[3]["count"]
total = data[0]["count"]

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
stats_md = f"""
**LeetCode Progress** 🏆  
- Total Solved: {total}  
- Easy: {easy}  
- Medium: {medium}  
- Hard: {hard}  

_Last updated on {timestamp}_
"""

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

marker = "<!-- LEETCODE-STATS -->"
if marker in content:
    before, after = content.split(marker)
    content = before + marker + "\n" + stats_md + "\n" + after
else:
    content += f"\n{marker}\n{stats_md}\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)
