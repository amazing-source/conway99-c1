"""How badly do broken structures miss positivity? (LAB 15/10/2026, task T3, quantitative form of (H-INV)).

Enumerates (as kernel_sat_enum.py, SAT + DP encoding of Gamma n = (3I - K) n) ALL admissible structures whose kernel
contains the kernel of a given structure, and for each structure computes the h-block decomposition
    T = [[A, B], [B^T, C]],  U = 7 Pi - T = [[A', -B], [-B^T, C']]   (E_+ / E_- = h-even / h-odd, h = (0 1)(2 3))
and the scale factors tT = sup{t : [[A, tB], [tB^T, C]] >= 0}, tU = sup{t : [[A', -tB], [-tB^T, C']] >= 0}
(tT = 0 when B^T does not vanish on ker A or A, C are not PSD; likewise for tU).  T, U >= 0 <=> tT >= 1 and tU >= 1
(given A, C, A', C' >= 0).  For broken structures (B != 0), min(tT, tU) < 1 measures how much B must shrink.
usage: python kernel_sat_measure.py <structure json> <out summary json> [max seconds]"""
import itertools
import json
import os
import random
import sys
import time
from collections import Counter

import numpy as np
from pycryptosat import Solver

sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS
from cls_decomp import nullspace_int

f, outf = sys.argv[1], sys.argv[2]
maxsec = float(sys.argv[3]) if len(sys.argv) > 3 else 3000
d = json.load(open(f))
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
assert [sorted(l) for l in S] == d["labels"]
E0 = {tuple(sorted(x)) for x in d["edges"]}
K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
G0 = [[1 if tuple(sorted((a, b))) in E0 else 0 for b in range(n)] for a in range(n)]
M = [[(24 if a == b else 0) - 8 * G0[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
N = nullspace_int(M)
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
nv = F.n
for vec in N:
    for i in range(n):
        tot = sum((24 if i == j else 0) * vec[j] - K8[i][j] * vec[j] for j in range(n))
        r = tot // 8
        terms = [(e[(i, j)], vec[j]) for j in range(n) if j != i and vec[j]]
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
Kf = np.array([[kval(a, b) for b in S] for a in S])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
P7 = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
H = np.zeros((n, n))
for i in range(n):
    H[hp[i], i] = 1
Qp = np.linalg.svd((np.eye(n) + H) / 2)[0][:, :22]
Qm = np.linalg.svd((np.eye(n) - H) / 2)[0][:, :22]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
pairs = list(itertools.combinations(range(n), 2))


def psd_root_pinv(X):
    w, V = np.linalg.eigh((X + X.T) / 2)
    if w[0] < -1e-8:
        return None, None
    keep = w > 1e-8
    return V[:, keep] / np.sqrt(w[keep]), V[:, ~keep]


REASONS = Counter()


def scale(Ab, Bb, Cb, tag=""):
    """sup t with [[Ab, tBb], [tBb^T, Cb]] >= 0 (Ab, Cb PSD required; Bb^T must vanish on ker Ab and Bb on ker Cb)."""
    Ra, Na = psd_root_pinv(Ab)
    Rc, Nc = psd_root_pinv(Cb)
    if Ra is None:
        REASONS[tag + ": even block not PSD"] += 1
        return 0.0
    if Rc is None:
        REASONS[tag + ": odd block not PSD"] += 1
        return 0.0
    if Na.shape[1] and np.abs(Bb.T @ Na).max() > 1e-8:
        REASONS[tag + ": B^T leaks into ker(even block) (dim %d)" % Na.shape[1]] += 1
        return 0.0
    if Nc.shape[1] and np.abs(Bb @ Nc).max() > 1e-8:
        REASONS[tag + ": B leaks into ker(odd block) (dim %d)" % Nc.shape[1]] += 1
        return 0.0
    REASONS[tag + ": finite scale"] += 1
    Mx = Ra.T @ Bb @ Rc
    s = np.linalg.norm(Mx, 2)
    return float('inf') if s < 1e-12 else 1.0 / s


t0 = time.time()
cnt = 0
complete = False
hist = Counter()
broken_scales = []
while time.time() - t0 < maxsec:
    ok, model = sol.solve()
    if not ok:
        complete = True
        break
    cnt += 1
    sol.add_clause([-e[p] if model[e[p]] else e[p] for p in pairs])
    G = np.zeros((n, n))
    for p in pairs:
        if model[e[p]]:
            G[p] = 1
            G[p[1], p[0]] = 1
    T = 3 * np.eye(n) - G - Kf
    U = P7 - T
    nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
    lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
    lu = float(np.linalg.eigvalsh(Pp @ U @ Pp + 50 * (np.eye(n) - Pp))[0])
    broken = any(G[i, j] != G[hp[i], hp[j]] for (i, j) in sl)
    A, B, C = Qp.T @ T @ Qp, Qp.T @ T @ Qm, Qm.T @ T @ Qm
    A2, C2 = Qp.T @ U @ Qp, Qm.T @ U @ Qm
    nb = float(np.abs(B).max())
    tT = scale(A, B, C, 'T') if nb > 1e-9 else float('inf')
    tU = scale(A2, -B, C2, 'U') if nb > 1e-9 else float('inf')
    psd = min(lt, lu) > -1e-9
    hist[(psd, nul, broken, "A,C psd" if np.linalg.eigvalsh(A)[0] > -1e-8 and np.linalg.eigvalsh(C)[0] > -1e-8 else "A or C not psd")] += 1
    if nb > 1e-9:
        rec = {"nullity": nul, "psd": psd, "lambda_T": lt, "lambda_U": lu, "tT": tT, "tU": tU,
               "rankB": int(np.linalg.matrix_rank(B, tol=1e-8)), "broken_matchings": bool(broken)}
        if 0 < tU < float('inf'):                       # near-misses: both average blocks of U are PSD
            rec["edges"] = [[i, j] for i, j in pairs if G[i, j]]
        broken_scales.append(rec)
    if cnt % 2000 == 0:
        print("progress: %d structures, %.0f s" % (cnt, time.time() - t0), flush=True)
print("%d structures (%s), %.0f s" % (cnt, "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
print("(PSD, nullity, matchings broken, symmetric blocks): count")
for k, v in sorted(hist.items(), key=str):
    print("  ", k, v)
if broken_scales:
    tts = np.array([b["tT"] for b in broken_scales])
    tus = np.array([b["tU"] for b in broken_scales])
    mins = np.minimum(tts, tus)
    print("structures with B != 0: %d ; tT in [%.3f, %.3f], tU in [%.3f, %.3f], min(tT, tU) max = %.4f"
          % (len(broken_scales), tts.min(), tts.max(), tus.min(), tus.max(), mins.max()))
    print("  fraction with tT = 0 (B^T leaks into ker A or A/C not PSD): %.3f ; with tU = 0: %.3f"
          % (float(np.mean(tts == 0)), float(np.mean(tus == 0))))
    print("  min(tT, tU) quantiles 50/90/99/100%%: %s" % (np.round(np.quantile(mins, [0.5, 0.9, 0.99, 1.0]), 4).tolist()))
print("reasons:", dict(REASONS))
json.dump({"source": f, "count": cnt, "complete": complete, "hist": {str(k): v for k, v in hist.items()},
           "labels": d["labels"], "broken": broken_scales[:20000]}, open(outf, "w"))
