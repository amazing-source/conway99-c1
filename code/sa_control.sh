cd /c/home/researcher/Desktop/c1_recherche/code
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=../.venv/Scripts/python.exe
for p in "99 14 1 2" "81 20 1 6" "77 16 0 4" "100 22 0 6" "56 10 0 2" "50 7 0 1" "243 22 1 2"; do
  $PY -W ignore sa_srg.py $p 480 1
done
