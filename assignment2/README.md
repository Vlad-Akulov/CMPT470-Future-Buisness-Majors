# Repo to analyse here

https://github.com/encode/httpx

### clone into assignemnt 2 directory
```sh
git clone https://github.com/encode/httpx
```
# Semgrep

### Download semgrep (if it tells you you have an externaly managed environemnt either make a venv or use pipx)
```sh
python3 -m pip install semgrep
```
### run semgrep on httpx by runing the scipt
```sh
run_Semgrep.sh
```

# Radon
### Download Radon
```sh
python3 -m pip install radon
python3 -m radon --version
```
Should display `6.0.1`+

### Running Radon analysis
```sh
cd Part3-Radon
./run_Radon.sh
```
Results should output to `radon_cc.txt` and `radon_mi.txt`.





