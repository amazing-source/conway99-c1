#!/bin/bash
# usage: z3sample.sh SEED0 SEED1 NUDGES
for s in $(seq $1 $2); do
  python3 z3cnf.py z3_$s.cnf $s $3 > /dev/null
  timeout 400 /tmp/solvers/kissat/build/kissat -q z3_$s.cnf > z3_$s.out; rc=$?
  if [ $rc -eq 10 ]; then echo "seed $s nudges $3: $(python3 z3decode.py z3_$s.cnf z3_$s.out z3s)";
  else echo "seed $s nudges $3: kissat rc=$rc"; fi
  rm -f z3_$s.cnf z3_$s.cnf.map z3_$s.out
done
