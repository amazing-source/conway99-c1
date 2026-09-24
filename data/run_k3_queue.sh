#!/bin/bash
# Sequential queue over the three-label twist patterns (data/k3_patterns.txt).
# One capped job at a time (1800 MB, 60 min); waits for free RAM > 3500 MB before each job.
# Results appended to data/k3_results.txt ("<spec> result: UNSAT (t s)" / SAT / UNKNOWN).
# Env: ONE=1 runs a single pattern; PATTERNS=file overrides the pattern list.
cd /c/home/researcher/Desktop/c1_recherche
PATTERNS="${PATTERNS:-data/k3_patterns.txt}"
touch data/k3_results.txt
n=0
tr -d '\r' < "$PATTERNS" > data/.k3_patterns_lf.txt
while read -r spec; do
  [ -z "$spec" ] && continue
  n=$((n+1))
  grep -qF "$spec " data/k3_results.txt && continue
  while true; do
    free=$(powershell -NoProfile -Command '[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)' | tr -d '\r')
    [ "$free" -ge 3500 ] && break
    sleep 60
  done
  tag=$(printf "k3_%03d" "$n")
  logw="C:/home/researcher/Desktop/c1_recherche/data/${tag}.runlog"
  powershell -NoProfile -ExecutionPolicy Bypass -File "C:/home/researcher/.claude/tools/run_capped.ps1" \
    -LimitMB 1800 -TimeoutSec 3600 -StatusSec 900 -WorkDir "C:/home/researcher/Desktop/c1_recherche/code" \
    -Log "$logw" -Exe "C:/home/researcher/Desktop/c1_recherche/.venv/Scripts/python.exe" \
    -ArgList "rooted_family.py spec $spec" > /dev/null 2>&1
  res=$(grep -o "result: [A-Z]* ([0-9.]*s)" "data/${tag}.runlog.out" 2>/dev/null)
  [ -z "$res" ] && res="result: UNKNOWN (timeout/killed/error)"
  echo "$spec $res" >> data/k3_results.txt
  [ -n "$ONE" ] && break
done < data/.k3_patterns_lf.txt
[ -z "$ONE" ] && echo "QUEUE DONE" >> data/k3_results.txt
