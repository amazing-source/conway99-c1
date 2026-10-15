"""Orientation-free tests for a fixed h-average (LAB 15/10/2026, task T3; tests proposed by Codex, message of 15/10
~09:50 UTC, re-implemented independently here).

For a broken structure Gamma, the average Gamma_0 = (Gamma + h Gamma h)/2 fixes A, C (blocks of T) and A', C' (blocks
of U = 7 Pi - T) on E_+ / E_- (orthonormal h-bases), and the set of broken edge orbits k = {e, h(e)} (exactly one of the
two label pairs is an edge).  The orientations eps_k = +-1 (which pair carries the edge) only change the mixed block
    B = sum_k eps_k B_k,   B_k = -(1/2) Q_+^T (E_e - E_h(e)) Q_-,   <B_k, B_l>_F = delta_kl / 2,  ||B||_F^2 = b / 2.
If T >= 0 then B^T kills ker A, so rank B <= rank A.  If moreover U >= 0:
  (1) shorted test: ||B||_F^2 = b/2 <= sum_{i <= rank A} lambda_i(S) lambda_i(C') (decreasing), where S is A' shorted
      to range A (Schur complement of A' on ker A);
  (2) orientation Gram: with H_kl = tr(S^+ B_k C'^+ B_l^T) (B_k restricted to range A), every orientation satisfies
      eps^T H eps <= rank A.  Lower bounds for min over eps: b lambda_min(H); for any diagonal d,
      eps^T H eps >= sum d + b lambda_min(H - diag d) (optimised here by subgradient ascent on d).
A bound > rank A excludes EVERY orientation of the average (admissible or not).  Range conditions (B_k leaking into
ker S or ker C') are reported, not used.
usage: python orient_tests.py <json with "labels" and "edges" | measure json with "broken" list> [max items]"""
import itertools
import json
import random
import sys

import numpy as np

sys.path.insert(0, '.')
from stars_rank import build, kval, LABELS

f = sys.argv[1]
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
d = json.load(open(f))
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
assert [sorted(l) for l in S] == d["labels"]
items = [r["edges"] for r in d["broken"] if "edges" in r] if "broken" in d else [d["edges"]]
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
pairs = list(itertools.combinations(range(n), 2))
TOL = 1e-8


def split(X):
    w, V = np.linalg.eigh((X + X.T) / 2)
    return w, V


