#!/bin/bash
# Full R5 run, resumable: items already in R5_surv_<o>.txt.kills (matched on qi pi mask) are skipped.
cd /c/home/researcher/Desktop/c1_recherche/code/r6/j2
NT=${1:-12}
export NO_SIDEBOUND=1
for o in 3 2 0 1; do
  A=$(python -c "import json; print(' '.join(map(str,json.load(open('R5_orbits.json'))[$o]['a'])))")
  touch R5_surv_$o.txt.kills
  python -c "
done=set(tuple(l.split()[1:4]) for l in open('R5_surv_$o.txt.kills') if len(l.split())>=8)
rem=[l for l in open('R5_list_$o.txt') if tuple(l.split()) not in done]
open('R5_rem_$o.txt','w').writelines(rem); print(len(rem))" > R5_rem_$o.count
  if [ "$(cat R5_rem_$o.count)" = "0" ]; then echo "orbit $o already complete" >> run_r5.log; continue; fi
  echo "orbit $o start $(date '+%H:%M:%S') remaining $(cat R5_rem_$o.count)" >> run_r5.log
  ./cut25.exe $A R5_sym_$o.txt 0 run R5_rem_$o.txt R5_surv_$o.txt $NT >> run_r5.log 2> run_r5_$o.err
  echo "orbit $o end $(date '+%H:%M:%S')" >> run_r5.log
done
echo "ALL DONE $(date '+%H:%M:%S')" >> run_r5.log
