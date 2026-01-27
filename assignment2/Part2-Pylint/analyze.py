import json
from collections import Counter

with open("pylint_out.json", encoding="utf-16") as f:
    issues = json.load(f)

# Total number of reported issues
total_issues = len(issues)

# Issues by category / severity
by_type = Counter(issue["type"] for issue in issues)

# Top 2 most frequent rule IDs
top_rules = Counter(issue["message-id"] for issue in issues).most_common(2)

print(f"Total issues: {total_issues}")
print("Issues by type:")
for k, v in by_type.items():
    print(f"  {k}: {v}")

print("Top 2 rule IDs:")
for rule, count in top_rules:
    print(f"  {rule}: {count}")