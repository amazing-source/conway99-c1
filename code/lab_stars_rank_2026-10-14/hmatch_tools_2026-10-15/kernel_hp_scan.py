"""Is the KERNEL invariant under some h-type involution g = h p? (LAB 15/10/2026, mechanism A)
For each structure: N = ker T (numerical, eigenvalues < 1e-8); candidates p = permutations of the outer letters with
M_1 = s_m p(M_0) and M_3 = s_l p(M_2) (matching-level relations, h itself = p = id included when it applies), plus p = id
always; for each, dim(N n gN) (SVD rank).  Reports the best candidate, whether N = gN, whether p is an involution and
mate-preserving (true symmetry) or not (fake), and whether the whole structure is g-invariant.
usage: python kernel_hp_scan.py <json> [...]"""
import itertools, json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, '.')
from stars_rank import kval

OUT = list(range(4, 14))
tab = Counter()
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]; n = len(S); idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n))
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    K = np.array([[float(kval(a, b)) for b in S] for a in S])
    T = 3 * np.eye(n) - G - K
    w, V = np.linalg.eigh(T)
    Nb = V[:, np.abs(w) < 1e-8]
    nu = Nb.shape[1]
    M = {}
    for a in range(4):
        part = {}
        for i in range(n):
            if a in S[i]:
                for j in range(n):
                    if j != i and a in S[j] and G[i, j]:
                        part[[t for t in S[i] if t != a][0]] = [t for t in S[j] if t != a][0]
        M[a] = part
    sw = {2: 3, 3: 2, 0: 1, 1: 0}
    B0 = {x: sw.get(M[1][sw.get(x, x)], M[1][sw.get(x, x)]) for x in M[1]}
    B2 = {x: sw.get(M[3][sw.get(x, x)], M[3][sw.get(x, x)]) for x in M[3]}
    cands = [tuple(OUT)]
    pm = {x: x for x in range(4)}

    def rec(k, used):
        if len(cands) > 300:
            return
        if k == len(OUT):
            cands.append(tuple(pm[x] for x in OUT))
            return
        x = OUT[k]
        for t in OUT:
            if t in used:
                continue
            pm[x] = t
            ok = True
            for Am, Bm in ((M[0], B0), (M[2], B2)):
                for u in list(pm):
                    y = Am.get(u)
                    if y is not None and y in pm and Bm.get(pm[u]) != pm[y]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                rec(k + 1, used | {t})
            del pm[x]
    rec(0, set())
    best = None
    for c in set(cands):
        g = {0: 1, 1: 0, 2: 3, 3: 2}
        g.update(dict(zip(OUT, c)))
        perm = [idx[frozenset(g[t] for t in S[i])] for i in range(n)]
        gN = Nb[np.argsort(perm), :]          # (g n)(x) = n(g^-1 x)
        sv = np.linalg.svd(np.hstack([Nb, gN]), compute_uv=False)
        inter = 2 * nu - int(np.sum(sv > 1e-7))
        moved = tuple(x for x, t in zip(OUT, c) if x != t)
        inv = all(dict(zip(OUT, c))[dict(zip(OUT, c))[x]] == x for x in OUT)
        mate = all(dict(zip(OUT, c))[x ^ 1] == dict(zip(OUT, c))[x] ^ 1 for x in OUT)
        whole = bool(np.array_equal(G[np.ix_(perm, perm)], G))
        key = (inter, -len(moved))
        if best is None or key > best[0]:
            best = (key, moved, inv, mate, whole)
    (inter, _), moved, inv, mate, whole = best
    tab[(nu, inter == nu, "p moves %s" % (moved,) if moved else "p = id (h)", "involution" if inv else "not inv",
         "true" if mate else "fake", "structure g-inv" if whole else "structure not g-inv")] += 1
print("(nu, kernel g-invariant for the best h p, p, involution?, true/fake, structure g-invariant?): count")
for k, v in sorted(tab.items(), key=lambda kv: -kv[1]):
    print("  ", k, v)
