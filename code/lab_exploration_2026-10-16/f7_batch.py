"""Batch: minimal-support 7-adic drop vectors on several PSD grid blocks (exploration, LAB 16/10/2026).
Picks up to N distinct PSD blocks with rank_Q - rank_F7 >= 1 (grid blocks in our data), from different sub-folders,
and runs the minimal-support search of f7_minsupport.py on each (first drop vector only, unless --all).
Output: for each block, the drop, and the minimal vector grouped by star and by the second letter, with the corner
values and the corner square.
usage: python f7_batch.py <root dir> <N> <seconds per solve> [--all]"""
import itertools
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from f7_kernel_look import t8, rref_mod, load  # noqa: E402

root, N, secs = sys.argv[1], int(sys.argv[2]), sys.argv[3]
here = os.path.dirname(os.path.abspath(__file__))
picked, folders = [], set()
for dp, dn, fn in os.walk(root):
    if dp in folders:
        continue
    for f in sorted(fn):
        if not f.endswith(".json"):
            continue
        try:
            S, E = load(os.path.join(dp, f))
        except Exception:
            continue
        if len(S) != 44:
            continue
        M = t8(S, E)
        ev = np.linalg.eigvalsh(M.astype(float))
        if ev[0] < -1e-6:
            continue
        rq = int(np.sum(ev > 1e-6))
        r7 = len(rref_mod(M.tolist(), 7)[0])
        if rq - r7 >= 1:
            picked.append((os.path.join(dp, f), rq, r7))
            folders.add(dp)
            break
    if len(picked) >= N:
        break
for path, rq, r7 in picked:
    r = subprocess.run([sys.executable, os.path.join(here, "f7_minsupport.py"), path, secs], capture_output=True,
                       text=True)
    lines = [l for l in r.stdout.splitlines() if l.startswith("block") or l.startswith("drop vector") or
             l.startswith("corner")]
    print("\n".join(lines[:2 if "--all" not in sys.argv else 99] + [l for l in lines if l.startswith("corner")]),
          flush=True)
    print("-", flush=True)
