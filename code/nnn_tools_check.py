"""notes/103 §13 checks.
(1) H^1 = 0 (F_2) for the triangle complexes of K(7,2) and K(6,2).
(2) NNN triangle rule: with all three edges non-isometric, the S_3-holonomy is a 3-cycle iff exactly two
    vertices receive concordantly (kappa(X->Y) = kappa(Z->Y)).
(3) Spectral lemma, local form: for every admissible star (G_P connected with an even number of edges, or
    empty), lambda_min of the cone over Petersen[I_P] (I_P = K5 - G_P), which is forced balanced."""
import itertools
import numpy as np

def rank_f2(rows, ncols):
    rows = [int(''.join('1' if c else '0' for c in r), 2) for r in rows]
    rank = 0
    piv_rows = []
    for r in rows:
        for p in piv_rows:
            r = min(r, r ^ p)
        if r:
            piv_rows.append(r)
            rank += 1
    return rank

def h1_triangle_complex(n):
    pairs = list(itertools.combinations(range(n), 2))
    edges = [(P, R) for P, R in itertools.combinations(pairs, 2) if not set(P) & set(R)]
    eid = {e: k for k, e in enumerate(edges)}
    eid.update({(R, P): k for (P, R), k in list(eid.items())})
    tris = [t for t in itertools.combinations(pairs, 3)
            if all(not set(a) & set(b) for a, b in itertools.combinations(t, 2))]
    rows = []
    for t in tris:
        r = [0] * len(edges)
        for a, b in itertools.combinations(t, 2):
            r[eid[(a, b)]] = 1
        rows.append(r)
    rk = rank_f2(rows, len(edges))
    dimZ1 = len(edges) - rk            # cocycles
    dimB1 = len(pairs) - 1             # coboundaries (connected)
    return len(pairs), len(edges), len(tris), dimZ1 - dimB1

for n in (7, 6):
    print('K(%d,2): vertices %d, edges %d, triangles %d, dim H^1(F_2) = %d' % ((n,) + h1_triangle_complex(n)[:3] + (h1_triangle_complex(n)[3],)))

# (2) NNN triangle rule, via the explicit bijections of partitions
def holonomy_is_3cycle(kap):
    """kap[(X,Y)] in Y = kappa(X->Y) for the 3 vertices X,Y,Z = 0,1,2, each vertex is a 2-set of classes.
    parts(V) = {'A'} u {('pi', c) : c in V}.  beta_{XY}: A_X -> pi_{kap(X,Y)}, pi_{kap(Y,X)} -> A_Y,
    other label -> other label."""
    V = {0: ('a', 'b'), 1: ('c', 'd'), 2: ('e', 'f')}
    def beta(X, Y, part):
        kxy, kyx = kap[(X, Y)], kap[(Y, X)]
        if part == 'A':
            return ('pi', kxy)
        if part == ('pi', kyx):
            return 'A'
        other_y = [c for c in V[Y] if c != kxy][0]
        return ('pi', other_y)
    parts0 = ['A', ('pi', 'a'), ('pi', 'b')]
    img = [beta(2, 0, beta(1, 2, beta(0, 1, p))) for p in parts0]
    perm = [parts0.index(q) for q in img]
    fixed = sum(1 for i in range(3) if perm[i] == i)
    return fixed == 0
V = {0: ('a', 'b'), 1: ('c', 'd'), 2: ('e', 'f')}
bad = 0
for choice in itertools.product(*[V[Y] for (X, Y) in [(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)]]):
    kap = dict(zip([(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)], choice))
    conc = [kap[(1, 0)] == kap[(2, 0)], kap[(0, 1)] == kap[(2, 1)], kap[(0, 2)] == kap[(1, 2)]]
    if holonomy_is_3cycle(kap) != (sum(conc) == 2):
        bad += 1
print('NNN rule (3-cycle <=> exactly two concordant vertices): %d exceptions over 64 kappa patterns' % bad)

# (3) local spectral test
K5 = list(itertools.combinations(range(5), 2))
def connected_even(G):
    if not G:
        return True
    if len(G) % 2:
        return False
    verts = set(v for e in G for v in e)
    seen = {next(iter(verts))}
    ch = True
    while ch:
        ch = False
        for u, v in G:
            if (u in seen) != (v in seen):
                seen |= {u, v}
                ch = True
    return seen == verts
seen_types = {}
for mask in range(1 << 10):
    G = [K5[b] for b in range(10) if mask >> b & 1]
    if not connected_even(G):
        continue
    I = [e for e in K5 if e not in G]
    n = len(I) + 1
    Mx = np.zeros((n, n))
    for a in range(len(I)):
        Mx[0, a + 1] = Mx[a + 1, 0] = 1
        for b in range(len(I)):
            if not set(I[a]) & set(I[b]):
                Mx[a + 1, b + 1] = 1
    lam = np.linalg.eigvalsh(Mx)
    key = (len(G), tuple(sorted(sum(1 for e in G if v in e) for v in range(5))))
    seen_types.setdefault(key, set()).add(round(lam[0], 6))
for key in sorted(seen_types):
    print('|G_P| = %2d, degree sequence %s : lambda_min(cone) = %s' % (key[0], key[1], sorted(seen_types[key])))
