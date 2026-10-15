"""Cauchy-Schwarz test (tr R)^2 / tr(R^2) on every h-invariant T, U PSD structure, both sides (R = even residual of
the m-side over the l-side, see even_residual.py); a ratio > 2 certifies rank R >= 3 (EVEN3).
usage (from work/stars_rank_2026-10-14): python hmatch_tools_2026-10-15/n9ng_attack/cs_ratio_test.py"""
import glob, json, sys
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval, LABELS
hm = {0: 1, 1: 0, 2: 3, 3: 2}
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
def resid(S, idx, T, a0, a1, b0, b1):
    n = len(S)
    def vec(pairs):
        v = np.zeros(n)
        for pq in pairs: v[idx[frozenset(pq)]] = 1
        return v
    U = [vec([(a0, y), (a1, y)]) for y in range(4, 14)]
    Gv = [vec([(b0, y), (b1, y)]) for y in range(4, 14)]
    p = vec([(a0, b0), (a1, b1)]); q = vec([(a0, b1), (a1, b0)])
    L = np.array(U + [p, q]).T; M = np.array(Gv).T
    R = M.T @ T @ M - (L.T @ T @ M).T @ np.linalg.pinv(L.T @ T @ L, rcond=1e-10) @ (L.T @ T @ M)
    R = (R + R.T) / 2
    w = np.linalg.eigvalsh(R)
    return int(np.sum(np.abs(w) > 1e-7)), float(np.trace(R)) ** 2 / max(float(np.sum(w ** 2)), 1e-12)
seen = set(); rows = []
files = sorted(glob.glob("*.json")) + sorted(glob.glob("hmatch_tools_2026-10-15/psd_*/*.json")) + sorted(glob.glob("hmatch_tools_2026-10-15/ng14_distinct/*.json"))
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
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    if not np.array_equal(G[np.ix_(hp, hp)], G): continue
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    Uu = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ Uu @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    r1, c1 = resid(S, idx, T, 0, 1, 2, 3); r2, c2 = resid(S, idx, T, 2, 3, 0, 1)
    rows.append(("grid" if grid else "no grid", nu, r1, r2, c1, c2, f))
for g in ("no grid", "grid"):
    sel = [r for r in rows if r[0] == g]
    if not sel: continue
    print("%s: %d h-invariant PSD structures; min rank R %d; min CS ratio %.3f; CS ratio <= 2 in %d structures"
          % (g, len(sel), min(min(r[2], r[3]) for r in sel), min(min(r[4], r[5]) for r in sel),
             sum(1 for r in sel if min(r[4], r[5]) <= 2 + 1e-9)))
    for r in sorted(sel, key=lambda r: min(r[4], r[5]))[:4]: print("    ", r[:6], r[6])
