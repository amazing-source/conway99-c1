#!/bin/bash
cd /c/home/researcher/Downloads/conway_c2_researcher2_start_2026_09_30/conway_c2_researcher2_start_2026_09_30/work/stars_rank_2026-10-14
while [ -n "$(powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { \$_.Name -eq 'python.exe' -and \$_.CommandLine -match 'hv2_c33' } | Select-Object -First 1 -ExpandProperty ProcessId")" ]; do sleep 30; done
bash "C:/home/researcher/AppData/Local/Temp/claude/C--Users-RESEARCHER-Downloads-conway-c2-researcher2-start-2026-09-30-conway-c2-researcher2-start-2026-09-30/cbac93e9-0e6a-4af7-8693-1962039bcf17/scratchpad/run_urep.sh" n1soft hmatch_tools_2026-10-15/near53/n_1.json 6 8802 0.1
