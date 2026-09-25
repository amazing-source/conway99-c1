"""notes/104 §6: the line skeleton at a Hamming point.
Each y in Q_P lies on 5 lines inside Gamma_2(x); they sit over 5 Kneser triangles through P that form a
perfect matching of the Petersen graph link(P).  l(t) = number of lines over the Kneser triangle t
= |Fix(holonomy)| in {0, 2, 4}.  The 4 matchings F(y), y in Q_P, cover each Petersen edge l(t) times (even),
hence (6 perfect matchings = vertices of K6, edges = pairs of them) the multiset is {M,M,M,M} (pattern A)
or {M,M,M',M'} (pattern B: l = 4 on the common edge t0, 2 on the other 8 edges of M u M', 0 elsewhere).
Question: which functions l on the 105 Kneser triangles are consistent with a pattern at every pair P?"""
import itertools, sys

pairs = list(itertools.combinations(range(7), 2))
pid = {P: n for n, P in enumerate(pairs)}
def disjoint(a, b): return not set(a) & set(b)
tris = [t for t in itertools.combinations(range(21), 3)
        if all(disjoint(pairs[a], pairs[b]) for a, b in itertools.combinations(t, 2))]
tid = {t: n for n, t in enumerate(tris)}
tris_at = [[n for n, t in enumerate(tris) if P in t] for P in range(21)]

def petersen_matchings(P):
    """perfect matchings of the Petersen graph on link(P), as sets of triangle ids through P"""
    link = [R for R in range(21) if disjoint(pairs[R], pairs[P])]
    pet_edges = [(R, S) for R, S in itertools.combinations(link, 2) if disjoint(pairs[R], pairs[S])]
    out = []
    for combo in itertools.combinations(pet_edges, 5):
        cov = [v for e in combo for v in e]
        if len(set(cov)) == 10:
            out.append(frozenset(tid[tuple(sorted((P, R, S)))] for R, S in combo))
    return out

options = []          # per P: list of dicts triangle -> l
for P in range(21):
    Ms = petersen_matchings(P)
    assert len(Ms) == 6
    opts = []
    for M in Ms:
        opts.append(('A', {t: (4 if t in M else 0) for t in tris_at[P]}))
    for t0 in tris_at[P]:
        two = [M for M in Ms if t0 in M]
        assert len(two) == 2
        d = {}
        for t in tris_at[P]:
            d[t] = 4 if t == t0 else (2 if (t in two[0] or t in two[1]) else 0)
        opts.append(('B', d))
    options.append(opts)

sols = []
def search(order, k, ell):
    if k == len(order):
        sols.append(dict(ell))
        return
    P = order[k]
    for kind, d in options[P]:
        if all(ell.get(t, d[t]) == d[t] for t in tris_at[P]):
            added = [t for t in tris_at[P] if t not in ell]
            for t in added:
                ell[t] = d[t]
            search(order, k + 1, ell)
            for t in added:
                del ell[t]

# order: BFS so that consecutive pairs share many triangles
order = [0]
while len(order) < 21:
    best = max((R for R in range(21) if R not in order),
               key=lambda R: sum(1 for t in tris_at[R] if any(Q in order for Q in tris[t])))
    order.append(best)
search(order, 0, {})
print('consistent l-skeletons (labelled):', len(sols))
from collections import Counter
prof = Counter()
for s in sols:
    c = Counter(s.values())
    nB = sum(1 for P in range(21) if sum(1 for t in tris_at[P] if s[t] == 2) > 0)
    prof[(c[4], c[2], c[0], nB)] += 1
for k, v in sorted(prof.items()):
    print('  #l=4: %d, #l=2: %d, #l=0: %d, pattern-B pairs: %d  ->  %d skeletons' % (k + (v,)))
import pickle
pickle.dump(sols, open('../data/ell_skeletons.pkl', 'wb'))
