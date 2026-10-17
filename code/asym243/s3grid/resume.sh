#!/bin/bash
# idempotent: restore the ledger from the committed snapshot if the container was lost, start workers + autosave
cd "$(dirname "$0")"; W=${1:-4}; TL=${2:-300}
[ -f ledger.jsonl ] || { [ -f ledger_snapshot.jsonl ] && cp ledger_snapshot.jsonl ledger.jsonl || python3 s3cubes.py init; }
mkdir -p logs
have=$(pgrep -fc "^python3 s3cubes.py work")
for i in $(seq $((have + 1)) $W); do setsid nohup python3 s3cubes.py work $TL >> logs/w$i.log 2>&1 < /dev/null & done
pgrep -f "^bash autosave.sh" >/dev/null || (setsid nohup bash autosave.sh >> logs/autosave.log 2>&1 < /dev/null &)
python3 s3cubes.py status
