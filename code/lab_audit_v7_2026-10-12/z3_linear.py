"""Lab session, 2026-10-12. The Z3-covers of the Brouwer-Haemers graph BH = srg(81,20,1,6) that are srg(243,22,1,2):
how large is the LINEAR part of the problem?  (New fact used: Codex's exact formulation of 12/10 - for a cover with
gains t -> t + b_xy, b in F_3, the conditions are: (T) b_xy + b_yz + b_zx = 0 on every line of BH; (L) for every
non-adjacent pair P, R, the six values c_Z = b_PZ + b_ZR over the common neighbours Z satisfy sum c = 0 AND
sum c^2 = 1 modulo 3, and these two moments are equivalent to "0, 1, 2 twice each".)

The script
 1. takes a srg(243,22,1,2) given as an edge list, finds a regular spread and the quotient BH;
 2. reads off the gains b of this cover (fibres oriented by propagation; the script stops if the cover is not a
    Z3-cover in this gauge) and checks (T), the first and the second moments on it: positive control of the formulation;
 3. computes over F_3 the dimension of { b : (T) and all first moments } and of the gauge space { b_xy = a_y - a_x },
    i.e. the number of free parameters left for the quadratic conditions.
If that number is small, ALL Z3-covers of BH can be listed by brute force on the quadratic conditions.

python z3_linear.py <file.edges> [index of the spread, default 0]        One process, below 1 GB."""
import sys, itertools, time
import numpy as np
n = 243

def load(path):
    A = np.zeros((n, n), dtype=np.int64)
    for line in open(path):
        if line.strip():
            i, j = map(int, line.split()); A[i, j] = A[j, i] = 1
    return A

def spreads(A):
    adj = [set(int(y) for y in np.nonzero(A[x])[0]) for x in range(n)]
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x]})
    out = []
    for l0 in [l for l in lines if 0 in l]:
        lineof = {p: l0 for p in l0}; queue = [l0]; good = True
        while queue and good:
            l = queue.pop()
            for a in l:
                others = [p for p in l if p != a]
                for x in adj[a]:
                    if x in l: continue
                    ys = []
                    for b in others:
                        cn = (adj[x] & adj[b]) - {a}
                        if len(cn) != 1: good = False; break
                        ys.append(next(iter(cn)))
                    if not good: break
                    cand = tuple(sorted([x] + ys))
                    if len(set(cand)) != 3 or ys[1] not in adj[ys[0]] or any(p in lineof and lineof[p] != cand for p in cand): good = False; break
                    if x not in lineof:
                        for p in cand: lineof[p] = cand
                        queue.append(cand)
                if not good: break
        if good and len(lineof) == n and len(set(lineof.values())) == 81: out.append(sorted(set(lineof.values())))
    return out, adj

def rank_mod3(M):
    M = M.copy() % 3; r = 0; rows, cols = M.shape
    for c in range(cols):
        p = np.nonzero(M[r:, c])[0]
        if len(p) == 0: continue
        p = p[0] + r
        if p != r: M[[r, p]] = M[[p, r]]
        if M[r, c] == 2: M[r] = (2 * M[r]) % 3
        nz = np.nonzero(M[:, c])[0]
        for q in nz:
            if q != r: M[q] = (M[q] - M[q, c] * M[r]) % 3
        r += 1
        if r == rows: break
    return r

