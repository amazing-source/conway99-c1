#!/bin/bash
# every 15 min: snapshot the live ledger and commit only the snapshot + status
cd "$(dirname "$0")"
while true; do
  sleep 900
  [ -f ledger.jsonl ] || continue
  cp ledger.jsonl ledger_snapshot.jsonl
  python3 s3cubes.py status > STATUS.txt 2>&1
  cd /home/user/conway99-c1 && git add code/asym243/s3grid/ledger_snapshot.jsonl code/asym243/s3grid/STATUS.txt && \
    git commit -q -m "S3 cubes checkpoint: $(head -1 code/asym243/s3grid/STATUS.txt)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DwoKi33od6QGceMH5o5GcR" && git push -q -u origin claude/v7-simultaneous
  cd /home/user/conway99-c1/code/asym243/s3grid
done
