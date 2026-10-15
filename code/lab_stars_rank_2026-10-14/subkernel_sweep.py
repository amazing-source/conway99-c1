"""Sub-kernel sweep (LAB 15/10/2026, (H-MATCH) test beyond the known kernels).

For each distinct kernel N of the 331 rank-30 objects (kernel_classes_331.json), split N = (star vectors) + (10
complementary basis vectors), drop DROP random complementary vectors (seeded), and enumerate with SAT ALL admissible
structures whose kernel contains the remaining (14 - DROP)-dimensional space (same DP encoding as kernel_sat_enum.py).
These structures have nullity >= 14 - DROP; those of nullity >= 14 have DROP kernel directions that are NOT prescribed
(possibly with h-odd components).  Reports, per run, the counts by (PSD, nullity, star matchings broken) and every
PSD structure of nullity >= 14 with broken star matchings (TARGET, saved _SK_*.json).
usage: python subkernel_sweep.py <runs per kernel> <drop> <seconds per run> [first rep] [last rep]"""
import itertools
import json
import random
import sys
import time
from collections import Counter

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from cls_decomp import nullspace_int

runs, drop, tsec = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3])
bundle = json.load(open("rank30_psd_objects_2026-10-15.json"))
reps = json.load(open("kernel_classes_331.json"))["reps"]
first = int(sys.argv[4]) if len(sys.argv) > 4 else 0
last = int(sys.argv[5]) if len(sys.argv) > 5 else len(reps) - 1
rng0 = random.Random(2026)
S0, idx0, e0, F0 = build([0, 1, 2, 3], random.Random(5))
n = len(S0)
assert [sorted(l) for l in S0] == bundle["labels"]
K8 = [[int(round(8 * kval(a, b))) for b in S0] for a in S0]
Kf = np.array([[kval(a, b) for b in S0] for a in S0])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S0], [pos[l] for l in S0])]
Z = np.array([[1.0 if y in l else 0.0 for l in S0] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx0[frozenset(hm.get(y, y) for y in s)] for s in S0]
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S0[i] & S0[j] & {0, 1, 2, 3}]
pairs = list(itertools.combinations(range(n), 2))
stars = [[1 if y in S0[i] else 0 for i in range(n)] for y in (0, 1, 2, 3)]
grand = Counter()
targets = 0
for ri in range(first, last + 1):
    k = reps[ri]
    st = bundle["structures"][k]
    E0 = {tuple(sorted(x)) for x in st["edges"]}
    M = [[(24 if a == b else 0) - 8 * (1 if tuple(sorted((a, b))) in E0 else 0) - K8[a][b] for b in range(n)]
         for a in range(n)]
    N = nullspace_int(M)
    # complementary vectors: greedy, independent modulo the star span
    comp = []
    base = [list(map(float, v)) for v in stars]
    for v in N:
        trial = np.array(base + [list(map(float, v))])
        if np.linalg.matrix_rank(trial, tol=1e-9) > len(base):
            base.append(list(map(float, v)))
            comp.append(v)
    assert len(comp) == 10, len(comp)
    for run in range(runs):
        keep = sorted(rng0.sample(range(10), 10 - drop))
        Nsub = stars + [comp[q] for q in keep]
        sol = Solver()
        for c in F0.clauses:
            sol.add_clause(c)
        nv = F0.n
        for vec in Nsub:
            for i in range(n):
                tot = sum((24 if i == j else 0) * vec[j] - K8[i][j] * vec[j] for j in range(n))
                r = tot // 8
                terms = [(e0[(i, j)], vec[j]) for j in range(n) if j != i and vec[j]]
                if not terms:
                    continue
                kk = len(terms)
                lo_suf = [0] * (kk + 1)
                hi_suf = [0] * (kk + 1)
                for t in range(kk - 1, -1, -1):
                    c = terms[t][1]
                    lo_suf[t] = lo_suf[t + 1] + min(0, c)
                    hi_suf[t] = hi_suf[t + 1] + max(0, c)
                layer = {0: None}
                for t, (x, c) in enumerate(terms):
                    nxt = {}
                    for v, yv in layer.items():
                        for val, lit in ((v, -x), (v + c, x)):
                            if not (val + lo_suf[t + 1] <= r <= val + hi_suf[t + 1]):
                                sol.add_clause([-lit] if yv is None else [-yv, -lit])
                                continue
                            if val not in nxt:
                                nv += 1
                                nxt[val] = nv
                            sol.add_clause([-lit, nxt[val]] if yv is None else [-yv, -lit, nxt[val]])
                    layer = nxt
        t0 = time.time()
        hist = Counter()
        cnt = 0
        complete = False
        while time.time() - t0 < tsec:
            ok, model = sol.solve()
            if not ok:
                complete = True
                break
            cnt += 1
            sol.add_clause([-e0[p] if model[e0[p]] else e0[p] for p in pairs])
            G = np.zeros((n, n))
            for (i, j) in pairs:
                if model[e0[(i, j)]]:
                    G[i, j] = G[j, i] = 1
            T = 3 * np.eye(n) - G - Kf
            nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
            if nul < 14:
                hist[("nul<14",)] += 1
                continue
            lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
            lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
            psd = min(lt, lu) > -1e-9
            masym = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
            hist[(psd, nul, masym > 0)] += 1
            if psd and masym > 0:
                targets += 1
                out = "subk_SK_%d_%d_%d.json" % (k, run, targets)
                json.dump({"labels": bundle["labels"], "edges": [[i, j] for i, j in pairs if G[i, j]], "masym": masym,
                           "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul, "from_object": k, "kept": keep},
                          open(out, "w"))
                print("SUBKERNEL TARGET: PSD, nullity %d, broken matchings (%d), object %d run %d, saved %s"
                      % (nul, masym, k, run, out), flush=True)
        for key, v in hist.items():
            grand[key] += v
        print("rep %d (object %d) run %d keep %s: %d structures (%s, %.0f s) %s"
              % (ri, k, run, keep, cnt, "COMPLETE" if complete else "stopped", time.time() - t0, dict(hist)), flush=True)
print("TOTAL (PSD, nullity, broken) over nullity >= 14:", dict(grand), "targets:", targets, flush=True)
