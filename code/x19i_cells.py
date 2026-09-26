r"""X19i -- block-level (P2) system + structures' antipodal-cell refinement, disaggregated (a valid relaxation).

Cells: in block R = {c,d} (c < d), cell A = {c_s d_t : s = t}, cell B = {c_s d_t : s != t}.
Identity for any two cell sets C, C' (from A_D^2 + A_D = 12I + 2J - d^T d):
    sum_z c_z(C) c_z(C') = 12|C cap C'| + 2|C||C'| - e(C,C') - L(C,C'),
    e(C,C') = sum_{w in C} c_w(C'),   L(C,C') = sum_{w in C, w' in C'} |w cap w'|.
Variables: x[z,t] (class-level types, as in X19) and, for every (z,t) and every generic block R of t, split
variables s[z,t,R,k] >= 0 with sum_k s = x[z,t]  (k = (m_A, m_B), m_A + m_B = t[R]).
Imposed (all linear): X19 rows; for every block R and every block R' the identity with C = A_R - B_R (signed) and
C' = R' (whole block); the same-block cell identities (C, C' in {A_R, B_R}); cell balance e(C,C') = e(C',C) for all
cell pairs; cell label balance sum_{y containing u} c_y(C) = 4 for cells avoiding class(u).
Products of splits in two different blocks are NOT imposed (they need joint splits)."""
import sys, itertools, pickle, time
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
sys.path.insert(0, 'scripts')
import x19_block_lp_generic as X
from x14_triangle_supports import LAB

PAIRS, BLOCKS, blk = X.PAIRS, X.BLOCKS, X.blk
cell_of = lambda y: (X.blk(y), 'A' if len({l[1] for l in y}) == 1 else 'B')
CELLS = [(R, h) for R in BLOCKS for h in 'AB']
CI = {c: i for i, c in enumerate(CELLS)}
members = {c: [y for y in PAIRS if cell_of(y) == c] for c in CELLS}
SPLITS = {1: [(1, 0), (0, 1)], 2: [(1, 1), (2, 0), (0, 2)], 3: [(2, 1), (1, 2)], 4: [(2, 2)]}


