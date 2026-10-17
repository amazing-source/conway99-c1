#!/bin/bash
# runcls.sh IDX TL : full_s3.cnf + clsIDX.units -> kissat, result appended to classes_ledger.txt
cd "$(dirname "$0")"; i=$1; TL=${2:-1200}
f=cls$i.cnf; u=$(wc -l < cls$i.units)
read -r _ _ nv nc < <(head -1 full_s3.cnf)
{ echo "p cnf $nv $((nc + u))"; tail -n +2 full_s3.cnf; cat cls$i.units; } > $f
timeout $((TL + 60)) /tmp/solvers/kissat/build/kissat --time=$TL $f > cls$i.out 2>&1
r=$(grep "^s " cls$i.out | head -1); t=$(grep process-time cls$i.out | awk '{print $(NF-1)}')
echo "$(date -u +%FT%T) cls$i ${r:-s KILLED} ${t}s" >> classes_ledger.txt
rm -f $f
