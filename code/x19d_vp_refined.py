r"""X19d -- block-level system of X19 refined by the V/P split of the P2 diagonal (exact, derived by hand):
in block R = {C,D} (max twist), each of the 4 label-sharing pairs has exactly ONE common neighbour in Delta_x (none if
the two pairs are adjacent) and each of the 2 complementary pairs has exactly 2 (1 if adjacent, in-block sigma).
A generic common neighbour z of a label-sharing pair sees them as a V (two G_z-edges meeting at the shared label);
of a complementary pair, as a P (two disjoint G_z-edges of R).  Special common neighbours (z's block meets R) are
fixed by (tau, sigma).  Hence
    sum_z V_R(z) = 4 - (adjacent label-sharing pairs) - SS_V(R),     sum_z P_R(z) = 4 - e(R) - SS_P(R).
Types: class-level multigraph + for every block with 2 edges the choice V or P (3 edges: 2V+1P; 4 edges: 4V+2P),
realisable on labels.  All X19 rows are kept."""
import sys, itertools, random, pickle, time
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'scripts')
from x19_block_lp_generic import specials, PAIRS, BLOCKS, blk, mate
from x14_triangle_supports import LAB


def realisable_vp(mg, vp, deg_lab):
    need = dict(deg_lab)
    items = [(tuple(sorted(R)), m) for R, m in mg.items() if m]

    def ok_choice(key, comb):
        if len(comb) != 2 or key not in vp:
            return True
        (a, b), (c, d) = comb
        share = len({a, b} & {c, d}) == 1
        return share if vp[key] == 'V' else not share

    def rec(i):
        if i == len(items):
            return all(v == 0 for v in need.values())
        (c, d), m = items[i]
        cand = [((c, s), (d, t)) for s in (0, 1) for t in (0, 1)]
        for comb in itertools.combinations(cand, m):
            if not ok_choice((c, d), comb):
                continue
            for a, b in comb:
                need[a] -= 1; need[b] -= 1
            if all(v >= 0 for v in need.values()) and rec(i + 1):
                return True
            for a, b in comb:
                need[a] += 1; need[b] += 1
        return False
    return rec(0)


def types_vp(z, spec):
    P, Q = sorted(blk(z))
    others = [c for c in range(7) if c not in (P, Q)]
    hits = Counter(l for w in spec for l in w if l[0] not in (P, Q))
    deg_lab = {(c, s): 2 - hits[(c, s)] for c in others for s in (0, 1)}
    if any(v < 0 for v in deg_lab.values()):
        return None
    dcls = {c: deg_lab[(c, 0)] + deg_lab[(c, 1)] for c in others}
    edges = [frozenset(e) for e in itertools.combinations(others, 2)]
    out = []

    def rec(i, cur, rem):
        if i == len(edges):
            if all(v == 0 for v in rem.values()):
                mg = dict(zip(edges, cur))
                twos = [R for R, mm in mg.items() if mm == 2]
                for choice in itertools.product(('V', 'P'), repeat=len(twos)):
                    vp = {tuple(sorted(R)): ch for R, ch in zip(twos, choice)}
                    if realisable_vp(mg, vp, deg_lab):
                        V, Pp = {}, {}
                        for R, mm in mg.items():
                            if mm == 2:
                                V[R] = 1 if vp[tuple(sorted(R))] == 'V' else 0
                                Pp[R] = 1 - V[R]
                            elif mm == 3:
                                V[R], Pp[R] = 2, 1
                            elif mm == 4:
                                V[R], Pp[R] = 4, 2
                        out.append(({R: mm for R, mm in mg.items() if mm}, V, Pp))
            return
        c, d = tuple(edges[i])
        for mm in range(0, min(4, rem[c], rem[d]) + 1):
            rem[c] -= mm; rem[d] -= mm
            rec(i + 1, cur + [mm], rem)
            rem[c] += mm; rem[d] += mm
    rec(0, [], dict(dcls))
    return out


