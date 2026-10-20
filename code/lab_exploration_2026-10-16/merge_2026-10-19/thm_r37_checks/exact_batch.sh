#!/bin/bash
# exact-only star tests (no unary real filter in prep, STAR_NOREAL=1 in the engine), one process at a time
M="C:/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/exploration_2026-10-16/merge_2026-10-19"
R="C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/boost/runs/thm_r37"
PY=C:/home/researcher/conway99-env/.venv/Scripts/python.exe
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
run() { # spec seed delta extra...
  spec=$1; seed=$2; delta=$3; shift 3
  for x in 0 1 2 3 4 5; do
    out=$($PY "$R/prep_nounary.py" $spec $seed 0 $x 37 $delta "$R/eb.bin" "$@" 2>&1)
    if echo "$out" | grep -q transversal; then continue; fi
    if echo "$out" | grep -q "possible directions"; then
      nk=$(echo "$out" | sed -n 's/.*: \([0-9]*\) possible directions.*/\1/p')
      for k in $(seq 0 $((nk-1))); do
        info=$($PY "$R/prep_nounary.py" $spec $seed 0 $x 37 $delta "$R/eb.bin" "$@" --kappa $k 2>&1 | tail -1)
        c=$(echo "$info" | sed -n 's/.*"c": \([0-9]*\).*/\1/p')
        if [ "$c" -ge 2 ]; then NR=1; else NR=; fi
        res=$(STAR_NOREAL=1 STAR_NORANK=$NR timeout 250 "$M/star39.exe" "$R/eb.bin" 200 | sed -n 's/.*"status": "\([A-Z]*\)".*"nodes": \([0-9]*\),.*"leaves": \([0-9]*\).*/\1 nodes=\2 leaves=\3/p')
        echo "$spec s$seed x$x delta=$delta $* kappa=$k : $res"
      done
      return
    fi
    c=$(echo "$out" | tail -1 | sed -n 's/.*"c": \([0-9]*\).*/\1/p')
    if [ "$c" -ge 2 ]; then NR=1; else NR=; fi
    if [ -n "$NR" ]; then res=$(STAR_NOREAL=1 STAR_NORANK=1 timeout 250 "$M/star39.exe" "$R/eb.bin" 200); else res=$(STAR_NOREAL=1 timeout 250 "$M/star39.exe" "$R/eb.bin" 200); fi
    res=$(echo "$res" | sed -n 's/.*"status": "\([A-Z]*\)".*"nodes": \([0-9]*\),.*"leaves": \([0-9]*\).*/\1 nodes=\2 leaves=\3/p')
    echo "$spec s$seed x$x delta=$delta $* : $res"
    return
  done
}
run c1t 1 1
run c1t 1 3
run blockst:3,3 1 1
run blockst:3,3 1 3
run blockst:3,3 1 0 --unbal
run c1tt 1 1
run c1tt 1 3
run c1tt 1 0 --unbal
rm -f "$R/eb.bin"
