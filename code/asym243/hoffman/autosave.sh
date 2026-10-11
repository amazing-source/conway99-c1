#!/bin/bash
# Every 20 minutes: commit and push the cube ledger (and its summary) if it changed.  Only these paths are committed.
cd "$(dirname "$0")"; D=cubes_alpha99
while true; do
  python3 cuberunner.py $D status > $D/STATUS.txt 2>&1
  if ! git diff --quiet -- $D/ledger.jsonl $D/STATUS.txt 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard -- $D/ledger.jsonl)" ]; then
    git add -- $D/ledger.jsonl $D/STATUS.txt && \
    git commit -q -m "alpha=22 cube ledger checkpoint: $(head -1 $D/STATUS.txt)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DwoKi33od6QGceMH5o5GcR" -- $D/ledger.jsonl $D/STATUS.txt && \
    for k in 1 2 3 4; do git push -q -u origin claude/v7-simultaneous && break; sleep $((2 ** k)); done
    echo "$(date) checkpoint pushed"
  fi
  sleep 1200
done