def build(tau, sigma):
    sinv = {c: {w: v for v, w in sigma[c].items()} for c in range(7)}
    spec = {z: specials(z, tau, sigma, sinv) for z in PAIRS}
    T = {}
    for z in PAIRS:
        t = types_vp(z, spec[z])
        if not t:
            return None
        T[z] = t
    var = [(z, i) for z in PAIRS for i in range(len(T[z]))]
    VI = {v: k for k, v in enumerate(var)}
    nv = len(var)

    def cnt(z, R):
        if R == blk(z) or (R & blk(z)):
            return sum(1 for w in spec[z] if blk(w) == R), {}
        return 0, {VI[(z, i)]: t[0].get(R, 0) for i, t in enumerate(T[z]) if t[0].get(R, 0)}
    rows, rhs = [], []

    def eq(F, c0, r):
        rows.append(F); rhs.append(r - c0)
    for z in PAIRS:
        eq({VI[(z, i)]: 1 for i in range(len(T[z]))}, 0, 1)
    for R, Rp in itertools.combinations(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            if blk(z) == R:
                c, f = cnt(z, Rp); c0 += c
                for k, v in f.items():
                    F[k] = F.get(k, 0) + v
            elif blk(z) == Rp:
                c, f = cnt(z, R); c0 -= c
                for k, v in f.items():
                    F[k] = F.get(k, 0) - v
        eq(F, c0, 0)
    for u in LAB:
        for R in BLOCKS:
            if u[0] in R:
                continue
            F = {}; c0 = 0
            for z in PAIRS:
                if u in z:
                    c, f = cnt(z, R); c0 += c
                    for k, v in f.items():
                        F[k] = F.get(k, 0) + v
            eq(F, c0, 8)
    for R, Rp in itertools.combinations_with_replacement(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            a0, fa = cnt(z, R); b0, fb = cnt(z, Rp)
            if not fa and not fb:
                c0 += a0 * b0; continue
            for i, t in enumerate(T[z]):
                av = a0 + (t[0].get(R, 0) if not (R & blk(z)) else 0)
                bv = b0 + (t[0].get(Rp, 0) if not (Rp & blk(z)) else 0)
                if av * bv:
                    F[VI[(z, i)]] = F.get(VI[(z, i)], 0) + av * bv
        r = 48 if R == Rp else 0
        for y in PAIRS:
            if blk(y) != R:
                continue
            for w in PAIRS:
                if blk(w) == Rp and w != y:
                    r += 2 - len(y & w)
        for y in PAIRS:
            if blk(y) == R:
                c, f = cnt(y, Rp); c0 += c
                for k, v in f.items():
                    F[k] = F.get(k, 0) + v
        eq(F, c0, r)
    for R in BLOCKS:
        ys = [y for y in PAIRS if blk(y) == R]
        share = [(a, b) for a, b in itertools.combinations(ys, 2) if len(a & b) == 1]
        comp = [(a, b) for a, b in itertools.combinations(ys, 2) if len(a & b) == 0]
        ssv = sum(1 for a, b in share for z in PAIRS if a in spec[z] and b in spec[z])
        ssp = sum(1 for a, b in comp for z in PAIRS if a in spec[z] and b in spec[z])
        e_R = sum(1 for a, b in comp if b in spec[a])
        adj_share = sum(1 for a, b in share if b in spec[a])
        Fv, Fp = {}, {}
        for z in PAIRS:
            if R & blk(z):
                continue
            for i, t in enumerate(T[z]):
                if t[1].get(R, 0):
                    Fv[VI[(z, i)]] = t[1][R]
                if t[2].get(R, 0):
                    Fp[VI[(z, i)]] = t[2][R]
        eq(Fv, 0, 4 - adj_share - ssv)
        eq(Fp, 0, 4 - e_R - ssp)
    A = lil_matrix((len(rows), nv))
    for i, F in enumerate(rows):
        for k, v in F.items():
            if v:
                A[i, k] = v
    return A.tocsr(), np.array(rhs, float), nv


def solve(tau, sigma):
    built = build(tau, sigma)
    if built is None:
        return 'no types'
    A, b, nv = built
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, 1), method='highs', options=dict(time_limit=240))
    return ('feasible' if res.status == 0 else 'INFEASIBLE' if res.status == 2 else res.message), nv, A.shape[0]


if __name__ == '__main__':
    W = pickle.load(open('data/x15_witness.pkl', 'rb'))
    print('control, Fano witness:', solve(W['tau'], W['sigma']), flush=True)
    S = pickle.load(open('data/x19_survivors_s11_S0.pkl', 'rb'))
    for k, s in enumerate(S):
        t = time.time()
        print(f'block-level survivor {k}:', solve(s['tau'], s['sigma']), f'{time.time()-t:.0f}s', flush=True)