def main():
    A = load(sys.argv[1]); which = int(sys.argv[2]) if len(sys.argv) > 2 else 0; t0 = time.time()
    S, adj = spreads(A); print("regular spreads found: %d; using number %d" % (len(S), which)); F = S[which]
    fib = {}
    for i, l in enumerate(F):
        for p in l: fib[p] = i
    Q = np.zeros((81, 81), dtype=np.int64)
    for i, l1 in enumerate(F):
        for l2 in F[i + 1:]:
            if A[np.ix_(l1, l2)].sum() == 3: Q[i, fib[l2[0]]] = Q[fib[l2[0]], i] = 1
    assert (Q @ Q + 5 * Q == 14 * np.eye(81, dtype=np.int64) + 6).all(), "quotient is not srg(81,20,1,6)"
    nb = [[int(j) for j in np.nonzero(Q[i])[0]] for i in range(81)]
    # orient the fibres: lab[p] in {0,1,2}; propagate so that every matching is a translation
    lab = {};
    for t, p in enumerate(F[0]): lab[p] = t
    seen = {0}; stack = [0]
    def match(i, j): return {p: next(q for q in F[j] if A[p, q]) for p in F[i]}
    while stack:
        i = stack.pop()
        for j in nb[i]:
            if j in seen: continue
            m = match(i, j)
            for p in F[i]: lab[m[p]] = lab[p]                       # gain 0 on the tree edges
            seen.add(j); stack.append(j)
    b = {}; z3 = True
    for i in range(81):
        for j in nb[i]:
            m = match(i, j); d = {(lab[m[p]] - lab[p]) % 3 for p in F[i]}
            if len(d) != 1: z3 = False
            b[(i, j)] = d.pop()
    print("the cover is a Z3-cover in the tree gauge (every matching a translation): %s" % z3)
    edges = [(i, j) for i in range(81) for j in nb[i] if i < j]; eidx = {e: k for k, e in enumerate(edges)}
    def coef(i, j): return (eidx[(i, j)], 1) if i < j else (eidx[(j, i)], 2)      # b_ji = -b_ij
    rows = []
    tri = sorted({tuple(sorted((i, j, k))) for i in range(81) for j in nb[i] for k in nb[i] if j < k and Q[j, k]})
    for i, j, k in tri:
        r = np.zeros(len(edges), dtype=np.int64)
        for u, v in ((i, j), (j, k), (k, i)):
            e, c = coef(u, v); r[e] = (r[e] + c) % 3
        rows.append(r)
    nT = len(rows)
    pairs = [(P, R) for P in range(81) for R in range(P + 1, 81) if not Q[P, R]]
    for P, R in pairs:
        r = np.zeros(len(edges), dtype=np.int64)
        for Z in range(81):
            if Q[P, Z] and Q[Z, R]:
                for u, v in ((P, Z), (Z, R)):
                    e, c = coef(u, v); r[e] = (r[e] + c) % 3
        rows.append(r)
    M = np.array(rows)
    if z3:
        bv = np.array([b[e] for e in edges])
        okT = not ((M[:nT] @ bv) % 3).any(); ok1 = not ((M[nT:] @ bv) % 3).any()
        m2 = [sum(((b[(P, Z)] + b[(Z, R)]) % 3) ** 2 for Z in range(81) if Q[P, Z] and Q[Z, R]) % 3 for P, R in pairs]
        multis = {tuple(sorted((b[(P, Z)] + b[(Z, R)]) % 3 for Z in range(81) if Q[P, Z] and Q[Z, R])) for P, R in pairs}
        print("positive control on this cover: lines %s, first moments %s, second moments all equal to 1: %s; multisets met: %s" % (okT, ok1, set(m2) == {1}, sorted(multis)))
    G = np.zeros((81, len(edges)), dtype=np.int64)
    for k, (i, j) in enumerate(edges): G[j, k] = 1; G[i, k] = 2
    rT = rank_mod3(M[:nT]); rM = rank_mod3(M); rG = rank_mod3(G)
    print("BH: %d edges, %d lines, %d non-adjacent pairs" % (len(edges), nT, len(pairs)))
    print("rank over F_3: line equations %d; line equations + first moments %d; gauge space %d" % (rT, rM, rG))
    print("solutions of the linear part: dimension %d; modulo the gauge: %d free parameters for the %d quadratic conditions  [%.0f s]" % (
        len(edges) - rM, len(edges) - rM - rG, len(pairs), time.time() - t0))

if __name__ == "__main__":
    main()
