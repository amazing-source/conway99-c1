#!/bin/bash
# sequential SDP runs (one heavy job at a time); each line: env + args
cd /c/home/researcher/Desktop/c1_recherche/code
PY=../.venv/Scripts/python.exe
echo "=== BvLS control, degree 3, E-5 kernel"; SRG_N=243 SRG_K=22 SRG_TAG=_bvls $PY -W ignore euclid_sdp3.py 3 BvLS-E-5
echo "=== 99, degree 3, E3 kernel"; $PY -W ignore euclid_sdp3.py 3 E3
echo "=== 99, degree 3, E-4 and E3 kernels"; $PY -W ignore euclid_sdp3.py 3 E-4,E3
echo "=== 99, degree 2, E-4"; $PY -W ignore euclid_sdp3.py 2 E-4
echo "=== 99, degree 2, E-4 and E3"; $PY -W ignore euclid_sdp3.py 2 E-4,E3
