"""Finish line (C), id 0 = O_24 (odd Leech), C1 27/09: classification of the pair (y1, y2) up to Aut(O_24) = 2^12:M24.

Coordinates a/sqrt8, a in Z^24.  Points 0..22 = F_23, point 23 = infinity.  Golay code = extended QR code (checked below).
Normal form (sign changes eps_C, C in Golay): a1 = 1 - 4*1_{T1}, a2 = eps_D (1 - 4*1_{T2}), D in Golay mod Omega, T1, T2 disjoint.
  y1 _|_ y2  <=>  |A & D| = 1 + |D|/4  (A = T1 u T2)  <=>  D (mod Omega) = octad meeting A in 3, or dodecad meeting A in 4.
  Trap (P) for O_24  <=>  no norm-3 v with |(v,y1)| = |(v,y2)| = 3  <=>  D not in {O+O', O+O'+Omega : O >= T1, O' >= T2 octads}.
Symmetries of the normal form: Stab_M24(T1) acting on (T2, [D]), and the swap (T1,T2,D) -> (T2,T1,D).
Output: orbit representatives with orbit sizes, (P) verdict, and the span/index test of the norm-3 vectors orthogonal to y1, y2
(N = <u> has rank 22 and index 1 or 7 in N_max = y-perp, so the norm-3 vectors of N_max must span a sublattice of index 1 or 7)."""
import itertools, json, random, sys
from fractions import Fraction as F
import numpy as np

P23 = 23
INF = 23
QR = sorted({(x * x) % P23 for x in range(1, P23)})
NQR = [x for x in range(1, P23) if x not in QR]


def mask(S):
    m = 0
    for i in S:
        m |= 1 << i
    return m


def pts(m):
    return [i for i in range(24) if m >> i & 1]


def popcount(m):
    return bin(m).count('1')


OMEGA = (1 << 24) - 1


# ---------- Golay code ----------
def golay_code():
    rows = []
    for i in range(P23):
        S = {(q + i) % P23 for q in QR} | {i}          # {i} + (Q + i): 12 points of F_23, parity bit 0
        rows.append(mask(S))
    rows.append(OMEGA)
    # span over F2
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
    code = {0}
    for b in basis:
        code |= {c ^ b for c in code}
    return basis, code


BASIS, CODE = golay_code()
WT = {}
for c in CODE:
    WT[popcount(c)] = WT.get(popcount(c), 0) + 1
assert len(BASIS) == 12 and WT == {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}, (len(BASIS), WT)
OCTADS = sorted(c for c in CODE if popcount(c) == 8)
DODECADS = sorted(c for c in CODE if popcount(c) == 12)


# ---------- M24 ----------
def inv_mod(x):
    return pow(x, P23 - 2, P23)


def perm_from(f):
    return np.array([f(i) for i in range(24)], dtype=np.int64)


def alpha(i):
    return INF if i == INF else (i + 1) % P23


def beta(i):
    return INF if i == INF else (2 * i) % P23


def gamma(i):
    if i == INF:
        return 0
    if i == 0:
        return INF
    return (-inv_mod(i)) % P23


def delta(i):
    if i == INF or i == 0:
        return i
    if i in QR:
        return (pow(i, 3, P23) * inv_mod(9)) % P23
    return (9 * pow(i, 3, P23)) % P23


GENS = [perm_from(f) for f in (alpha, beta, gamma, delta)]


def apply_mask(p, m):
    r = 0
    for i in pts(m):
        r |= 1 << int(p[i])
    return r


for g in GENS:
    assert sorted(g.tolist()) == list(range(24))
    assert all(apply_mask(g, b) in CODE for b in BASIS), 'generator does not preserve the code'


def compose(p, q):
    """first p, then q"""
    return q[p]


def inverse(p):
    r = np.empty_like(p)
    r[p] = np.arange(24)
    return r


def sympy_order(gens):
    from sympy.combinatorics import Permutation, PermutationGroup
    return PermutationGroup([Permutation(g.tolist()) for g in gens]).order()


# ---------- orbit machinery ----------
def schreier(gens, start, act):
    """BFS orbit of `start` under gens; returns dict point -> transversal element u with act(u, start) = point."""
    ident = np.arange(24)
    tree = {start: ident}
    queue = [start]
    while queue:
        x = queue.pop()
        ux = tree[x]
        for s in gens:
            y = act(s, x)
            if y not in tree:
                tree[y] = compose(ux, s)
                queue.append(y)
    return tree


def schreier_gens(gens, tree, act, k=40, seed=1):
    """k random Schreier generators of the stabiliser of the start point (a subgroup; completeness never depends on it)."""
    rnd = random.Random(seed)
    items = list(tree.items())
    out = []
    for _ in range(k * 4):
        x, ux = rnd.choice(items)
        s = rnd.choice(gens)
        y = act(s, x)
        g = compose(compose(ux, s), inverse(tree[y]))
        if not np.array_equal(g, np.arange(24)):
            out.append(g)
        if len(out) >= k:
            break
    return out


