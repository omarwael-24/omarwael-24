import requests
from datetime import datetime

# === غيره باسم المستخدم بالضبط على LeetCode ===
USERNAME = "omarelmaru"

query = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
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
resp.raise_for_status()
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

# تحديث README
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
