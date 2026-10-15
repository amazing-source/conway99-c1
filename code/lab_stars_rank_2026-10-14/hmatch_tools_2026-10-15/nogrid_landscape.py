"""Non-grid PSD landscape (LAB 15/10/2026 evening, (NG14) campaign).  For every distinct T, U PSD structure of a corpus:
grid on (l, m) or not, nullity, t, spectral c, file family (prefix before the first '_' digit block).  Prints, for the
non-grid ones, the maximal nullity per family and the full (nu, c, t) table.
usage: python nogrid_landscape.py <dir or json> [...]   (FLAT=1: no recursion)"""
import glob, json, os, re, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from stars_rank import kval, LABELS
D84 = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D84[y, j] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: i for i, l in enumerate(LABELS)}
files = []
for a in sys.argv[1:]:
    if os.path.isdir(a):
        files += sorted(glob.glob(os.path.join(a, "*.json"))) if os.environ.get("FLAT") else sorted(glob.glob(os.path.join(a, "**", "*.json"), recursive=True))
    else:
        files.append(a)
seen = set(); tab = Counter(); fam = defaultdict(lambda: [0, None]); ex = {}
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
    grid = all(G[idx[frozenset(p)], idx[frozenset(q)]] for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))))
    if grid:
        continue
    K = np.array([[kval(a, b) for b in S] for a in S]); T = 3 * np.eye(n) - G - K
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    U = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ U @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    nu = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-7))
    tl = sum(1 for x in range(2, 14) if G[idx[frozenset((0, x))], idx[frozenset((1, x))]])
    tm = sum(1 for x in [0, 1] + list(range(4, 14)) if G[idx[frozenset((2, x))], idx[frozenset((3, x))]])
    def cc(a0, a1):
        X = [i for i in range(n) if S[i] & {a0, a1}]
        return 23 - int(np.sum(np.abs(np.linalg.eigvalsh(T[np.ix_(X, X)])) > 1e-7))
    sq = sum(1 for p, q in (((0, 2), (0, 3)), ((1, 2), (1, 3)), ((0, 2), (1, 2)), ((0, 3), (1, 3))) if G[idx[frozenset(p)], idx[frozenset(q)]])
    family = re.split(r"_(?:[A-Z]|\d)", os.path.basename(f))[0]
    k = (nu, (cc(0, 1), cc(2, 3)), (tl, tm), "square edges %d/4" % sq)
    tab[k] += 1; ex.setdefault(k, f)
    if nu > fam[family][0]:
        fam[family] = [nu, f]
print("NON-GRID T, U PSD structures (distinct): %d" % sum(tab.values()))
for k, v in sorted(tab.items(), key=lambda kv: (-kv[0][0], -kv[1]))[:40]:
    print("  ", k, v, ex[k])
print("max nullity per family (non-grid):")
for k, v in sorted(fam.items(), key=lambda kv: -kv[1][0]):
    print("  ", k, v)
