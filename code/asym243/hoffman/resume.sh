#!/bin/bash
# Idempotent (re)start of the alpha = 22 cube search after any crash or container restart.
#   bash resume.sh [WORKERS] [TIMEOUT_SECONDS]
# Verdicts live in cubes_alpha99/ledger.jsonl (pushed by autosave.sh); nothing already decided is redone.
cd "$(dirname "$0")"
W=${1:-3}; T=${2:-1800}; D=cubes_alpha99
[ -f alpha99.cnf ] || python3 alpha_cnf.py 99 14 1 2 22 alpha99.cnf alpha99.units
# after a lost container: restore the live ledger from the last pushed snapshot
[ -f $D/ledger.jsonl ] || { [ -f $D/ledger_snapshot.jsonl ] && cp $D/ledger_snapshot.jsonl $D/ledger.jsonl; }
[ -f $D/ledger.jsonl ] || python3 cuberunner.py $D init
mkdir -p $D/logs
running=$(pgrep -fc "^python3 cuberunner.py $D work")
for i in $(seq $((running + 1)) $W); do
  nohup python3 cuberunner.py $D work $T >> $D/logs/worker_$i.out 2>&1 &
done
pgrep -f "^bash autosave.sh" >/dev/null || nohup bash autosave.sh >> $D/logs/autosave.out 2>&1 &
echo "workers: $(pgrep -fc "^python3 cuberunner.py $D work")"
