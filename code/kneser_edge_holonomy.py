"""notes/103: Hamming point x.  At a Kneser edge (P, P') the three triangle holonomies theta_R (R in the 3 class pairs
disjoint from P u P') satisfy  sum_R Perm(theta_R) = 2J - I - Sib_P - Sib'  (SRG condition on the (P,P') block).
A-edge (phi preserves antipodal pairs):  target I + 2 iota.   Non-A edge: target I + M_c + M_A (move to the pi_c partner
or to the antipode, never to the pi_c' partner).  Enumerate all ordered triples in S_4 and list conjugacy-class multisets."""
import itertools
from collections import Counter

pts = [(0, 0), (0, 1), (1, 0), (1, 1)]
idx = {p: k for k, p in enumerate(pts)}
iota = lambda p: (1 - p[0], 1 - p[1])
m_i = lambda p: (p[0], 1 - p[1])        # partner with the same class-i label (pi_i matching)
m_j = lambda p: (1 - p[0], p[1])        # partner with the same class-j label


def perm_matrix(perm):
    M = [[0] * 4 for _ in range(4)]
    for a in range(4):
        M[a][perm[a]] = 1
    return M


def mat_of(f):
    M = [[0] * 4 for _ in range(4)]
    for p in pts:
        M[idx[p]][idx[f(p)]] += 1
    return M


def add(*Ms):
    return [[sum(M[r][c] for M in Ms) for c in range(4)] for r in range(4)]


def ctype(perm):
    seen, cyc = set(), []
    for a in range(4):
        if a in seen:
            continue
        l, b = 0, a
        while b not in seen:
            seen.add(b); b = perm[b]; l += 1
        cyc.append(l)
    return {(1, 1, 1, 1): 'id', (1, 1, 2): 'tr', (2, 2): 'dt', (1, 3): '3c', (4,): '4c'}[tuple(sorted(cyc))]


I = mat_of(lambda p: p)
targets = {'A-edge  (I + 2 iota)': add(I, mat_of(iota), mat_of(iota)),
           'non-A edge (I + M_c + M_A), c = i': add(I, mat_of(m_i), mat_of(iota))}
S4 = list(itertools.permutations(range(4)))
for name, T in targets.items():
    found = Counter()
    for tri in itertools.combinations_with_replacement(S4, 3):
        if add(*(perm_matrix(t) for t in tri)) == T:
            found[tuple(sorted(ctype(t) for t in tri))] += 1
    print(name, '->', dict(found))
