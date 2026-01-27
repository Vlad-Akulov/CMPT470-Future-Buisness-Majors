import json
from collections import Counter
import os

with open("pylint_out.json", encoding="utf-16") as f:
    issues = json.load(f)

# Total number of reported issues
total_issues = len(issues)

# Issues by category / severity
by_type = Counter(issue["type"] for issue in issues)

# Top 2 most frequent rule IDs
top_rules = Counter(issue["message-id"] for issue in issues).most_common(2)

# Count issues by file path (extract just the filename from full path)
by_path = Counter(os.path.basename(issue["path"]) for issue in issues)

# Count by warning type (symbol/message-id)
by_warning = Counter(issue["symbol"] for issue in issues)

print(f"Total issues: {total_issues}")
print("\nIssues by type:")
for k, v in by_type.items():
    print(f"  {k}: {v}")

print("\nTop 2 rule IDs:")
for rule, count in top_rules:
    print(f"  {rule}: {count}")

print("\nIssues by file path:")
for path, count in sorted(by_path.items(), key=lambda x: x[1], reverse=True):
    print(f"  {path}: {count}")

print("\nIssues by warning type:")
for warning, count in sorted(by_warning.items(), key=lambda x: x[1], reverse=True):
    print(f"  {warning}: {count}")