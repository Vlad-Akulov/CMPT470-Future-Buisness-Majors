#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGEC_SRC="${SCRIPT_DIR}/agec2/src"

JAR_PATH=""
ASM_DIR=""
OUT_DIR=""
PYTHON_BIN="${PYTHON_BIN:-python}"
DISASM_TIMEOUT_SEC="${DISASM_TIMEOUT_SEC:-30}"

log() {
  printf "[%s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

usage() {
  cat <<'EOF'
Usage:
  run_table1_metrics.sh --jar /path/to/argouml-0.28.1.jar [--out-dir DIR] [--python python2]
  run_table1_metrics.sh --asm-dir /path/to/disasm_argouml_0281 [--out-dir DIR] [--python python2]

Description:
  Runs AGEC and collects the Table I metrics used in the paper:
  - Classes having method definitions
  - Method definitions
  - Locations where n-grams were generated
  - Distinct n-grams
  - n-grams of code clones

Notes:
  - Use Python 2.7 for AGEC.
  - If --jar is provided, this script will disassemble class-by-class with timeout.
  - Set DISASM_TIMEOUT_SEC to adjust per-class timeout (default: 30).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --jar)
      JAR_PATH="${2:-}"
      shift 2
      ;;
    --asm-dir)
      ASM_DIR="${2:-}"
      shift 2
      ;;
    --out-dir)
      OUT_DIR="${2:-}"
      shift 2
      ;;
    --python)
      PYTHON_BIN="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "${AGEC_SRC}" ]]; then
  echo "error: cannot find agec2 source directory: ${AGEC_SRC}" >&2
  exit 1
fi

