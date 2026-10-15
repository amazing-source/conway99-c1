"""(KER-SYM-13) over a corpus (LAB 15/10/2026): for every distinct T, U PSD structure of nullity >= NUMIN (default 13),
is ker T invariant under h p for SOME involution p of the outer letters (all 9 496, mate-preserving or not)?
p = id is tested first.  Reports (nu, best dim(N n gN), invariant?, kind of p) and examples.
usage: python kersym13_scan.py <dir or json> [...]"""
import glob, json, os, sys
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stars_rank import kval, LABELS
OUT = list(range(4, 14))


def involutions(elems):
    # all involutions of a finite set (identity first), as dicts
    if not elems:
        yield {}
        return
    a, rest = elems[0], elems[1:]
    for inv in involutions(rest):
        d = dict(inv); d[a] = a
        yield d
    for k, b in enumerate(rest):
        rest2 = rest[:k] + rest[k + 1:]
        for inv in involutions(rest2):
            d = dict(inv); d[a] = b; d[b] = a
            yield d
INVS = list(involutions(OUT))
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
seen = set(); tab = Counter(); ex = {}
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
    w, V = np.linalg.eigh(T)
    N = V[:, np.abs(w) < 1e-8]; nu = N.shape[1]
    if nu < numin:
        continue
    Z = np.array([[1.0 if y in s_ else 0.0 for s_ in S] for y in (0, 1, 2, 3)]).T
    Q, _ = np.linalg.qr(Z); P = np.eye(n) - Q @ Q.T
    if np.linalg.eigvalsh(P @ T @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    U = 7 * Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])] - T
    if np.linalg.eigvalsh(P @ U @ P + 50 * Q @ Q.T)[0] < -1e-9:
        continue
    best = (-1, None, None)
    for p in INVS:                                    # INVS[0] is the identity
        g = {0: 1, 1: 0, 2: 3, 3: 2}; g.update(p)
        perm = [idx[frozenset(g[t] for t in s)] for s in S]
        inter = 2 * nu - int(np.sum(np.linalg.svd(np.hstack([N, N[perm, :]]), compute_uv=False) > 1e-7))
        moved = tuple(x for x in OUT if p[x] != x)
        if inter > best[0] or (inter == best[0] and len(moved) < len(best[1])):
            best = (inter, moved, p)
        if inter == nu and not moved:
            break
    inter, moved, pbest = best
    if not moved:
        kind = "p = id"
    else:
        kind = "true (mate-preserving)" if all(pbest[x ^ 1] == pbest[x] ^ 1 for x in OUT) else "fake"
    hinv = bool(np.array_equal(G[np.ix_([idx[frozenset({0: 1, 1: 0, 2: 3, 3: 2}.get(y, y) for y in s)] for s in S],
                                        [idx[frozenset({0: 1, 1: 0, 2: 3, 3: 2}.get(y, y) for y in s)] for s in S])], G))
    k = (nu, inter == nu, kind if inter == nu else "best dim(N n gN) = %d" % inter, "structure h-inv" if hinv else "structure not h-inv")
    tab[k] += 1; ex.setdefault(k, f)
print("(nu, kernel invariant under some h p, kind of p, structure h-invariant?): count, example")
for k, v in sorted(tab.items(), key=lambda kv: (-kv[0][0], kv[0][1], -kv[1])):
    print("  ", k, v, ex[k])
