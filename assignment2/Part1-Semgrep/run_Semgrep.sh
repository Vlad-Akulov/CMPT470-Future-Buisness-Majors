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
rm ../Part1-Semgrep/semgrep.txt
time semgrep --config auto ./httpx/ >> ../Part1-Semgrep/semgrep.txt 2>&1


