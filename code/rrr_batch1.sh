cd /c/home/researcher/Desktop/c1_recherche/code
PY=../.venv/Scripts/python.exe
for b in 0.02 0.1 0.2; do echo "== Gewirtz beta $b"; $PY rrr_srg.py 56 10 0 2 200000 2 $b; done
for b in 0.05 0.1; do echo "== srg(81,20,1,6) beta $b"; $PY rrr_srg.py 81 20 1 6 100000 2 $b; done
