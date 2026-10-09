"""C1, lab session, 2026-10-10. Pilot: rank 37 against a norm-14 eigenvector, with a rigid basis instead of a line ball.

Rank 37 means: the Seidel matrix S = J - I - 2A has rank 36 modulo 7, so the vertices are isotropic vectors of a
36-dimensional space W with product -1 on edges and +1 on non-edges (NOTE 17.92 A). Any vertex set whose Seidel
submatrix has rank 36 is a basis of W; every other vertex is then determined by its adjacencies to that set.

World of a norm-14 eigenvector 1_X - 1_Y (hand, NOTE 17.90): X, Y two 7-sets with the biplane between them
(x ~ y iff the point x is not on the Fano line y); 70 boundary vertices, each adjacent to one x and one y (one for an
adjacent pair (x, y), two for a non-adjacent pair); 15 far vertices, pairwise non-adjacent, with no neighbour in
X + Y; every boundary vertex has 3 far neighbours; for each core point the far vertices are the 15 edges of a simple
cubic graph on its 10 boundary neighbours.

BASE (39 vertices, all adjacencies known): X + Y + far + the ten boundary neighbours B0 of x_0, i.e. a cubic graph
on B0 avoiding six pairs (the three lines through x_0 among the six "flag" neighbours and the three pairs of twins).
Three relations hold automatically, so the base has Seidel rank at most 36; when it is 36 the base is a basis of W.
TEST: the ten boundary neighbours B1 of x_1. Their labels and mutual adjacency are known; a candidate for a member is
(3 far neighbours, 1 or 2 neighbours in B0); it must be isotropic, the 45 products must be the prescribed ones, each
far vertex lies in exactly two of the ten triples and each vertex of B0 has its prescribed number of neighbours in B1.

python fano37_pilot.py <seed> <number of random bases> [node cap per base]
One process, below 1 GB. Random bases (not an exhaustive enumeration): this is a measurement of the method."""
import sys, os, itertools, random, time
import numpy as np

P7 = 7
NOGRAM = os.environ.get('FANO37_NOGRAM') is not None      # control: the 45 products are not tested; a complete cell must then exist
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
INC = [[x not in LINES[y] for y in range(7)] for x in range(7)]            # x_x ~ y_y

