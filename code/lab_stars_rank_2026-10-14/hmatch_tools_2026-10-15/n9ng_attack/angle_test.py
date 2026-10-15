"""Principal angles between the V4-quotient spans of the two sides: V_L = span(u_y, 1_C), V_M = span(g_y, 1_C) in the
Gram geometry of A++.  dim(V_L n V_M) <= sum cos^2 = tr(P_L P_M).  (QUOT) <=> dim(V_L n V_M) <= 8 - max c.
Reports tr(P_L P_M) against 9 - max c (a strict inequality tr < 9 - max c would prove QUOT for that structure).
usage: python angle_test.py <glob> [...]"""
import glob, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
seen = set(); rows = []
for f in files:
    try: d = json.load(open(f))
    except Exception: continue
    if not isinstance(d, dict) or "edges" not in d or len(d.get("labels", [])) != 44: continue
    S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen: continue
    seen.add(key)
    G = np.zeros((n, n))
    for a, b in d["edges"]: G[a, b] = G[b, a] = 1
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    if grid: continue
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    W = []
    for (a, b) in ((0, 1), (2, 3)):
        for y in range(4, 14):
            v = np.zeros(n); v[idx[frozenset((a, y))]] = 1; v[idx[frozenset((b, y))]] = 1; W.append(v)
    v = np.zeros(n)
    for p in ((0, 2), (0, 3), (1, 2), (1, 3)): v[idx[frozenset(p)]] = 1
    W.append(v); W = np.array(W).T
    A = W.T @ T @ W
    w, V = np.linalg.eigh(A); keep = w > 1e-9
    F = (V[:, keep] * np.sqrt(w[keep])).T          # Gram factor: columns = Gram vectors of the 21 orbit vectors
    L = list(range(10)) + [20]; M = list(range(10, 21))
    def proj(cols):
        X = F[:, cols]; U, s, _ = np.linalg.svd(X, full_matrices=False); U = U[:, s > 1e-7]; return U @ U.T
    PL, PM = proj(L), proj(M)
    tr = float(np.trace(PL @ PM))
    sv = np.linalg.svd(np.linalg.svd(F[:, L], full_matrices=False)[0][:, np.linalg.svd(F[:, L], compute_uv=False) > 1e-7].T @
                       np.linalg.svd(F[:, M], full_matrices=False)[0][:, np.linalg.svd(F[:, M], compute_uv=False) > 1e-7], compute_uv=False)
    dint = int(np.sum(sv > 1 - 1e-7))
    def side(st):
        lab = [i for i in range(n) if S[i] & set(st)]
        return int(np.sum(np.abs(np.linalg.eigvalsh(T[np.ix_(lab, lab)])) < 1e-7)) - 1
    cl, cm = side((0, 1)), side((2, 3))
    rows.append((tr - (9 - max(cl, cm)), tr, dint, 8 - max(cl, cm), cl, cm, f))
rows.sort(reverse=True)
print("non-grid T>=0 structures: %d; tr(P_L P_M) < 9 - max c in %d of them" % (len(rows), sum(1 for r in rows if r[0] < -1e-9)))
for r in rows[:8]: print("  tr - (9 - max c) = %.3f  tr = %.3f  dim(int) = %d (bound %d)  c = (%d,%d)  %s" % r)
