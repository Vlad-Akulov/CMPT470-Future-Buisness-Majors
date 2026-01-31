#!/usr/bin/env bash

# Absolute path to this script (resolves symlinks)
SCRIPT_PATH="$(readlink -f "$0")"

# Parent directory of the script
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"

# cd into it
cd "$SCRIPT_DIR" || exit 1

# load semgrep into path 
source ./venv/bin/activate


# run semgrep on the httpx directory to analyse only the code 
cd ../httpx/
rm ../Part1-Semgrep/semgrep.json
time semgrep --config auto ./httpx/ \
  --json \
  --output ../Part1-Semgrep/semgrep.json \
  --no-git-ignore \
  > ../Part1-Semgrep/semgrep_run.txt 2>&1



# pretty format for inspection
if command -v jq >/dev/null 2>&1; then
  jq . ../Part1-Semgrep/semgrep.json > ../Part1-Semgrep/semgrep_pretty.json
else
  echo "jq not found — skipping pretty JSON formatting."
  echo "Install with: sudo apt install jq"
fi