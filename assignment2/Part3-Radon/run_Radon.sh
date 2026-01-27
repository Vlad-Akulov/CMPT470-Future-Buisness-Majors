#!/usr/bin/env bash
set -e

# run from the folder this script is in
cd "$(dirname "$0")"

# run inside the httpx repo
cd ../httpx

# outputs (back in Part3-Radon)
# CC: --average complexity 
time {
    python3 -m radon cc -s -a ./httpx > ../Part3-Radon/radon_cc.txt 2>&1
    python3 -m radon mi -s ./httpx > ../Part3-Radon/radon_mi.txt 2>&1
    python3 -m radon raw -s ./httpx > ../Part3-Radon/radon_raw.txt 2>&1
    python3 -m radon hal ./httpx > ../Part3-Radon/radon_hal.txt 2>&1
}


echo "Wrote:"
echo "  ../Part3-Radon/radon_cc.txt"
echo "  ../Part3-Radon/radon_mi.txt"
echo "  ../Part3-Radon/radon_raw.txt"
