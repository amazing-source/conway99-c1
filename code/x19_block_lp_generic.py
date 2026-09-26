r"""X19 -- C2's winning method transferred to C1: block-level system with (P2) linearised by pair types, for GIVEN
local data (tau, sigma) at a vertex x in maximal torsion (generic counts are unknown variables).

For each pair z: special neighbours (2 tau, 2 sigma) are fixed by (tau, sigma).  Its generic neighbours form a graph
G_z on the 10 labels outside its classes, 8 edges, label degrees 2 - h_z(label), no mate edge, simple.  The TYPE of z
is the class-level multigraph of G_z (counts g_z(R) on the 10 blocks disjoint from blk(z)); only label-realisable
types are kept.  Variables x[z,t] >= 0, sum_t x[z,t] = 1.  Linear constraints:
  (B)  block balance N(R,R') = N(R',R);
  (L)  label balance sum_{y containing u} cnt(y,R') = 8  (R' avoiding class(u));
  (P2) sum_z cnt(z,R) cnt(z,R') = 12|R cap R'| - N(R,R') + sum_{y in R, w in R'} (2 - |y cap w|)   (all R <= R').
Feasibility by HiGHS (<= 5 min).  Controls: the Fano-tight witness (X15) must be feasible.
"""
import sys, itertools, random, pickle, time
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0, 'scripts')
from x14_triangle_supports import LAB, random_tau, random_sigma, build, admissible

mate = lambda l: (l[0], 1 - l[1])
BLOCKS = [frozenset(b) for b in itertools.combinations(range(7), 2)]
BI = {R: i for i, R in enumerate(BLOCKS)}
PAIRS = [frozenset({(c, s), (d, t)}) for c, d in itertools.combinations(range(7), 2) for s in (0, 1) for t in (0, 1)]
blk = lambda y: frozenset(l[0] for l in y)


def specials(y, tau, sigma, sinv):
    e, f = tuple(y)
    out = [frozenset({e, tau[e][f]}), frozenset({f, tau[f][e]})]
    for u, v in ((e, f), (f, e)):
        c = u[0]
        w = sigma[c][v] if u[1] == 0 else sinv[c][v]
        sp = frozenset({mate(u), w})
        if sp not in out:              # an in-block sigma edge is both sigma-specials of its ends: count it once
            out.append(sp)
    return out


def label_realisable(mg, deg_lab, classes):
    """mg: dict frozenset({c,c'}) -> multiplicity; deg_lab: label -> required degree. Backtracking on label edges."""
    need = dict(deg_lab)
    items = [(tuple(sorted(R)), m) for R, m in mg.items() if m]
    def rec(i):
        if i == len(items):
            return all(v == 0 for v in need.values())
        (c, d), m = items[i]
        cand = [(( c, s), (d, t)) for s in (0, 1) for t in (0, 1)]
        for comb in itertools.combinations(cand, m):
            ok = True
            for a, b in comb:
                need[a] -= 1; need[b] -= 1
            if all(v >= 0 for v in need.values()) and rec(i + 1):
                return True
            for a, b in comb:
                need[a] += 1; need[b] += 1
        return False
    return rec(0)


def types_for(z, spec):
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
                if label_realisable(mg, deg_lab, others):
                    out.append({R: m for R, m in mg.items() if m})
            return
        c, d = tuple(edges[i])
        for m in range(0, min(4, rem[c], rem[d]) + 1):
            rem[c] -= m; rem[d] -= m
            rec(i + 1, cur + [m], rem)
            rem[c] += m; rem[d] += m
    rec(0, [], dict(dcls))
    return out


