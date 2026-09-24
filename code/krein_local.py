"""LOCAL Krein conditions at a vertex x of srg(99,14,1,2) (pure mathematics, notes/70).
H = graph on X = Gamma_2(x) (84 vertices = pairs {a,b} of non-mate labels). U = B^T R^14 is H-invariant with H|U ~ J-I-M
(eigenvalues 12, -2, 0); on U^perp (70-dim) (H-3)(H+4) = 0.  Idempotents of H:
  E1 = J/84, E2 (lifted class-symmetric, 6-dim), E3p (lifted antisymmetric, 7-dim),
  E3H = (H - C)/7 with C = -4I + 16E1 + 2E2 + 4E3p,   E4H = (C' - H)/7 with C' = 3I + 9E1 - 5E2 - 3E3p.
Entries depend only on H-adjacency and the label type of (z,z'): T0 same, T1m share a label + other labels mates,
T1o share a label otherwise, T2m2/T2m1/T2m0 disjoint label pairs with 2/1/0 mate relations.
Local statistics: W = |W(x)| = twisted labelled edges, D2 = disjoint edges of type m2; D1 = W - 2 D2 (L6), D0 = 420 - W + D2.
Condition: for idempotents X, Y, Z:  sum_{z,z'} X Y Z >= 0.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement

types = ['T0', 'T1m', 'T1o', 'T2m2', 'T2m1', 'T2m0']
E1 = {t: F(1, 84) for t in types}
E2 = {'T0': F(1, 14), 'T1m': F(1, 14), 'T1o': F(3, 140), 'T2m2': F(1, 14), 'T2m1': F(3, 140), 'T2m0': F(-1, 35)}
E3p = {'T0': F(1, 12), 'T1m': F(0), 'T1o': F(1, 24), 'T2m2': F(-1, 12), 'T2m1': F(-1, 24), 'T2m0': F(0)}
C = {t: (-4 if t == 'T0' else 0) + 16 * E1[t] + 2 * E2[t] + 4 * E3p[t] for t in types}
Cp = {t: (3 if t == 'T0' else 0) + 9 * E1[t] - 5 * E2[t] - 3 * E3p[t] for t in types}


def entry(name, t, adj):
    h = 1 if adj else 0
    if name == 'E1': return E1[t]
    if name == 'E2': return E2[t]
    if name == 'E3p': return E3p[t]
    if name == 'E3H': return (h - C[t]) / 7
    if name == 'E4H': return (Cp[t] - h) / 7


def counts(W, D2):
    D1, D0 = W - 2 * D2, 420 - W + D2
    return {('T0', 0): 84,
            ('T1m', 1): 2 * (84 - W), ('T1m', 0): 2 * W,
            ('T1o', 1): 2 * W, ('T1o', 0): 1680 - 2 * W,
            ('T2m2', 1): 2 * D2, ('T2m2', 0): 84 - 2 * D2,
            ('T2m1', 1): 2 * D1, ('T2m1', 0): 1680 - 2 * D1,
            ('T2m0', 1): 2 * D0, ('T2m0', 0): 3360 - 2 * D0}


# sanity: idempotents sum to I, traces 1, 6, 7, 40, 30, and E3H + E4H + E1 + E2 + E3p = I entrywise
names = ['E1', 'E2', 'E3p', 'E3H', 'E4H']
for t in types:
    for adj in ([0] if t == 'T0' else [0, 1]):
        s = sum(entry(nm, t, adj) for nm in names)
        assert s == (1 if t == 'T0' else 0), (t, adj, s)
print('traces:', [84 * entry(nm, 'T0', 0) for nm in names])

cond = []
for trip in combinations_with_replacement(names, 3):
    if not ({'E3H', 'E4H'} & set(trip)):
        continue
    # linear in (W, D2): evaluate at 3 points
    val = lambda W, D2: sum(c * entry(trip[0], t, a) * entry(trip[1], t, a) * entry(trip[2], t, a)
                            for (t, a), c in counts(W, D2).items())
    c0 = val(0, 0)
    cW = val(1, 0) - c0
    cD = val(0, 1) - c0
    cond.append((trip, c0, cW, cD))
    print(f'{"*".join(trip):16s}: {float(c0):+.5f} {float(cW):+.6f}*W {float(cD):+.6f}*D2')

# feasible region: 0 <= W <= 84, 0 <= D2, W - 2 D2 >= 0, 420 - W + D2 >= 0
feas = [(W, D2) for W in range(85) for D2 in range(0, W // 2 + 1)
        if all(c0 + cW * W + cD * D2 >= 0 for _, c0, cW, cD in cond)]
Ws = sorted(set(w for w, _ in feas))
print(f'feasible (W, D2) integer points: {len(feas)};  W range {min(Ws) if Ws else None}..{max(Ws) if Ws else None}')
for W in (0, 6, 12, 14, 20, 30, 42, 60, 84):
    ds = [d for w, d in feas if w == W]
    print(f'   W = {W:2d}: D2 in {min(ds) if ds else "-"}..{max(ds) if ds else "-"}')
