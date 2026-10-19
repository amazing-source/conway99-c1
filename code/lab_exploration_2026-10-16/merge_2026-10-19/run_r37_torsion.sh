#!/bin/bash
# rank 37, c = 2 lines with d = 3 (7-torsion in a component): balanced (residual rank 2) and unbalanced (b c^T + c b^T)
S="$1"; OUT="$2"
PY=/c/home/researcher/conway99-env/.venv/Scripts/python.exe
run() { # gt seed rho delta
  f="$S/t_$(echo $1 | tr ':,' '__')_s$2_r$3_d$4.bin"
  meta=$(timeout 280 $PY oblr_prep.py $1 $2 0 $3 $4 "$f" | sed 's/, "s01.*/}/')
  res=$(timeout 230 ./oblr.exe "$f" 200)
  echo "{\"meta\": $meta, \"mode\": \"$3/$4\", \"res\": $res}" >> "$OUT"
  rm -f "$f"
}
for sd in 1 2 3; do for bl in blockst:3,3 blockst:2,4 blockst:1,5; do
  run $bl $sd 2 1; run $bl $sd 2 3; run $bl $sd -1 1
done; done
echo DONE >> "$OUT"
