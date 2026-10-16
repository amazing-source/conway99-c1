#!/bin/bash
# U-repair from the obj53 near-misses (16/10 night): plateau {nu >= 14, T >= 0}, score lambda_min(U), heavy penalty when the
# star matchings become h-related (HREQ); a structure with nu >= 14, T, U >= 0 and broken matchings is saved as _HQ_k.json
cd /c/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/stars_rank_2026-10-14
export PYTHONPATH="C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/pylib"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export HREQ=50 NFREE=$3 MAXSEC=3000 INIT=$2 SOFTPLAT=${5:-}
/c/home/researcher/AppData/Local/Programs/Python/Python312/python.exe sym4g.py "4,4" 100000000 $4 hmatch_tools_2026-10-16/urep/u_$1 urep2 anyc > hmatch_tools_2026-10-16/urep/u_$1.log 2> hmatch_tools_2026-10-16/urep/u_$1.err
