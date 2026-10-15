"""Transversals versus the odd defect on PSD structures (LAB 15/10/2026 evening, bridge (T8) after the ODD9 refutation).
For every distinct T, U PSD structure of nullity >= NUMIN (default 13) of a corpus: t(l), t(m) (transversals over the
12 letters other than the line, as in sym4g.py), c(l), c(m) (spectral, 23 - rank T_X), b = dim of the h-odd sector kernel (numerical; b = 2 is
ODD9), grid on (l, m) or not.  Prints the joint table, the minimum of t(l) + t(m) and of min(t) per (nu, b).
usage: python t_odd_scan.py <dir or json> [...]"""
import glob, json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from stars_rank import kval, LABELS
hm = {0: 1, 1: 0, 2: 3, 3: 2}
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
numin = int(os.environ.get("NUMIN", "13"))
files = []
for a in sys.argv[1:]:
    files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
seen = set(); tab = Counter(); ex = {}; mins = defaultdict(lambda: [99, 99, None])
for f in files:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if not isinstance(d, dict) or "edges" not in d or len(d.get("labels", [])) != 44:
        continue
    S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
    key = frozenset(frozenset((S[a], S[b])) for a, b in d["edges"])
    if key in seen:
        continue
    seen.add(key)
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    if nu < numin:
        continue
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    U = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ U @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    tl = sum(1 for x in range(2, 14) if G[idx[frozenset((0, x))], idx[frozenset((1, x))]])
    tm = sum(1 for x in [0, 1] + list(range(4, 14)) if G[idx[frozenset((2, x))], idx[frozenset((3, x))]])
    def comps(a0, a1):
        # spectral c(l) = 23 - rank of T on X_l (= components of the letter graph H_l, G2 / P8)
        X = [i for i in range(n) if S[i] & {a0, a1}]
        w = np.linalg.eigvalsh(T[np.ix_(X, X)])
        return 23 - int(np.sum(np.abs(w) > 1e-7))
    cl, cm = comps(0, 1), comps(2, 3)
    hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
    reps = [i for i in range(n) if i < hp[i]]
    Em = np.zeros((n, 22))
    for k, r in enumerate(reps):
        Em[r, k] = 1 / np.sqrt(2); Em[hp[r], k] = -1 / np.sqrt(2)
    b = int(np.sum(np.abs(np.linalg.eigvalsh(Em.T @ T @ Em)) < 1e-7))
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    k = (nu, b, (cl, cm), (tl, tm), "grid" if grid else "no grid")
    tab[k] += 1; ex.setdefault(k, f)
    mm = mins[(nu, b)]
    if tl + tm < mm[0]:
        mm[0] = tl + tm; mm[2] = f
    mm[1] = min(mm[1], min(tl, tm))
print("(nu, b = odd kernel dim, c, t, grid): count, example")
for k, v in sorted(tab.items(), key=lambda kv: (-kv[0][0], -kv[0][1], kv[0][3])):
    print("  ", k, v, ex[k])
print("per (nu, b): min t(l)+t(m), min of min(t), example of the min sum")
for k, v in sorted(mins.items(), key=lambda kv: (-kv[0][0], -kv[0][1])):
    print("  ", k, v)
