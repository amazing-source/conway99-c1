#!/bin/bash
# Full inspection of a candidate counterexample to (H-MATCH) (LAB 15/10/2026). Run from work/stars_rank_2026-10-14.
# usage: bash hmatch_tools_2026-10-15/verify_hmatch.sh <json> [python] [pythonpath]
f="$1"; PY="${2:-/c/home/researcher/AppData/Local/Programs/Python/Python312/python.exe}"; export PYTHONPATH="$3"
echo "=================== 1. EXACT VALIDITY (independent verifier, no search code) ==================="
"$PY" -I verify_counterexample.py "$f" edges 0,1,2,3
echo "=================== 2. MATCHINGS (independent combinatorial check) ==================="
"$PY" -I hmatch_tools_2026-10-15/matching_check.py "$f"
echo "=================== 3. HIDDEN SYMMETRIES (h p, p any outer permutation) ==================="
"$PY" hmatch_tools_2026-10-15/hidden_sym.py "$f" | head -14
echo "=================== 4. CONWAY-BLOCK TESTS: DISC, rank mod 7, extension of the 40 outer labels ==================="
"$PY" disc_scan.py "$f"
"$PY" r7_scan.py "$f"
"$PY" ext4.py "$f" all | tail -25
echo "=================== 5. MECHANISM: components, balance, h-blocks, break types, kernel shape ==================="
"$PY" hmatch_tools_2026-10-15/side_check.py "$f"
"$PY" hmatch_tools_2026-10-15/balance.py "$f"
"$PY" hmatch_tools_2026-10-15/hblock_ranks.py "$f"
"$PY" hmatch_tools_2026-10-15/break_types.py "$f"
"$PY" hmatch_tools_2026-10-15/mixed_shape.py "$f"
"$PY" hmatch_tools_2026-10-15/kernel_shape.py "$f"
