#!/usr/bin/env bash
set -e

# run from the folder this script is in
cd "$(dirname "$0")"

# activate venv (common locations)
if [[ -f ./venv/bin/activate ]]; then
  source ./venv/bin/activate
elif [[ -f ./.venv/bin/activate ]]; then
  source ./.venv/bin/activate
elif [[ -f ./venv/Scripts/activate ]]; then
  source ./venv/Scripts/activate   # Git Bash on Windows
elif [[ -f ./.venv/Scripts/activate ]]; then
  source ./.venv/Scripts/activate  # Git Bash on Windows
else
  echo "No venv found (venv/ or .venv/). Skipping activation."
fi


# run inside the httpx repo
cd ../httpx

# outputs (back in Part3-Radon)
python -m radon cc -s -a ./httpx > ../Part3-Radon/radon_cc.txt 2>&1
python -m radon mi -s ./httpx > ../Part3-Radon/radon_mi.txt 2>&1
python -m radon raw -s ./httpx > ../Part3-Radon/radon_raw.txt 2>&1


echo "Wrote:"
echo "  ../Part3-Radon/radon_cc.txt"
echo "  ../Part3-Radon/radon_mi.txt"
echo "  ../Part3-Radon/radon_raw.txt"
