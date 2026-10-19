#!/bin/bash
# rank-37 per-line obligations on random G_T (one process at a time, <= 200 s per run)
S="$1"; OUT="$2"
PY=/c/home/researcher/conway99-env/.venv/Scripts/python.exe
run() { # gt seed rho delta
  f="$S/b_$(echo $1 | tr ':,' '__')_s$2_r$3_d$4.bin"
  meta=$(timeout 280 $PY oblr_prep.py $1 $2 0 $3 $4 "$f" | sed 's/, "s01.*/}/')
  res=$(timeout 230 ./oblr.exe "$f" 200)
  echo "{\"meta\": $meta, \"res\": $res}" >> "$OUT"
  rm -f "$f"
}
for sd in 2 3 4 5; do run c1 $sd 0 1; done
for sd in 2 3; do for bl in blocks:3,3 blocks:2,4 blocks:1,5; do for dl in 1 3; do run $bl $sd 1 $dl; done; done; done
for sd in 3 4; do for dl in 1 3; do run c1t $sd 1 $dl; done; done
echo DONE >> "$OUT"