def build_lp(tau, sigma, with_P2=True):
    sinv = {c: {w: v for v, w in sigma[c].items()} for c in range(7)}
    spec = {z: specials(z, tau, sigma, sinv) for z in PAIRS}
    for z in PAIRS:
        for w in spec[z]:
            if z not in spec[w]:
                return None, 'asymmetric special structure'
    T = {}
    for z in PAIRS:
        t = types_for(z, spec[z])
        if not t:
            return None, f'no type for {sorted(z)}'
        T[z] = t
    var = [(z, i) for z in PAIRS for i in range(len(T[z]))]
    VI = {v: k for k, v in enumerate(var)}
    nv = len(var)
    # cnt(z,R) as (constant, {var: coef})
    def cnt(z, R):
        if R == blk(z):
            return sum(1 for w in spec[z] if blk(w) == R), {}
        if R & blk(z):
            return sum(1 for w in spec[z] if blk(w) == R), {}
        return 0, {VI[(z, i)]: t.get(R, 0) for i, t in enumerate(T[z]) if t.get(R, 0)}
    rows, rhs = [], []
    def eq(F, c0, r):
        rows.append(F); rhs.append(r - c0)
    for z in PAIRS:
        eq({VI[(z, i)]: 1 for i in range(len(T[z]))}, 0, 1)
    # block balance
    for R, Rp in itertools.combinations(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            if blk(z) == R:
                c, f = cnt(z, Rp); c0 += c
                for k, v in f.items(): F[k] = F.get(k, 0) + v
            elif blk(z) == Rp:
                c, f = cnt(z, R); c0 -= c
                for k, v in f.items(): F[k] = F.get(k, 0) - v
        eq(F, c0, 0)
    # label balance
    for u in LAB:
        for R in BLOCKS:
            if u[0] in R:
                continue
            F = {}; c0 = 0
            for z in PAIRS:
                if u in z:
                    c, f = cnt(z, R); c0 += c
                    for k, v in f.items(): F[k] = F.get(k, 0) + v
            eq(F, c0, 8)
    if with_P2:
        for R, Rp in itertools.combinations_with_replacement(BLOCKS, 2):
            F = {}; c0 = 0
            for z in PAIRS:
                a0, fa = cnt(z, R); b0, fb = cnt(z, Rp)
                # product: types of z are mutually exclusive, so product is linear in x[z,i]
                if not fa and not fb:
                    c0 += a0 * b0; continue
                for i, t in enumerate(T[z]):
                    k = VI[(z, i)]
                    av = a0 + (t.get(R, 0) if not (R & blk(z)) else 0)
                    bv = b0 + (t.get(Rp, 0) if not (Rp & blk(z)) else 0)
                    if av * bv:
                        F[k] = F.get(k, 0) + av * bv
            r = 48 if R == Rp else 0
            for y in PAIRS:
                if blk(y) != R:
                    continue
                for w in PAIRS:
                    if blk(w) == Rp and w != y:
                        r += 2 - len(y & w)
            # - N(R,R') on the right  -> + sum_{y in R} cnt(y,R') on the left (R != R'); for R = R', N(R,R) = 2 e(R)
            for y in PAIRS:
                if blk(y) == R:
                    c, f = cnt(y, Rp); c0 += c
                    for k, v in f.items(): F[k] = F.get(k, 0) + v
            eq(F, c0, r)
    A = lil_matrix((len(rows), nv))
    for i, F in enumerate(rows):
        for k, v in F.items():
            if v:
                A[i, k] = v
    return (A.tocsr(), np.array(rhs, float), nv, T), 'ok'


def solve(tau, sigma, with_P2=True):
    built, msg = build_lp(tau, sigma, with_P2)
    if built is None:
        return msg
    A, b, nv, T = built
    t = time.time()
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, 1), method='highs', options=dict(time_limit=240))
    return f'status {res.status} ({"feasible" if res.status == 0 else "INFEASIBLE" if res.status == 2 else res.message}), ' \
           f'{nv} vars, {A.shape[0]} rows, {time.time() - t:.1f}s'


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'control'
    if mode == 'control':
        W = pickle.load(open('data/x15_witness.pkl', 'rb'))
        print('Fano witness, without P2:', solve(W['tau'], W['sigma'], False), flush=True)
        print('Fano witness, with P2   :', solve(W['tau'], W['sigma'], True), flush=True)
    else:
        seed, n = int(sys.argv[2]), int(sys.argv[3])
        rng = random.Random(seed)
        done = 0
        while done < n:
            tau = {u: random_tau(u, rng) for u in LAB}
            sigma = {c: random_sigma(c, rng) for c in range(7)}
            # local admissibility on all 42 fully determined supports first
            ok = True
            for tri in itertools.combinations(range(7), 3):
                pairs = [frozenset({(i, s), (j, t)}) for i, j in itertools.combinations(tri, 2) for s in (0, 1) for t in (0, 1)]
                if not admissible(build(pairs, tau, sigma)):
                    ok = False; break
            if not ok:
                continue
            done += 1
            print(f'random admissible config {done}: without P2:', solve(tau, sigma, False), '| with P2:', solve(tau, sigma, True), flush=True)
