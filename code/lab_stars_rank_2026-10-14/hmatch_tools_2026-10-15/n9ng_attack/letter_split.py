"""Split of ker T_S by letter sums: nu0 = dim(ker T_S n ker B) (these are exactly the 3-eigenvectors of Gamma_S with
zero letter sums), nuB = dim B(ker T_S) (letter-sum profiles, <= 14).  Also lambda_max of Gamma_S compressed to ker B.
usage: python letter_split.py <glob> [...]"""
import glob, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
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
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    w_, V = np.linalg.eigh(T); N = V[:, np.abs(w_) < 1e-7]; nu = N.shape[1]
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    tpsd = np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] > -1e-9
    if not tpsd: continue
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    B = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in range(14)])
    BN = B @ N
    nuB = int(np.sum(np.linalg.svd(BN, compute_uv=False) > 1e-7)) if nu else 0
    nu0 = nu - nuB
    # compression of Gamma to ker B
    u, s, vt = np.linalg.svd(B); r = int(np.sum(s > 1e-9)); KB = vt[r:].T
    lm = np.linalg.eigvalsh(KB.T @ G @ KB)[-1]
    k = ("grid" if grid else "nogrid", nu, nu0, nuB)
    cnt[k] += 1; ex.setdefault(k, (f, round(lm, 4)))
for k in sorted(cnt): print(k, cnt[k], ex[k])
