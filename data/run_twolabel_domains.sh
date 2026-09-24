#!/bin/bash
cd /c/home/researcher/Desktop/c1_recherche
for D in 23 234 2345 23456; do
  powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\RESEARCHER\.claude\tools\run_capped.ps1" -LimitMB 1800 -TimeoutSec 5400 -StatusSec 600 -WorkDir "C:\Users\RESEARCHER\Desktop\c1_recherche\code" -Log "C:\Users\RESEARCHER\Desktop\c1_recherche\data\twolabel_dom$D.runlog" -Exe "C:\Users\RESEARCHER\Desktop\c1_recherche\.venv\Scripts\python.exe" -ArgList "rooted_family.py sources 00,10 $D"
done