def build(tau, sigma, track=False):
    sinv = {c: {w: v for v, w in sigma[c].items()} for c in range(7)}
    spec = {z: X.specials(z, tau, sigma, sinv) for z in PAIRS}
    T = {z: X.types_for(z, spec[z]) for z in PAIRS}
    if any(not T[z] for z in PAIRS):
        return None
    # variable indexing
    var = []
    for z in PAIRS:
        for i, t in enumerate(T[z]):
            var.append(('x', z, i))
            for R, m in t.items():
                for k in SPLITS[m]:
                    var.append(('s', z, i, R, k))
    VI = {v: j for j, v in enumerate(var)}
    nv = len(var)
    spec_cells = {z: Counter(cell_of(w) for w in spec[z]) for z in PAIRS}
    # linear forms: dict var->coef, const
    def cz_cell(z, C):
        R, h = C
        if R & blk(z):
            return {}, spec_cells[z][C]
        F = {}
        for i, t in enumerate(T[z]):
            m = t.get(R, 0)
            if m:
                for k in SPLITS[m]:
                    val = k[0] if h == 'A' else k[1]
                    if val:
                        F[VI[('s', z, i, R, k)]] = val
        return F, 0
    def cz_block(z, R):
        if R & blk(z):
            return {}, sum(1 for w in spec[z] if blk(w) == R)
        return {VI[('x', z, i)]: t[R] for i, t in enumerate(T[z]) if t.get(R, 0)}, 0
    rows, rhs, rnames = [], [], []
    def eq(F, c0, r, name=''):
        rows.append(F); rhs.append(r - c0); rnames.append(name)
    def addto(F, G, sgn=1):
        for k, v in G.items():
            F[k] = F.get(k, 0) + sgn * v
    # conv + consistency
    for z in PAIRS:
        eq({VI[('x', z, i)]: 1 for i in range(len(T[z]))}, 0, 1, 'conv|' + '-'.join(f'{l[0]}.{l[1]}' for l in sorted(z)))
        for i, t in enumerate(T[z]):
            for R, m in t.items():
                F = {VI[('s', z, i, R, k)]: 1 for k in SPLITS[m]}
                F[VI[('x', z, i)]] = -1
                eq(F, 0, 0, f'cons|{i}|' + ''.join(map(str, sorted(R))) + '|' + '-'.join(f'{l[0]}.{l[1]}' for l in sorted(z)))
    # X19 rows (block level): balance, label balance, P2
    for R, Rp in itertools.combinations(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            if blk(z) == R:
                G, c = cz_block(z, Rp); addto(F, G); c0 += c
            elif blk(z) == Rp:
                G, c = cz_block(z, R); addto(F, G, -1); c0 -= c
        eq(F, c0, 0, 'bal|' + ''.join(map(str, sorted(R))) + '|' + ''.join(map(str, sorted(Rp))))
    for u in LAB:
        for R in BLOCKS:
            if u[0] in R:
                continue
            F = {}; c0 = 0
            for z in PAIRS:
                if u in z:
                    G, c = cz_block(z, R); addto(F, G); c0 += c
            eq(F, c0, 8, f'lab|{u[0]}.{u[1]}|' + ''.join(map(str, sorted(R))))
    def Lval(C1, C2):
        return sum(len(a & b) for a in C1 for b in C2)
    for R, Rp in itertools.combinations_with_replacement(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            if (R & blk(z)) and (Rp & blk(z)):
                c0 += cz_block(z, R)[1] * cz_block(z, Rp)[1]; continue
            for i, t in enumerate(T[z]):
                a = t.get(R, 0) if not (R & blk(z)) else cz_block(z, R)[1]
                b = t.get(Rp, 0) if not (Rp & blk(z)) else cz_block(z, Rp)[1]
                if a * b:
                    F[VI[('x', z, i)]] = F.get(VI[('x', z, i)], 0) + a * b
        yR = [y for y in PAIRS if blk(y) == R]; yRp = [y for y in PAIRS if blk(y) == Rp]
        r = 12 * len(set(yR) & set(yRp)) + 2 * 16 - Lval(yR, yRp)
        for w in yR:
            G, c = cz_block(w, Rp); addto(F, G); c0 += c
        eq(F, c0, r, 'P2|' + ''.join(map(str, sorted(R))) + '|' + ''.join(map(str, sorted(Rp))))
    # cell refinement (a): signed cell of R  x  whole block R'   (all R, R')
    for R in BLOCKS:
        A_, B_ = (R, 'A'), (R, 'B')
        for Rp in BLOCKS:
            F = {}; c0 = 0
            for z in PAIRS:
                Rspec = bool(R & blk(z)); Rpspec = bool(Rp & blk(z))
                if Rspec and Rpspec:
                    c0 += (spec_cells[z][A_] - spec_cells[z][B_]) * cz_block(z, Rp)[1]; continue
                for i, t in enumerate(T[z]):
                    b = t.get(Rp, 0) if not Rpspec else cz_block(z, Rp)[1]
                    if not b:
                        continue
                    if Rspec:
                        d = spec_cells[z][A_] - spec_cells[z][B_]
                        if d:
                            F[VI[('x', z, i)]] = F.get(VI[('x', z, i)], 0) + d * b
                    else:
                        m = t.get(R, 0)
                        for k in SPLITS.get(m, []):
                            d = k[0] - k[1]
                            if d:
                                j = VI[('s', z, i, R, k)]
                                F[j] = F.get(j, 0) + d * b
            yA, yB, yRp = members[A_], members[B_], [y for y in PAIRS if blk(y) == Rp]
            r = 12 * (len(set(yA) & set(yRp)) - len(set(yB) & set(yRp))) + 2 * (len(yA) - len(yB)) * len(yRp) \
                - (Lval(yA, yRp) - Lval(yB, yRp))
            for w in yA:
                G, c = cz_block(w, Rp); addto(F, G); c0 += c
            for w in yB:
                G, c = cz_block(w, Rp); addto(F, G, -1); c0 -= c
            eq(F, c0, r, 'cellcross|' + ''.join(map(str, sorted(R))) + '|' + ''.join(map(str, sorted(Rp))))
    # cell refinement (b): same-block cell pairs
    for R in BLOCKS:
        for h1, h2 in (('A', 'A'), ('A', 'B'), ('B', 'B')):
            C1, C2 = (R, h1), (R, h2)
            F = {}; c0 = 0
            for z in PAIRS:
                if R & blk(z):
                    c0 += spec_cells[z][C1] * spec_cells[z][C2]; continue
                for i, t in enumerate(T[z]):
                    m = t.get(R, 0)
                    for k in SPLITS.get(m, []):
                        v1 = k[0] if h1 == 'A' else k[1]; v2 = k[0] if h2 == 'A' else k[1]
                        if v1 * v2:
                            j = VI[('s', z, i, R, k)]
                            F[j] = F.get(j, 0) + v1 * v2
            r = 12 * len(set(members[C1]) & set(members[C2])) + 2 * 4 - Lval(members[C1], members[C2])
            for w in members[C1]:
                G, c = cz_cell(w, C2); addto(F, G); c0 += c
            eq(F, c0, r, 'cellsame|' + ''.join(map(str, sorted(R))) + '|' + h1 + h2)
    # cell refinement (c): cell balance e(C,C') = e(C',C)
    for C1, C2 in itertools.combinations(CELLS, 2):
        F = {}; c0 = 0
        for w in members[C1]:
            G, c = cz_cell(w, C2); addto(F, G); c0 += c
        for w in members[C2]:
            G, c = cz_cell(w, C1); addto(F, G, -1); c0 -= c
        eq(F, c0, 0, 'cellbal|' + ''.join(map(str, sorted(C1[0]))) + C1[1] + '|' + ''.join(map(str, sorted(C2[0]))) + C2[1])
    # cell refinement (d): cell label balance
    for u in LAB:
        for C in CELLS:
            if u[0] in C[0]:
                continue
            F = {}; c0 = 0
            for y in PAIRS:
                if u in y:
                    G, c = cz_cell(y, C); addto(F, G); c0 += c
            eq(F, c0, 2 * len(members[C]), f'celllab|{u[0]}.{u[1]}|' + ''.join(map(str, sorted(C[0]))) + C[1])
    r_, c_, d_ = [], [], []
    for i, F in enumerate(rows):
        for k, v in F.items():
            if v:
                r_.append(i); c_.append(k); d_.append(v)
    A = coo_matrix((d_, (r_, c_)), shape=(len(rows), nv)).tocsr()
    if track:
        return A, np.array(rhs, float), nv, rnames, var, T, spec
    return A, np.array(rhs, float), nv


def solve(tau, sigma):
    t0 = time.time()
    out = build(tau, sigma)
    if out is None:
        return 'no types'
    A, b, nv = out
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, None), method='highs-ipm', options=dict(time_limit=250))
    st = 'feasible' if res.status == 0 else 'INFEASIBLE' if res.status == 2 else res.message
    return f'{st} ({nv} vars, {A.shape[0]} rows, {time.time()-t0:.0f}s)'


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if which in ('witness', 'all'):
        W = pickle.load(open('data/x15_witness.pkl', 'rb'))
        print('control, Fano witness:', solve(W['tau'], W['sigma']), flush=True)
    if which != 'witness':
        S = pickle.load(open('data/x19_survivors_s11_S0.pkl', 'rb'))
        idx = range(len(S)) if which == 'all' else [int(k) for k in which.split(',')]
        for k in idx:
            print(f'survivor {k}:', solve(S[k]['tau'], S[k]['sigma']), flush=True)
