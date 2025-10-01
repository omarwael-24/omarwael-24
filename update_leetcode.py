import requests
import json
from datetime import datetime

# غير ده لاسم المستخدم بتاعك في LeetCode
USERNAME = "omarelmaru"

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
response = requests.post(url, json={"query": query, "variables": variables})

if response.status_code != 200:
    print("❌ Failed to fetch data:", response.text)
    exit(1)

data = response.json()
user = data["data"]["matchedUser"]

stats = user["submitStats"]["acSubmissionNum"]
easy = stats[1]["count"]
medium = stats[2]["count"]
hard = stats[3]["count"]
total = stats[0]["count"]

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# نكتب النتيجة في README.md
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

marker = "<!-- LEETCODE-STATS -->"
new_stats = f"""
**LeetCode Progress** 🏆  
- Total Solved: {total}  
- Easy: {easy}  
- Medium: {medium}  
- Hard: {hard}  

_Last updated on {timestamp}_  
"""

if marker in readme:
    before = readme.split(marker)[0]
    after = readme.split(marker)[1]
    readme = before + marker + "\n" + new_stats + "\n" + after
else:
    readme += f"\n{marker}\n{new_stats}\n"

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
