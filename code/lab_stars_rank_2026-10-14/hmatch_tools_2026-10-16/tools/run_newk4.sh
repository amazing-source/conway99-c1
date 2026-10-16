#!/bin/bash
cd /c/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/stars_rank_2026-10-14
while [ -n "$(powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'python.exe' -and \$_.CommandLine -match 'hv3_' } | Select-Object -First 1 -ExpandProperty ProcessId")" ]; do sleep 30; done
export PYTHONPATH="C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/pylib"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/c/home/researcher/AppData/Local/Programs/Python/Python312/python.exe
$PY hmatch_tools_2026-10-15/new_kernel_classes.py hmatch_tools_2026-10-16/newk4 "hmatch_tools_2026-10-16/harv2/*_H30_*.json" rank30_psd_objects_2026-10-15.json rank30_new_objects.json hmatch_tools_2026-10-15/newk1/*.json hmatch_tools_2026-10-15/newk2/*.json hmatch_tools_2026-10-16/newk3/*.json > hmatch_tools_2026-10-16/newk4.log 2>&1
$PY hmatch_tools_2026-10-15/ksat_dir.py hmatch_tools_2026-10-16/newk4 hmatch_tools_2026-10-16/ksat_newk4.log 300 > hmatch_tools_2026-10-16/ksat_newk4_drv.out 2> hmatch_tools_2026-10-16/ksat_newk4_drv.err
