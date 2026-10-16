#!/bin/bash
cd /c/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/stars_rank_2026-10-14
export PYTHONPATH="C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/pylib"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/c/home/researcher/AppData/Local/Programs/Python/Python312/python.exe hmatch_tools_2026-10-15/ksat_dir.py hmatch_tools_2026-10-16/nu13 hmatch_tools_2026-10-16/ksat_nu13.log 300 > hmatch_tools_2026-10-16/ksat_nu13_drv.out 2> hmatch_tools_2026-10-16/ksat_nu13_drv.err
