#!/bin/bash
# star-level survivor counts for the 12 (orbit, base star) choices, 12 single-thread processes
cd /c/home/researcher/Desktop/c1_recherche/code/r6/j2
for i in $(seq 1 12); do
  ( ./star0_count.exe $(sed -n ${i}p alphas.txt) > count_$i.out 2>&1 ) &
done
wait
echo ALLDONE
