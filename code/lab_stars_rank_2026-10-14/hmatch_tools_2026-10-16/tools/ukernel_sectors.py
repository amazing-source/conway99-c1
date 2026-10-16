"""h-invariant T, U PSD structures: nullities of U in the h-even and h-odd sectors beyond the 4 star vectors
(nu(A'), nu(C') on the complements of the stars), against nu(T) and nu(A).  Is the odd U-kernel forced at nu(T) = 14?
usage: python ukernel_sectors.py <glob> [...]"""
import glob, json, sys
from collections import Counter
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
seen = set(); cnt = Counter(); ex = {}
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
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    Us = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    if np.linalg.eigvalsh(P @ Us @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    H = np.zeros((n, n))
    for i, j in enumerate(hp): H[j, i] = 1
    U1, s1, _ = np.linalg.svd((np.eye(n) + H) / 2); Be = U1[:, s1 > 0.5]
    U2, s2, _ = np.linalg.svd((np.eye(n) - H) / 2); Bo = U2[:, s2 > 0.5]
    def compl(B):
        X = B.T @ Z; u, s, vt = np.linalg.svd(X, full_matrices=True); r = int(np.sum(s > 1e-9)); return B @ u[:, r:]
    Be2, Bo2 = compl(Be), compl(Bo)
    nA = int(np.sum(np.abs(np.linalg.eigvalsh(Be2.T @ T @ Be2)) < 1e-7)); nC = int(np.sum(np.abs(np.linalg.eigvalsh(Bo2.T @ T @ Bo2)) < 1e-7))
    nAp = int(np.sum(np.abs(np.linalg.eigvalsh(Be2.T @ Us @ Be2)) < 1e-7)); nCp = int(np.sum(np.abs(np.linalg.eigvalsh(Bo2.T @ Us @ Bo2)) < 1e-7))
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    k = (nu, nA, nC, nAp, nCp, "grid" if grid else "nogrid")
    cnt[k] += 1; ex.setdefault(k, f)
print("(nu T, nu A*, nu C*, nu A'*, nu C'*, grid) [* = beyond the star vectors of the sector]: count, example")
for k in sorted(cnt, key=lambda k: (-k[0], k)): print(" ", k, cnt[k], ex[k])