def inv_mod(M):
    """inverse of a square matrix modulo 7 (None if singular) and its determinant"""
    n = len(M); A = [[int(v) % P7 for v in row] + [int(i == j) for j in range(n)] for i, row in enumerate(M)]; det = 1
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c]), None)
        if p is None: return None, 0
        if p != c: A[c], A[p] = A[p], A[c]; det = -det
        det = det * A[c][c] % P7; iv = pow(A[c][c], P7 - 2, P7); A[c] = [v * iv % P7 for v in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                f = A[r][c]; A[r] = [(a - f * b) % P7 for a, b in zip(A[r], A[c])]
    return np.array([row[n:] for row in A], dtype=np.int64), det % P7

def independent_rows(K):
    """indices of a maximal set of linearly independent rows of K modulo 7"""
    rows = []; basis = []
    for i in range(len(K)):
        v = [int(x) % P7 for x in K[i]]
        for piv, b in basis:
            if v[piv]:
                f = v[piv]; v = [(a - f * c) % P7 for a, c in zip(v, b)]
        piv = next((j for j, x in enumerate(v) if x), None)
        if piv is None: continue
        iv = pow(v[piv], P7 - 2, P7); v = [x * iv % P7 for x in v]
        basis.append((piv, v)); rows.append(i)
    return rows

def cell(point):
    """the ten boundary neighbours of x_point: (line j, twin s); first the four on a line x y e, then the six flags"""
    return [(j, 0) for j in range(7) if point not in LINES[j]] + [(j, s) for j in range(7) if point in LINES[j] for s in (0, 1)]

def flag_lines():
    """the three lines through the core point among its six flag neighbours (positions 4..9), one fixed choice"""
    return [(4, 6), (5, 8), (7, 9)]

def random_cubic(rng, forbidden):
    """a random simple cubic graph on 10 vertices avoiding the forbidden pairs: list of 15 edges"""
    while True:
        stubs = [v for v in range(10) for _ in range(3)]; rng.shuffle(stubs)
        E = set(); ok = True
        for a, b in zip(stubs[0::2], stubs[1::2]):
            e = (min(a, b), max(a, b))
            if a == b or e in E or e in forbidden: ok = False; break
            E.add(e)
        if ok: return sorted(E)

def run(seed, nbases, cap):
    rng = random.Random(seed)
    B0 = cell(0); B1 = cell(1); FL = flag_lines()
    forb = set(FL) | {(4, 5), (6, 7), (8, 9)}
    IX = lambda i: i; IY = lambda j: 7 + j; IF = lambda k: 14 + k; IB = lambda t: 29 + t
    quota1 = [1 + (0 in LINES[j]) for j, s in B1]            # neighbours in B0 of a member of B1
    quota0 = [1 + (1 in LINES[j]) for j, s in B0]            # neighbours in B1 of a vertex of B0
    adj1 = np.zeros((10, 10), dtype=np.int64)
    for a, b in FL: adj1[a][b] = adj1[b][a] = 1
    triples = list(itertools.combinations(range(15), 3))
    tmask = np.array([sum(1 << k for k in t) for t in triples], dtype=np.int64)
    pop = np.array([bin(i).count("1") for i in range(1 << 15)], dtype=np.int64)
    stats = dict(bases=0, rank36=0, sign_ok=0, dead=0, alive=0, capped=0)
    tot_nodes = 0; depth_hist = {}; cand_sizes = []; lvl_sum = np.zeros(11); t0 = time.time(); rank_hist = {}
    for _ in range(nbases):
        C = random_cubic(rng, forb); stats["bases"] += 1
        A = np.zeros((39, 39), dtype=np.int64)
        for x in range(7):
            for y in range(7):
                if INC[x][y]: A[IX(x)][IY(y)] = A[IY(y)][IX(x)] = 1
        for t, (j, s) in enumerate(B0):
            A[IB(t)][IX(0)] = A[IX(0)][IB(t)] = 1; A[IB(t)][IY(j)] = A[IY(j)][IB(t)] = 1
        for a, b in FL: A[IB(a)][IB(b)] = A[IB(b)][IB(a)] = 1
        blk0 = [0] * 10
        for k, (a, b) in enumerate(C):
            A[IF(k)][IB(a)] = A[IB(a)][IF(k)] = 1; A[IF(k)][IB(b)] = A[IB(b)][IF(k)] = 1
            blk0[a] |= 1 << k; blk0[b] |= 1 << k
        K = (1 - np.eye(39, dtype=np.int64) - 2 * A) % P7
        I = independent_rows(K)
        rank_hist[len(I)] = rank_hist.get(len(I), 0) + 1
        if len(I) != 36: continue
        stats["rank36"] += 1
        Kinv, det = inv_mod(K[np.ix_(I, I)])
        if det in (1, 2, 4): continue                         # the discriminant of W is a non-residue (L23)
        stats["sign_ok"] += 1
        ends = C                                              # far vertex k is adjacent to ends[k] in B0
        # candidates of each member of B1
        cands = []
        for m, (j, s) in enumerate(B1):
            q = quota1[m]; pats = []
            for Pset in itertools.combinations(range(10), q):
                if any(B0[t][0] == j and j != 0 for t in Pset): continue          # same line label: adjacent only for the flags of line 0
                if q == 2:
                    a, b = Pset
                    if (a, b) in forb or blk0[a] & blk0[b]: continue              # the two neighbours: non-adjacent, not twins, no common far vertex
                    if B0[a][0] == B0[b][0]: continue
                pats.append(Pset)
            rows = []
            for Pset in pats:
                pm = sum(1 << t for t in Pset)
                ok = np.ones(len(triples), dtype=bool)
                for t in range(10):
                    same = int(B0[t][0] == j); c = pop[tmask & blk0[t]]
                    ok &= (same + c <= (1 if t in Pset else 2))
                for k in range(15):                           # a far neighbour has exactly one common neighbour with the member
                    e = (1 << ends[k][0]) | (1 << ends[k][1])
                    if bin(pm & e).count("1") == 2: ok &= ((tmask >> k) & 1) == 0
                base = np.zeros(39, dtype=np.int64); base[IX(1)] = 1; base[IY(j)] = 1
                for t in Pset: base[IB(t)] = 1
                for ti in np.nonzero(ok)[0]:
                    a = base.copy()
                    for k in triples[ti]: a[IF(k)] = 1
                    rows.append((1 - 2 * a[I], int(tmask[ti]), pm))
            if not rows: cands.append((np.zeros((0, 36), dtype=np.int64), np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.int64))); continue
            Sv = np.array([r[0] for r in rows], dtype=np.int64) % P7
            Q = np.einsum("ij,jk,ik->i", Sv, Kinv, Sv) % P7
            keep = Q == 0
            cands.append((Sv[keep], np.array([r[1] for r in rows], dtype=np.int64)[keep], np.array([r[2] for r in rows], dtype=np.int64)[keep]))
        sizes = [len(c[0]) for c in cands]; cand_sizes.append(sizes)
        order = sorted(range(10), key=lambda m: sizes[m])
        # compatibility of candidates of two members
        comp = {}
        for x in range(10):
            for y in range(x + 1, 10):
                a, b = order[x], order[y]
                if sizes[a] == 0 or sizes[b] == 0: comp[(x, y)] = np.zeros((sizes[a], sizes[b]), dtype=bool); continue
                G = (cands[a][0] @ Kinv @ cands[b][0].T) % P7
                want = 6 if adj1[a][b] else 1
                fi = pop[cands[a][1][:, None] & cands[b][1][None, :]]
                pi = pop[cands[a][2][:, None] & cands[b][2][None, :]]
                twins = (B1[a][0] == B1[b][0])
                lim = 0 if (adj1[a][b] or twins) else 1
                comp[(x, y)] = ((G == want) | NOGRAM) & (fi + pi <= lim)
        # search: exact covers of the far vertices (twice each) and of B0 (quota0)
        nodes = 0; best = 0; found = 0; lvl = [0] * 11
        alive0 = [np.ones(sizes[order[x]], dtype=bool) for x in range(10)]
        def rec(x, alive, fcnt, bcnt):
            nonlocal nodes, best, found
            if nodes > cap or (NOGRAM and found): return
            if x == 10:
                if all(c == 2 for c in fcnt) and all(bcnt[t] == quota0[t] for t in range(10)): found += 1
                return
            m = order[x]; idx = np.nonzero(alive[x])[0]
            for i in idx:
                nodes += 1; lvl[x + 1] += 1
                if x + 1 > best: best = x + 1
                fm = int(cands[m][1][i]); pm = int(cands[m][2][i])
                f2 = list(fcnt); b2 = list(bcnt); ok = True
                for k in range(15):
                    if (fm >> k) & 1:
                        f2[k] += 1
                        if f2[k] > 2: ok = False
                for t in range(10):
                    if (pm >> t) & 1:
                        b2[t] += 1
                        if b2[t] > quota0[t]: ok = False
                if not ok: continue
                fullf = sum(1 << k for k in range(15) if f2[k] == 2); fullb = sum(1 << t for t in range(10) if b2[t] == quota0[t])
                new = list(alive)
                dead = False
                for y in range(x + 1, 10):
                    my = order[y]
                    a = alive[y] & comp[(x, y)][i] & ((cands[my][1] & fullf) == 0) & ((cands[my][2] & fullb) == 0)
                    if not a.any(): dead = True; break
                    new[y] = a
                if dead: continue
                rec(x + 1, new, f2, b2)
                if nodes > cap: return
        if min(sizes) > 0: rec(0, alive0, [0] * 15, [0] * 10)
        tot_nodes += nodes; depth_hist[best] = depth_hist.get(best, 0) + 1; lvl_sum += np.array(lvl)
        if nodes > cap: stats["capped"] += 1
        elif found: stats["alive"] += 1
        else: stats["dead"] += 1
    n = max(1, stats["sign_ok"])
    print("random bases %d; Seidel rank 36: %d; discriminant a non-residue: %d" % (stats["bases"], stats["rank36"], stats["sign_ok"]))
    print("Seidel rank of the 39-vertex base, histogram:", sorted(rank_hist.items()))
    if cand_sizes:
        cs = np.array(cand_sizes); print("isotropic candidates per member (mean over the bases tested), members in the order of cell(1):", " ".join("%.0f" % v for v in cs.mean(axis=0)))
    print("bases with a complete cell: %d; dead: %d; stopped at the node cap %d: %d" % (stats["alive"], stats["dead"], cap, stats["capped"]))
    print("nodes per base tested: %.0f; mean nodes by depth:" % (tot_nodes / n), " ".join("%.1f" % (v / n) for v in lvl_sum[1:]))
    print("bases by deepest partial cell:", sorted(depth_hist.items()), " [%.0f s]" % (time.time() - t0))

if __name__ == "__main__":
    run(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 200000)
