#!/bin/bash
# Case I exact search (16/10 night): harvest new h-invariant PSD nullity-14 objects in <h> from a warm start; their kernel
# classes are then enumerated completely (kernel_sat_enum.py) looking for a PSD member with broken star matchings.
cd /c/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/stars_rank_2026-10-14
export PYTHONPATH="C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/pylib"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export SAVE30=400 CPEN=0 SAVEPSD=0 NFREE=$3 MAXSEC=2400 INIT=$2
/c/home/researcher/AppData/Local/Programs/Python/Python312/python.exe sym4g.py "0,1;2,3" 100000000 $4 hmatch_tools_2026-10-16/harv2/hv3_$1 b1 anyc > hmatch_tools_2026-10-16/harv2/hv3_$1.log 2> hmatch_tools_2026-10-16/harv2/hv3_$1.err
