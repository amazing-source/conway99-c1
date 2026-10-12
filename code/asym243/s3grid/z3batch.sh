#!/bin/bash
# run random Z3-cover instances, decode SAT ones into edge lists; log to z3batch.log
cd "$(dirname "$0")"
for seed in "$@"; do
  python3 z3rand.py $seed 0 z3r_$seed.cnf > /dev/null
  timeout 900 /tmp/solvers/kissat/build/kissat --time=840 --seed=$seed z3r_$seed.cnf > z3r_$seed.out 2>&1
  r=$(grep "^s " z3r_$seed.out | head -1)
  if [ "$r" = "s SATISFIABLE" ]; then
    cp full_control.cnf.map z3r_$seed.cnf.map
    python3 decode_full.py z3r_$seed.cnf z3r_$seed.out graphs/z3r_$seed.edges > z3r_$seed.dec 2>&1
    echo "$(date -u +%T) seed $seed SAT $(tr '\n' ' ' < z3r_$seed.dec)" >> z3batch.log
  else
    echo "$(date -u +%T) seed $seed ${r:-KILLED}" >> z3batch.log
  fi
  rm -f z3r_$seed.cnf z3r_$seed.cnf.map
done
