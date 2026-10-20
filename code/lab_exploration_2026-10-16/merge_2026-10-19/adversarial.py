"""Adversarial search for line graphs G_T that RESIST the rank-37 obligation (LAB 20/10/2026, step 2).

State: a connected cubic line graph G_T (three bijections s01, s12, s20 between the classes, partner i <-> i^1) with
d = 1 (7 does not divide tau) and (tau | 7) = -1 (Codex's L23: the only generic connected lines possible at rank 37),
K >= 0.  Score = number of search nodes oblr2 needs to refute the rank-37 far structure (rho = 0), time-limited.
Move: swap two images in one of the three bijections; keep the move if every condition still holds and the score does
not decrease (plateau moves allowed), else accept with probability exp((score' - score) / temp) (simulated annealing on
log score).  Any FOUND is saved at once (it would be a far structure satisfying every exact constraint of the line).
Runs at IDLE priority.  usage: python adversarial.py <seed> <steps> <engine seconds> <out.jsonl>"""
import ctypes
import json
import math
import os
import random
import subprocess
import sys
import tempfile

import numpy as np

if sys.platform == "win32":
    ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x40)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from oblr_prep import P7, near_block  # noqa: E402
from ll_test import components, gt_matrix, k_matrix, random_gt  # noqa: E402
from rank7_line import rank_mod  # noqa: E402

n = 12


def det_mod(M, p):
    M = M.copy() % p
    k = M.shape[0]
    det = 1
    for c in range(k):
        piv = np.nonzero(M[c:, c])[0]
        if len(piv) == 0:
            return 0
        i = c + piv[0]
        if i != c:
            M[[c, i]] = M[[i, c]]
            det = -det
        det = det * int(M[c, c]) % p
        inv = pow(int(M[c, c]), p - 2, p)
        M[c] = M[c] * inv % p
        rows = np.nonzero(M[c + 1:, c])[0] + c + 1
        if len(rows):
            M[rows] = (M[rows] - np.outer(M[rows, c], M[c])) % p
    return det % p


def legal(s01, s12, s20):
    G = gt_matrix(n, s01, s12, s20)
    if (k_matrix(n, G) < 0).any():
        return None
    nc, _ = components(G)
    if nc != 1:
        return None
    L = (3 * np.eye(3 * n, dtype=np.int64) - G) % P7
    if 3 * n - rank_mod(L, P7) != 1:
        return None
    t = det_mod(L[1:, 1:], P7)                            # tau mod 7 (any cofactor of the Laplacian)
    if pow(t, 3, P7) != P7 - 1:                           # Euler: (t|7) = t^3 mod 7; need -1
        return None
    return G


def score(s01, s12, s20, sec, tmpdir):
    f = os.path.join(tmpdir, "adv.bin")
    meta = subprocess.run([sys.executable, os.path.join(HERE, "oblr_prep_gt.py"), json.dumps([s01, s12, s20]), f],
                          capture_output=True, text=True)
    if meta.returncode:
        return None, meta.stderr[-300:]
    r = subprocess.run([os.path.join(HERE, "oblr2.exe"), f, str(sec)], capture_output=True, text=True)
    res = json.loads(r.stdout.strip().splitlines()[-1])
    return res, None


def main():
    seed, steps, sec, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4]
    rng = random.Random(seed)
    tmpdir = tempfile.mkdtemp(prefix="adv_")
    while True:
        s01, s12, s20, _ = random_gt(n, rng, 1)
        if legal(s01, s12, s20) is not None:
            break
    res, err = score(s01, s12, s20, sec, tmpdir)
    cur = math.log(res["nodes"] + 1)
    best = (cur, [s01[:], s12[:], s20[:]], res)
    temp = 0.3
    for step in range(steps):
        t01, t12, t20 = s01[:], s12[:], s20[:]
        which = rng.choice((t01, t12, t20))
        i, j = rng.sample(range(n), 2)
        which[i], which[j] = which[j], which[i]
        if legal(t01, t12, t20) is None:
            continue
        r2, err = score(t01, t12, t20, sec, tmpdir)
        if r2 is None:
            continue
        new = math.log(r2["nodes"] + 1)
        rec = {"step": step, "nodes": r2["nodes"], "depth": r2["max_depth"], "status": r2["status"],
               "accepted": False}
        if r2["status"] == "FOUND":
            rec["gt"] = [t01, t12, t20]
            rec["res"] = r2
        if new >= cur or rng.random() < math.exp((new - cur) / temp):
            s01, s12, s20, cur = t01, t12, t20, new
            rec["accepted"] = True
            if new > best[0]:
                best = (new, [t01[:], t12[:], t20[:]], r2)
                rec["best"] = True
                rec["gt"] = [t01, t12, t20]
        with open(out, "a") as g:
            g.write(json.dumps(rec) + "\n")
    with open(out, "a") as g:
        g.write(json.dumps({"final_best_nodes": best[2]["nodes"], "final_best_depth": best[2]["max_depth"],
                            "final_best_status": best[2]["status"], "gt": best[1]}) + "\n")


if __name__ == "__main__":
    main()
