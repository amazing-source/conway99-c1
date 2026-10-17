#!/bin/bash
# Every 20 minutes: snapshot the live ledger (ignored by git) to ledger_snapshot.jsonl and commit/push it with its
# summary if they changed.  Only these two paths are committed, so the working tree stays clean between snapshots.
cd "$(dirname "$0")"; D=cubes_alpha99
while true; do
  cp $D/ledger.jsonl $D/ledger_snapshot.jsonl.tmp && mv $D/ledger_snapshot.jsonl.tmp $D/ledger_snapshot.jsonl
  python3 cuberunner.py $D status > $D/STATUS.txt 2>&1
  if ! git diff --quiet -- $D/ledger_snapshot.jsonl $D/STATUS.txt 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard -- $D/ledger_snapshot.jsonl)" ]; then
    git add -- $D/ledger_snapshot.jsonl $D/STATUS.txt && \
    git commit -q -m "alpha=22 cube ledger checkpoint: $(head -1 $D/STATUS.txt)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DwoKi33od6QGceMH5o5GcR" -- $D/ledger_snapshot.jsonl $D/STATUS.txt && \
    for k in 1 2 3 4; do git push -q -u origin claude/v7-simultaneous && break; sleep $((2 ** k)); done
    echo "$(date) checkpoint pushed"
  fi
  sleep 1200
done
