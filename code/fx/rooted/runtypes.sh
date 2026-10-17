#!/bin/bash
cd "$(dirname "$0")"
for t in "$@"; do
  python3 gen_rooted.py 7 $t.cnf $t.units > /dev/null
  timeout 560 /tmp/solvers/kissat/build/kissat --time=480 $t.cnf > $t.out 2>&1
  echo "$(date -u +%T) $t $(grep '^s ' $t.out | head -1) $(grep process-time $t.out | awk '{print $(NF-1)}')s" >> types.log
  rm -f $t.cnf
done
