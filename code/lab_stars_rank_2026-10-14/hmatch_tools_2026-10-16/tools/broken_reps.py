"""Case II exact sweep (16/10 night): all distinct T, U PSD structures on file whose star matchings are NOT h-related,
with nullity >= 11; one representative per distinct h-homogeneous kernel part N n hN (numerical projector key), minus
the two already enumerated (HB_1, asy_best11).  Written as newk_k.json for a KHOMOG run of ksat_dir.py.
usage: python broken_reps.py <out dir> <glob> [...]"""
import glob, json, os, sys
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval, LABELS
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l: D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
hm = {0: 1, 1: 0, 2: 3, 3: 2}
files = []
for g in sys.argv[2:]: files += sorted(glob.glob(g))
seen = set(); keys = {}; rows = []
def homog_key(N, hp):
    # N n hN: vectors x in span(N) with h x in span(N)
    if N.shape[1] == 0: return None, 0
    Ph = N[hp, :]                       # h applied to basis vectors
    # solve N a = Ph b  <=> [N, -Ph] [a; b] = 0
    M = np.hstack([N, -Ph]); u, s, vt = np.linalg.svd(M); r = int(np.sum(s > 1e-8)); C = vt[r:].T
    X = N @ C[:N.shape[1], :]
    if X.shape[1] == 0: return None, 0
    U_, s2, _ = np.linalg.svd(X, full_matrices=False); B = U_[:, s2 > 1e-8]
    return tuple(np.round(B @ B.T, 6).ravel()), B.shape[1]
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
    if all(G[i, j] == G[hp[i], hp[j]] for (i, j) in sl): continue          # star matchings h-related
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    w, V = np.linalg.eigh(T); nu = int(np.sum(np.abs(w) < 1e-7))
    if nu < 11: continue
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    Uu = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ Uu @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    N = V[:, np.abs(w) < 1e-7]
    hk, dh = homog_key(N, hp)
    rows.append((f, nu, dh))
    if hk in keys: continue
    keys[hk] = f
print("distinct broken PSD structures with nullity >= 11:", len(rows))
from collections import Counter
print("  (nullity, dim N n hN):", dict(Counter((r[1], r[2]) for r in rows)))
k = 0
for hk, f in keys.items():
    base = os.path.basename(f)
    if base in ("hm_id_c22_HB_1.json", "asy_best11.json", "asy_hb1_HB_50.json"): continue
    d = json.load(open(f))
    json.dump({"labels": d["labels"], "edges": d["edges"], "source": f}, open(os.path.join(out, "newk_%d.json" % k), "w"))
    print("  rep newk_%d.json <- %s" % (k, f)); k += 1
print("distinct homogeneous kernels:", len(keys), " written:", k)
