"""Broken obj53-class structures (and the kmilp ambig files): lambda_min(T) and lambda_min(U) on the complement of the
star vectors, lambda_min of the h-odd block C' of U and of the h-even block A' of U; lists those with T >= 0 and C' >= 0.
usage: python obj53_cprime.py <glob> [...]"""
import glob, json, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
hm = {0: 1, 1: 0, 2: 3, 3: 2}
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
rows = []; seen = set()
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
    sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
    if all(G[i, j] == G[hp[i], hp[j]] for (i, j) in sl): continue
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    if nu < 14: continue
    Us = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    lt = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0]; lu = np.linalg.eigvalsh(P @ Us @ P + 50 * Q @ Q.T)[0]
    H = np.zeros((n, n))
    for i, j in enumerate(hp): H[j, i] = 1
    U1, s1, _ = np.linalg.svd((np.eye(n) + H) / 2); Be = U1[:, s1 > 0.5]
    U2, s2, _ = np.linalg.svd((np.eye(n) - H) / 2); Bo = U2[:, s2 > 0.5]
    # complements of the star vectors inside each sector
    def compl(B, vecs):
        X = B.T @ vecs; u, s, vt = np.linalg.svd(X, full_matrices=True); r = int(np.sum(s > 1e-9)); return B @ u[:, r:]
    st = Z
    Be2 = compl(Be, st); Bo2 = compl(Bo, st)
    lcp = np.linalg.eigvalsh(Bo2.T @ Us @ Bo2)[0]; lap = np.linalg.eigvalsh(Be2.T @ Us @ Be2)[0]
    rows.append((f, nu, lt, lu, lap, lcp))
ok = [r for r in rows if r[2] > -1e-9 and r[5] > -1e-9]
print("broken nullity>=14 structures scanned:", len(rows), "; with T >= 0 and C' >= 0:", len(ok))
for r in [x for x in sorted(ok, key=lambda r: -r[3]) if x[1] >= 15][:4] + sorted(ok, key=lambda r: -r[3])[:2]:
    print("  %s nu %d lambda_T %.4f lambda_U %.4f lambda_min A' %.4f lambda_min C' %.4f" % r)
tp = [r for r in rows if r[2] > -1e-9]
print("with T >= 0 only:", len(tp), "; C' >= 0 regardless of T:", sum(1 for r in rows if r[5] > -1e-9))