seen = set()
out = []
for edges in items[:mx]:
    G = np.zeros((n, n))
    for i, j in edges:
        G[i, j] = G[j, i] = 1
    hG = G[np.ix_(hp, hp)]                     # (h Gamma h)[i, j] = Gamma[h i, h j]
    G0 = (G + hG) / 2
    key = tuple(np.round(2 * G0[np.triu_indices(n, 1)]).astype(int))
    if key in seen:
        continue
    seen.add(key)
    T0 = 3 * np.eye(n) - G0 - Kf
    U0 = P7 - T0
    A, C = Qp.T @ T0 @ Qp, Qm.T @ T0 @ Qm
    A2, C2 = Qp.T @ U0 @ Qp, Qm.T @ U0 @ Qm
    wA, VA = split(A)
    if wA[0] < -TOL or split(C)[0][0] < -TOL or split(A2)[0][0] < -TOL or split(C2)[0][0] < -TOL:
        print("average with a non-PSD symmetric block: skipped (min eig A %.3f C %.3f A' %.3f C' %.3f)"
              % (wA[0], split(C)[0][0], split(A2)[0][0], split(C2)[0][0]))
        continue
    Nk = VA[:, wA < TOL]                       # ker A (orthonormal)
    R = VA[:, wA >= TOL]                       # range A
    rkA = R.shape[1]
    # broken edge orbits
    orbs = []
    for (i, j) in pairs:
        a, b = hp[i], hp[j]
        hpair = (min(a, b), max(a, b))
        if (i, j) < hpair and G[i, j] != G[hpair]:
            orbs.append(((i, j), hpair))
    bcount = len(orbs)
    Bks = []
    for (p, q) in orbs:
        Dk = np.zeros((n, n))
        Dk[p] = Dk[p[::-1]] = 1
        Dk[q] = Dk[q[::-1]] = -1
        Bks.append(-0.5 * Qp.T @ Dk @ Qm)
    Bact = Qp.T @ (3 * np.eye(n) - G - Kf) @ Qm
    eps = np.array([1.0 if G[p] else -1.0 for (p, q) in orbs])
    assert np.allclose(sum(s * Bk for s, Bk in zip(eps, Bks)), Bact, atol=1e-9)
    # shorted A' on range A:  S = A'_RR - A'_RN (A'_NN)^+ A'_NR  (coordinates of range A)
    ARR, ARN, ANN = R.T @ A2 @ R, R.T @ A2 @ Nk, Nk.T @ A2 @ Nk
    Ssh = ARR - ARN @ np.linalg.pinv(ANN, rcond=1e-10) @ ARN.T
    wS, VS = split(Ssh)
    wC2, VC2 = split(C2)
    lamS = np.sort(np.clip(wS, 0, None))[::-1]
    lamC = np.sort(np.clip(wC2, 0, None))[::-1]
    t1 = float(np.sum(lamS[:rkA] * lamC[:rkA]))
    # leakage of B_k (restricted to range A) into ker S or ker C'
    kerS = VS[:, wS < TOL]
    kerC = VC2[:, wC2 < TOL]
    Br = [R.T @ Bk for Bk in Bks]               # rkA x 22
    leak = max([0.0] + [float(np.abs(kerS.T @ X).max()) if kerS.shape[1] else 0.0 for X in Br]
               + [float(np.abs(X @ kerC).max()) if kerC.shape[1] else 0.0 for X in Br])
    Sp = np.linalg.pinv(Ssh, rcond=1e-10)
    Cp = np.linalg.pinv(C2, rcond=1e-10)
    Hm = np.array([[np.trace(Sp @ Br[k] @ Cp @ Br[l].T) for l in range(bcount)] for k in range(bcount)])
    Hm = (Hm + Hm.T) / 2
    lb0 = bcount * float(np.linalg.eigvalsh(Hm)[0])
    dg = np.diag(Hm).copy()
    gersh = float(np.sum(np.diag(Hm) - (np.abs(Hm).sum(1) - np.abs(np.diag(Hm)))))
    # subgradient ascent on f(d) = sum d + b lambda_min(H - diag d)
    best = max(lb0, gersh)
    dd = np.diag(Hm).copy()
    step = 0.5
    for it in range(400):
        w, V = np.linalg.eigh(Hm - np.diag(dd))
        val = float(dd.sum() + bcount * w[0])
        best = max(best, val)
        g = 1 - bcount * V[:, 0] ** 2
        dd = dd + step * g / (1 + it) ** 0.5
    actual = float(eps @ Hm @ eps)
    # local search for the minimum over orientations (upper estimate of min)
    rng = random.Random(1)
    mn = actual
    for trial in range(20):
        s = np.array([rng.choice((-1.0, 1.0)) for _ in range(bcount)])
        val = s @ Hm @ s
        improved = True
        while improved:
            improved = False
            for k in range(bcount):
                delta = -4 * s[k] * (Hm[k] @ s - Hm[k, k] * s[k])
                if delta < -1e-12:
                    s[k] = -s[k]
                    val += delta
                    improved = True
        mn = min(mn, float(val))
    rec = dict(b=bcount, rankA=rkA, test1_rhs=t1, test1_excl=bool(bcount / 2 > t1 + 1e-9), leak=leak,
               H_actual=actual, H_min_local=mn, lb_eig=lb0, lb_gersh=gersh, lb_best=best,
               test2_excl=bool(best > rkA + 1e-9), trS=float(np.trace(Ssh)), lmaxC2=float(wC2[-1]))
    out.append(rec)
    print("b %d rank A %d | test1: b/2 = %.2f vs sum lambda(S) lambda(C') = %.3f -> %s | tr S %.3f, max eig C' %.3f | "
          "test2: eps^T H eps actual %.3f, local min %.3f, lower bounds eig %.3f gersh %.3f best %.3f -> %s | leak %.1e"
          % (bcount, rkA, bcount / 2, t1, "EXCLUDED" if rec["test1_excl"] else "pass", rec["trS"], rec["lmaxC2"],
             actual, mn, lb0, gersh, best, "EXCLUDED" if rec["test2_excl"] else "inconclusive", leak), flush=True)
print("distinct averages tested: %d ; excluded by test 1: %d ; by test 2 (bounds): %d"
      % (len(out), sum(r["test1_excl"] for r in out), sum(r["test2_excl"] for r in out)))
