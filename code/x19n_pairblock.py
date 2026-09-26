r"""X19n -- 'pair x block' level: disaggregate each class-level type per block into the exact subset S of the block's
pairs that z is adjacent to (|S| = multiplicity).  All of the following become LINEAR:
  cons     : sum_S s[z,t,R,S] = x[z,t]
  labdeg   : for every label l outside z's classes: sum_R sum_S s[z,t,R,S] * #{pairs of S containing l} = (2 - h_z(l)) x[z,t]
  pairblk  : for every pair y and block R':  sum_z [z ~ y] cnt(z,R') = sum_{w in R'} (A_D^2)_{yw}
             (A_D^2)_{yw} = 12 if y = w, else 2 - |y cap w| - [y ~ w]   (the [y ~ w] terms are cnt(y,R'), linear)
  pairpair : for y != y' in the same block R: sum_z [z ~ y][z ~ y'] = 2 - |y cap y'| - [y ~ y']
plus the block-level rows of X19 (bal, lab, P2).  Products across two different blocks of the SAME z are only
used through (subset in R) x (class count in R'), never (subset in R) x (subset in R').  Valid relaxation."""
import sys, itertools, pickle, time
from collections import Counter
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
sys.path.insert(0, 'scripts')
import x19_block_lp_generic as X
from x14_triangle_supports import LAB

PAIRS, BLOCKS, blk = X.PAIRS, X.BLOCKS, X.blk
PIDX = {p: i for i, p in enumerate(PAIRS)}
bpairs = {R: [y for y in PAIRS if blk(y) == R] for R in BLOCKS}

