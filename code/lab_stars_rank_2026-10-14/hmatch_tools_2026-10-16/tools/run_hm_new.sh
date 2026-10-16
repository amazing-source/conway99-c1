#!/bin/bash
# H-MATCH counterexample search, 16/10 night: new symmetry families (true g = h p with small k, and fake two-transposition
# groups), cold starts, b1 objective with HBREAK + HMATCH (score -60 when the star matchings are h-related), 1 h each.
cd /c/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/stars_rank_2026-10-14
export PYTHONPATH="C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/pylib"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/c/home/researcher/AppData/Local/Programs/Python/Python312/python.exe
O=hmatch_tools_2026-10-16/hm_new
k=$1; g="$2"; fake=$3; seed=$((9100 + k))
if [ "$fake" = 1 ]; then export FAKEOK=1; fi
export HBREAK=1 HMATCH=1 CPEN=0 SAVEPSD=0 NFREE=5 MAXSEC=3600 HBSAVEMIN=12
$PY sym4g.py "$g" 100000000 $seed $O/f$k b1 anyc > $O/f$k.log 2> $O/f$k.err