to_abs_path() {
  local p="$1"
  if [[ "${p}" = /* ]]; then
    printf "%s\n" "${p}"
  else
    printf "%s\n" "$(cd "$(dirname "${p}")" && pwd)/$(basename "${p}")"
  fi
}

pick_timeout_cmd() {
  if command -v timeout >/dev/null 2>&1; then
    printf "%s\n" "timeout"
    return 0
  fi
  if command -v gtimeout >/dev/null 2>&1; then
    printf "%s\n" "gtimeout"
    return 0
  fi
  return 1
}

pick_python2() {
  local py="$1"
  if "${py}" -c 'import sys; raise SystemExit(0 if sys.version_info[0] == 2 else 1)' >/dev/null 2>&1; then
    printf "%s\n" "${py}"
    return 0
  fi
  if command -v python2 >/dev/null 2>&1; then
    printf "%s\n" "python2"
    return 0
  fi
  if command -v pyenv >/dev/null 2>&1; then
    local pyenv_py
    pyenv_py="$(pyenv which python 2>/dev/null || true)"
    if [[ -n "${pyenv_py}" ]] && "${pyenv_py}" -c 'import sys; raise SystemExit(0 if sys.version_info[0] == 2 else 1)' >/dev/null 2>&1; then
      printf "%s\n" "${pyenv_py}"
      return 0
    fi
  fi
  return 1
}

if ! PYTHON_BIN="$(pick_python2 "${PYTHON_BIN}")"; then
  echo "error: could not find a Python 2 interpreter. set --python or PYTHON_BIN to python2.7" >&2
  exit 1
fi
log "using python interpreter: ${PYTHON_BIN}"

if [[ -z "${OUT_DIR}" ]]; then
  TS="$(date +%Y%m%d_%H%M%S)"
  OUT_DIR="${SCRIPT_DIR}/results/table1_${TS}"
fi
OUT_DIR="$(to_abs_path "${OUT_DIR}")"
mkdir -p "${OUT_DIR}"
log "output directory: ${OUT_DIR}"

if [[ -z "${JAR_PATH}" && -z "${ASM_DIR}" ]]; then
  if [[ -d "${AGEC_SRC}/disasm_argouml_0281" ]]; then
    ASM_DIR="${AGEC_SRC}/disasm_argouml_0281"
  elif [[ -f "${SCRIPT_DIR}/argouml-0.28.1.jar" ]]; then
    JAR_PATH="${SCRIPT_DIR}/argouml-0.28.1.jar"
  else
    echo "error: no input provided. pass --jar or --asm-dir (or place disasm at agec2/src/disasm_argouml_0281)" >&2
    usage
    exit 1
  fi
fi

if [[ -n "${ASM_DIR}" ]]; then
  ASM_DIR="$(to_abs_path "${ASM_DIR}")"
  if [[ ! -d "${ASM_DIR}" ]]; then
    echo "error: asm directory does not exist: ${ASM_DIR}" >&2
    exit 1
  fi
else
  JAR_PATH="$(to_abs_path "${JAR_PATH}")"
  if [[ ! -f "${JAR_PATH}" ]]; then
    echo "error: jar file does not exist: ${JAR_PATH}" >&2
    exit 1
  fi
  ASM_DIR="${OUT_DIR}/disasm_argouml_0281"
fi

NGRAMS_FILE="${OUT_DIR}/ngrams_argouml_0281.txt"
DIAG_FILE="${OUT_DIR}/diag_argouml_0281.txt"
CLONE_MD_FILE="${OUT_DIR}/clone-indices-md_argouml_0281.txt"
METRICS_TSV="${OUT_DIR}/table1_metrics.tsv"
METRICS_MD="${OUT_DIR}/table1_metrics.md"
DISASM_FAILURES_FILE="${OUT_DIR}/disasm_failures.txt"

cd "${AGEC_SRC}"
log "working directory: ${AGEC_SRC}"

if [[ -n "${JAR_PATH}" ]]; then
  TIMEOUT_CMD="$(pick_timeout_cmd || true)"
  JAR_EXPAND_DIR="${JAR_PATH}.files"
  CLASS_LIST_FILE="${JAR_EXPAND_DIR}/class_list"

  if [[ ! -d "${JAR_EXPAND_DIR}" ]]; then
    mkdir -p "${JAR_EXPAND_DIR}"
    unzip -q "${JAR_PATH}" -d "${JAR_EXPAND_DIR}"
  fi

  if [[ ! -f "${CLASS_LIST_FILE}" ]]; then
    (
      cd "${JAR_EXPAND_DIR}"
      find . -type f -name "*.class" | sed 's#^\./##; s#\.class$##' | sort > class_list
    )
  fi

  mkdir -p "${ASM_DIR}"
  : > "${DISASM_FAILURES_FILE}"
  total_classes="$(wc -l < "${CLASS_LIST_FILE}" | tr -d '[:space:]')"
  done_classes="$(find "${ASM_DIR}" -type f -name "*.asm" | wc -l | tr -d '[:space:]')"
  if [[ "${done_classes}" -ge "${total_classes}" && "${total_classes}" -gt 0 ]]; then
    log "disasm already complete: ${done_classes}/${total_classes}, skipping"
  else
    log "disasm start: ${done_classes}/${total_classes} already present"

    i=0
    while IFS= read -r cn; do
      i=$((i + 1))
      out="${ASM_DIR}/${cn}.asm"
      if [[ -f "${out}" ]]; then
        continue
      fi
      mkdir -p "$(dirname "${out}")"
      cn_dot="${cn//\//.}"
      if [[ -n "${TIMEOUT_CMD}" ]]; then
        if ! "${TIMEOUT_CMD}" "${DISASM_TIMEOUT_SEC}s" /usr/bin/javap -classpath "${JAR_EXPAND_DIR}" -c -p -l -constants "${cn_dot}" > "${out}" 2>/dev/null; then
          rm -f "${out}"
          printf "%s\n" "${cn}" >> "${DISASM_FAILURES_FILE}"
        fi
      else
        if ! /usr/bin/javap -classpath "${JAR_EXPAND_DIR}" -c -p -l -constants "${cn_dot}" > "${out}" 2>/dev/null; then
          rm -f "${out}"
          printf "%s\n" "${cn}" >> "${DISASM_FAILURES_FILE}"
        fi
      fi
      if (( i % 100 == 0 )); then
        done_now="$(find "${ASM_DIR}" -type f -name "*.asm" | wc -l | tr -d '[:space:]')"
        log "disasm progress: ${done_now}/${total_classes}"
      fi
    done < "${CLASS_LIST_FILE}"
  fi

  done_classes="$(find "${ASM_DIR}" -type f -name "*.asm" | wc -l | tr -d '[:space:]')"
  failed_classes="$(wc -l < "${DISASM_FAILURES_FILE}" | tr -d '[:space:]')"
  log "disasm complete: ${done_classes}/${total_classes}, failed=${failed_classes}"
fi

log "step start: gen_ngram"
"${PYTHON_BIN}" gen_ngram.py -v -a "${ASM_DIR}" > "${NGRAMS_FILE}"
log "step done: gen_ngram -> ${NGRAMS_FILE}"

log "step start: det_clone"
"${PYTHON_BIN}" det_clone.py "${NGRAMS_FILE}" > "${CLONE_MD_FILE}"
log "step done: det_clone -> ${CLONE_MD_FILE}"

log "step start: gen_ngram --mode-diagnostic"
"${PYTHON_BIN}" gen_ngram.py -v -a "${ASM_DIR}" --mode-diagnostic > "${DIAG_FILE}"
log "step done: diagnostic -> ${DIAG_FILE}"

classes="$(awk -F': ' '/^classes:/{print $2; exit}' "${DIAG_FILE}")"
method_defs="$(awk -F': ' '/^method bodies:/{print $2; exit}' "${DIAG_FILE}")"
locations="$(awk 'BEGIN{blk=0;c=0} /^#/{next} NF==0{if(blk){c++;blk=0};next} {blk=1} END{if(blk)c++; print c}' "${NGRAMS_FILE}")"
distinct_ngrams="$(awk 'BEGIN{s=""} /^#/{next} NF==0{if(s!=""){print s;s=""};next} {split($0,a,"\t"); s=s (s==""?"":"\t") a[1]} END{if(s!="")print s}' "${NGRAMS_FILE}" | sort -u | wc -l | tr -d '[:space:]')"
clone_ngrams="$(rg -c '^ope:$' "${CLONE_MD_FILE}" 2>/dev/null || grep -c '^ope:$' "${CLONE_MD_FILE}" || true)"

cat > "${METRICS_TSV}" <<EOF
metric	paper_value	my_run
Classes having method definitions	1700	${classes}
Method definitions	8888	${method_defs}
Locations where n-grams were generated	1232292	${locations}
Distinct n-grams	282753	${distinct_ngrams}
n-grams of code clones	4634	${clone_ngrams}
EOF

cat > "${METRICS_MD}" <<EOF
| Metric | Paper Value | My Run |
|---|---:|---:|
| Classes having method definitions | 1,700 | ${classes} |
| Method definitions | 8,888 | ${method_defs} |
| Locations where n-grams were generated | 1,232,292 | ${locations} |
| Distinct n-grams | 282,753 | ${distinct_ngrams} |
| n-grams of code clones | 4,634 | ${clone_ngrams} |
EOF

log "step done: metrics extraction"
printf "\nTable I metrics (paper vs run)\n"
cat "${METRICS_MD}"
printf "\nSaved files:\n"
printf "  %s\n" "${METRICS_TSV}" "${METRICS_MD}" "${DIAG_FILE}" "${NGRAMS_FILE}" "${CLONE_MD_FILE}"
if [[ -f "${DISASM_FAILURES_FILE}" ]]; then
  printf "  %s\n" "${DISASM_FAILURES_FILE}"
fi
