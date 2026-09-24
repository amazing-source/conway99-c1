cd /c/home/researcher/Desktop/c1_recherche/code
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=../.venv/Scripts/python.exe
echo "== generic RRR, beta 0.02, 20 min"; $PY -W ignore rrr_campaign.py control81 1200
echo "== lines RRR, beta 0.02, 20 min"; $PY -W ignore rrr_lines.py 81 20 6 1200 1 0.02
echo "== lines RRR, beta 0.05, 20 min"; $PY -W ignore rrr_lines.py 81 20 6 1200 1 0.05
