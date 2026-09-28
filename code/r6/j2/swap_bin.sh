#!/bin/bash
# when orbit 3 ends, restart the resumable run with cut25_next.exe (validated identical trees, faster)
cd /c/home/researcher/Desktop/c1_recherche/code/r6/j2
until grep -q "orbit 3 end" run_r5.log; do sleep 15; done
sleep 5
powershell -NoProfile -Command "\$p='run_'+'r5'+'.sh'; Get-CimInstance Win32_Process | Where-Object { \$_.CommandLine -and \$_.CommandLine.Contains(\$p) } | ForEach-Object { Stop-Process -Id \$_.ProcessId -Force }; Get-Process cut25 -ErrorAction SilentlyContinue | Stop-Process -Force"
sleep 3
cp cut25_next.exe cut25.exe && cp cut25g.c cut25.c
echo "--- restart with cut25g $(date '+%H:%M:%S')" >> run_r5.log
nohup ./run_r5.sh 12 > /dev/null 2>&1 &
sleep 10
powershell -NoProfile -Command "Get-Process cut25 | ForEach-Object { \$_.PriorityClass = 'BelowNormal' }"