def canon_D(D):
    """representative of {D, D + Omega}: the one of weight <= 12; for dodecads the smaller mask."""
    Dc = D ^ OMEGA
    w = popcount(D)
    if w < 12:
        return D
    if w > 12:
        return Dc
    return min(D, Dc)


def main():
    G = GENS
    oG = sympy_order(G)
    print('|<gens>| =', oG)
    assert oG == 244823040
    T1 = mask([0, 1, 2, 3])
    act_set = lambda p, m: apply_mask(p, m)
    tree1 = schreier(G, T1, act_set)
    assert len(tree1) == 10626
    H1 = schreier_gens(G, tree1, act_set, k=30)
    oH1 = sympy_order(H1)
    print('|Stab(T1)| from Schreier generators =', oH1)
    assert oH1 == 23040
    # T2 orbits under Stab(T1)
    tetrads = [mask(c) for c in itertools.combinations(range(24), 4)]
    free = [t for t in tetrads if t & T1 == 0]
    assert len(free) == 4845
    seen, T2reps = set(), []
    for t in free:
        if t in seen:
            continue
        tr = schreier(H1, t, act_set)
        seen |= set(tr)
        T2reps.append((t, tr))
    print('T2 orbits under Stab(T1):', [len(tr) for t, tr in T2reps])
    sextet_T1 = [o for o in OCTADS if o & T1 == T1]
    results = []
    orbit_of = {}                        # (T2rep_index, canonD) -> orbit id
    orbits = []                          # list of dicts
    for ti, (t2, tr2) in enumerate(T2reps):
        H12 = schreier_gens(H1, tr2, act_set, k=30, seed=7 + ti)
        o12 = sympy_order(H12)
        assert o12 * len(tr2) == 23040, (o12, len(tr2))
        A = T1 | t2
        cands = set()
        for o in OCTADS:
            if popcount(o & A) == 3:
                cands.add(canon_D(o))
        for d in DODECADS:
            if popcount(d & A) == 4:
                cands.add(canon_D(d))
        act_D = lambda p, m: canon_D(apply_mask(p, m))
        left = set(cands)
        while left:
            d0 = min(left)
            orb = schreier(H12, d0, act_D)
            assert set(orb) <= cands
            left -= set(orb)
            oid = len(orbits)
            for d in orb:
                orbit_of[(ti, d)] = oid
            orbits.append({'T2rep': ti, 'D': d0, 'size_in_T2fibre': len(orb), 'fibre': len(tr2)})
    print('orbits of Stab(T1) on (T2,[D]):', len(orbits))
    # swap: (T1, T2, D) -> (T2, T1, D) -> map T2 to T1 by some h in M24
    parent = list(range(len(orbits)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    tree_all = tree1                      # u_x maps T1 -> x
    for oid, ob in enumerate(orbits):
        t2 = T2reps[ob['T2rep']][0]
        h = inverse(tree_all[t2])         # h maps t2 -> T1
        newT2 = apply_mask(h, T1)
        newD = canon_D(apply_mask(h, ob['D']))
        # locate newT2 in its Stab(T1)-orbit
        for ti, (t, tr) in enumerate(T2reps):
            if newT2 in tr:
                k = inverse(tr[newT2])    # maps newT2 -> rep t
                dd = canon_D(apply_mask(k, newD))
                other = orbit_of[(ti, dd)]
                ra, rb = find(oid), find(other)
                if ra != rb:
                    parent[ra] = rb
                break
    classes = {}
    for oid in range(len(orbits)):
        classes.setdefault(find(oid), []).append(oid)
    print('orbits under Stab(T1) x swap:', len(classes))
    # verdicts
    out = []
    for root, members in sorted(classes.items()):
        ob = orbits[members[0]]
        t2 = T2reps[ob['T2rep']][0]
        A = T1 | t2
        D = ob['D']
        sextet_T2 = [o for o in OCTADS if o & t2 == t2]
        sums = {canon_D(o ^ o2) for o in sextet_T1 for o2 in sextet_T2}
        killed_P = D in sums
        size = sum(orbits[m]['size_in_T2fibre'] * orbits[m]['fibre'] for m in members)
        out.append({'T1': pts(T1), 'T2': pts(t2), 'D': pts(D), 'D_weight': popcount(D),
                    'A_is_octad': A in CODE, 'A_D': popcount(A & D),
                    'normalised_configs': size, 'P_killed': killed_P})
    return out


if __name__ == '__main__':
    res = main()
    tot = sum(r['normalised_configs'] for r in res)
    print('total normalised configurations covered:', tot)
    for r in res:
        print(r)
    json.dump({'golay_basis': BASIS, 'points': '0..22 = F_23, 23 = infinity', 'orbits': res},
              open(sys.argv[1] if len(sys.argv) > 1 else 'o24_ypairs.json', 'w'), indent=1)