def build(tau, sigma, track=False):
    sinv = {c: {w: v for v, w in sigma[c].items()} for c in range(7)}
    spec = {z: X.specials(z, tau, sigma, sinv) for z in PAIRS}
    T = {z: X.types_for(z, spec[z]) for z in PAIRS}
    if any(not T[z] for z in PAIRS):
        return None
    var = []
    for z in PAIRS:
        for i, t in enumerate(T[z]):
            var.append(('x', z, i))
            for R, m in t.items():
                for S in itertools.combinations(bpairs[R], m):
                    var.append(('s', z, i, R, frozenset(S)))
    VI = {v: j for j, v in enumerate(var)}; nv = len(var)
    hits = {}
    for z in PAIRS:
        P, Q = sorted(blk(z))
        h = Counter(l for w in spec[z] for l in w if l[0] not in (P, Q))
        hits[z] = {l: 2 - h[l] for l in LAB if l[0] not in (P, Q)}
    rows, rhs, rnames = [], [], []
    fmt = lambda l: f'{l[0]}.{l[1]}'
    pn = lambda z: '-'.join(fmt(l) for l in sorted(z))
    bn = lambda R: ''.join(map(str, sorted(R)))
    def eq(F, c0, r, name=''):
        rows.append(F); rhs.append(r - c0); rnames.append(name)
    def add(F, k, v):
        F[k] = F.get(k, 0) + v
    def cnt_block(z, R):            # (form, const)
        if R & blk(z):
            return {}, sum(1 for w in spec[z] if blk(w) == R)
        return {VI[('x', z, i)]: t[R] for i, t in enumerate(T[z]) if t.get(R, 0)}, 0
    # conv, cons, labdeg
    for z in PAIRS:
        eq({VI[('x', z, i)]: 1 for i in range(len(T[z]))}, 0, 1, f'conv|{pn(z)}')
        for i, t in enumerate(T[z]):
            for R, m in t.items():
                F = {VI[('s', z, i, R, frozenset(S))]: 1 for S in itertools.combinations(bpairs[R], m)}
                F[VI[('x', z, i)]] = -1
                eq(F, 0, 0, f'cons|{i}|{bn(R)}|{pn(z)}')
            for l, need in hits[z].items():
                F = {VI[('x', z, i)]: -need}
                for R, m in t.items():
                    if l[0] in R:
                        for S in itertools.combinations(bpairs[R], m):
                            k = sum(1 for y in S if l in y)
                            if k:
                                add(F, VI[('s', z, i, R, frozenset(S))], k)
                eq(F, 0, 0, f'labdeg|{i}|{fmt(l)}|{pn(z)}')
    # block-level rows (X19): bal, lab, P2
    for R, Rp in itertools.combinations(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            if blk(z) == R:
                G, c = cnt_block(z, Rp); c0 += c
                for k, v in G.items(): add(F, k, v)
            elif blk(z) == Rp:
                G, c = cnt_block(z, R); c0 -= c
                for k, v in G.items(): add(F, k, -v)
        eq(F, c0, 0, f'bal|{bn(R)}|{bn(Rp)}')
    for u in LAB:
        for R in BLOCKS:
            if u[0] in R: continue
            F = {}; c0 = 0
            for z in PAIRS:
                if u in z:
                    G, c = cnt_block(z, R); c0 += c
                    for k, v in G.items(): add(F, k, v)
            eq(F, c0, 8, f'lab|{fmt(u)}|{bn(R)}')
    for R, Rp in itertools.combinations_with_replacement(BLOCKS, 2):
        F = {}; c0 = 0
        for z in PAIRS:
            if (R & blk(z)) and (Rp & blk(z)):
                c0 += cnt_block(z, R)[1] * cnt_block(z, Rp)[1]; continue
            for i, t in enumerate(T[z]):
                a = t.get(R, 0) if not (R & blk(z)) else cnt_block(z, R)[1]
                b = t.get(Rp, 0) if not (Rp & blk(z)) else cnt_block(z, Rp)[1]
                if a * b: add(F, VI[('x', z, i)], a * b)
        r = (48 if R == Rp else 0) + sum(2 - len(y & w) for y in bpairs[R] for w in bpairs[Rp] if w != y)
        for w in bpairs[R]:
            G, c = cnt_block(w, Rp); c0 += c
            for k, v in G.items(): add(F, k, v)
        eq(F, c0, r, f'P2|{bn(R)}|{bn(Rp)}')
    # [z ~ y] as (form, const) for a given z and pair y
    def adj(z, y):
        if y == z:
            return {}, 0
        if blk(y) & blk(z):
            return {}, int(y in spec[z])
        R = blk(y); F = {}
        for i, t in enumerate(T[z]):
            m = t.get(R, 0)
            if m:
                for S in itertools.combinations(bpairs[R], m):
                    if y in S:
                        F[VI[('s', z, i, R, frozenset(S))]] = 1
        return F, 0
    # pairblk: for every pair y and block R'
    for y in PAIRS:
        Ry = blk(y)
        for Rp in BLOCKS:
            F = {}; c0 = 0
            for z in PAIRS:
                if z == y: continue
                zspec_y = bool(Ry & blk(z)); zspec_Rp = bool(Rp & blk(z))
                if zspec_y and zspec_Rp:
                    c0 += int(y in spec[z]) * cnt_block(z, Rp)[1]; continue
                for i, t in enumerate(T[z]):
                    cR = t.get(Rp, 0) if not zspec_Rp else cnt_block(z, Rp)[1]
                    if not cR: continue
                    if zspec_y:
                        if y in spec[z]: add(F, VI[('x', z, i)], cR)
                    else:
                        m = t.get(Ry, 0)
                        for S in itertools.combinations(bpairs[Ry], m):
                            if y in S: add(F, VI[('s', z, i, Ry, frozenset(S))], cR)
            r = sum(12 if w == y else 2 - len(y & w) for w in bpairs[Rp])
            G, c = cnt_block(y, Rp)                       # the -[y ~ w] terms, moved to the left
            c0 += c
            for k, v in G.items(): add(F, k, v)
            eq(F, c0, r, f'pairblk|{pn(y)}|{bn(Rp)}')
    # pairpair inside a block
    for R in BLOCKS:
        for y, y2 in itertools.combinations(bpairs[R], 2):
            F = {}; c0 = 0
            for z in PAIRS:
                if z in (y, y2): continue
                if R & blk(z):
                    c0 += int(y in spec[z] and y2 in spec[z]); continue
                for i, t in enumerate(T[z]):
                    m = t.get(R, 0)
                    for S in itertools.combinations(bpairs[R], m):
                        if y in S and y2 in S: add(F, VI[('s', z, i, R, frozenset(S))], 1)
            eq(F, c0, 2 - len(y & y2) - int(y2 in spec[y]), f'pairpair|{pn(y)}|{pn(y2)}')
    r_, c_, d_ = [], [], []
    for i, F in enumerate(rows):
        for k, v in F.items():
            if v: r_.append(i); c_.append(k); d_.append(v)
    A = coo_matrix((d_, (r_, c_)), shape=(len(rows), nv)).tocsr()
    if track:
        cnames = []
        for v in var:
            if v[0] == 'x':
                _, z, i = v
                cnames.append(f'x|{pn(z)}|{i}|' + ','.join(f'{bn(R)}:{mm}' for R, mm in sorted(T[z][i].items(), key=lambda kv: bn(kv[0]))))
            else:
                _, z, i, R, S = v
                cnames.append(f's|{pn(z)}|{i}|{bn(R)}|' + '+'.join(sorted(pn(y) for y in S)))
        return A, np.array(rhs, float), nv, rnames, cnames, spec
    return A, np.array(rhs, float), nv

def solve(tau, sigma, tlim=280):
    t0 = time.time()
    out = build(tau, sigma)
    if out is None: return 'no types'
    A, b, nv = out
    t1 = time.time()
    res = linprog(np.zeros(nv), A_eq=A, b_eq=b, bounds=(0, None), method='highs-ipm', options=dict(time_limit=tlim))
    st = 'feasible' if res.status == 0 else 'INFEASIBLE' if res.status == 2 else res.message
    return f'{st} ({nv} vars, {A.shape[0]} rows, nnz {A.nnz}, build {t1-t0:.0f}s, solve {time.time()-t1:.0f}s)'

if __name__ == '__main__':
    if len(sys.argv) > 2:          # single survivor: python x19n_pairblock.py <name> <time_limit>
        name, tlim = sys.argv[1], float(sys.argv[2])
        if name.startswith('seed11#'):
            s = pickle.load(open('data/x19_survivors_s11_S0.pkl', 'rb'))[int(name.split('#')[1])]
        elif name.endswith('.pkl') or '.pkl#' in name:
            f, k = name.split('#')
            s = pickle.load(open(f, 'rb'))[int(k)]
        else:
            s = pickle.load(open('data/x19l_final_s21.pkl', 'rb'))[int(name.split('#')[1])]
        print(name, ':', solve(s['tau'], s['sigma'], tlim), flush=True)
        sys.exit()
    fin = []
    S11 = pickle.load(open('data/x19_survivors_s11_S0.pkl', 'rb')); fin.append(('seed11#0', S11[0]))
    for j, s in enumerate(pickle.load(open('data/x19l_final_s21.pkl', 'rb'))):
        fin.append((f'seed21#{j}', s))
    for name, s in fin:
        print(name, ':', solve(s['tau'], s['sigma']), flush=True)
