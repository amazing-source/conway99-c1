"""h-invariant structures: spectrum of Gamma_S on the h-odd sector (signed quotient graph, 22 vertices).
Claim: T_S >= 0 => lambda_max(Gamma odd) <= 3 (k1 = chi0-chi1, k2 = chi2-chi3 have eigenvalue 0), and
odd nullity of T_S = 2 + multiplicity of the eigenvalue 3.  Prints lambda_max, multiplicity of 3, odd nullity.
usage: python odd_spectral.py <glob> [...]"""
import glob, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
hm = {0: 1, 1: 0, 2: 3, 3: 2}
files = []
for g in sys.argv[1:]: files += sorted(glob.glob(g))
seen = set(); cnt = Counter(); gaps = {}
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
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    H = np.zeros((n, n))
    for i, j in enumerate(hp): H[j, i] = 1
    Po = (np.eye(n) - H) / 2
    U, s, _ = np.linalg.svd(Po); Bo = U[:, s > 0.5]
    go = np.linalg.eigvalsh(Bo.T @ G @ Bo)
    to = np.linalg.eigvalsh(Bo.T @ T @ Bo)
    lmax = go[-1]; m3 = int(np.sum(np.abs(go - 3) < 1e-7)); onull = int(np.sum(np.abs(to) < 1e-7))
    k = ("grid" if grid else "nogrid", "odd nullity %d" % onull, "mult(3) %d" % m3, "consistent" if onull == 2 + m3 else "INCONSISTENT")
    cnt[k] += 1
    if not grid:
        gaps.setdefault(k, []).append(3 - (go[go < 3 - 1e-7].max()))
    if lmax > 3 + 1e-7: cnt[("lambda_max > 3 !!", f)] += 1
for k in sorted(cnt, key=str): print(k, cnt[k])
for k, v in gaps.items(): print(k, "gap 3 - (largest eigenvalue below 3): min %.4f" % min(v))
