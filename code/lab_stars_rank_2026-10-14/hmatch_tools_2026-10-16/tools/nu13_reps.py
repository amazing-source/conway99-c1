"""Case II exact sweep (16/10 night): h-invariant T, U PSD structures of nullity exactly 13 on file, one representative
per distinct exact kernel; written as newk_k.json into <out dir> for ksat_dir.py (complete enumeration of all
admissible structures containing that 13-dimensional kernel: a member of nullity 14 with broken star matchings and
T, U PSD would refute (H-MATCH)).  usage: python nu13_reps.py <out dir> <glob> [...]"""
import glob, json, os, sys
import numpy as np
from fractions import Fraction as Fr
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
seen = set(); kernels = set(); k = 0
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
    w, V = np.linalg.eigh(T)
    if int(np.sum(np.abs(w) < 1e-7)) != 13: continue
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    Uu = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ Uu @ P + 50 * Q @ Q.T)[0] < -1e-9: continue
    N = V[:, np.abs(w) < 1e-7]
    Pn = N @ N.T
    kk = tuple(np.round(Pn, 6).ravel())
    if kk in kernels: continue
    kernels.add(kk)
    json.dump({"labels": d["labels"], "edges": d["edges"], "source": f}, open(os.path.join(out, "newk_%d.json" % k), "w"))
    k += 1
print("distinct h-invariant PSD nullity-13 kernels:", k, "(from", len(seen), "distinct structures)")
