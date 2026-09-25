r"""X15n -- Fano-tight system with the second-order block identities (P2), linearised by pair-type indicators.

For each pair z (classes P < Q, third point M), t[z,(a,b)] = [landing via P is a][landing via Q is b], restricted to
the combinations allowed by kappa + (F5): b in {Phi(P,a), Phi(Q,a)}  (the line through a and b passes through P or Q).
cnt(z,R) is a function of (a,b) only, so  sum_z cnt(z,R) cnt(z,R')  is linear in t.
(P2): sum_z cnt(z,R) cnt(z,R') = 12|R cap R'| + sum_{y in R, w in R', y != w} (2 - |y cap w|) - N(R,R').
Families imposed: K, B, L, D (as in X15g) + P2 (all block pairs, R = R' included).  <= 5 min check.
"""
import sys, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0, 'scripts')
from x15_fano_tight import FANO, PHI, LINE_OF, LAB, BLOCKS, PAIRS, blk, allowed
import x15g_ilp as G


def cnt_given(z, R, a, b):
    P, Q = sorted(blk(z)); M = PHI[(P, Q)]
    if R == blk(z):
        return 0
    if R & blk(z):
        (A_,) = R & blk(z); d = next(iter(R - {A_}))
        land = a if A_ == P else b
        return int(d == M) + int(land == d)
    if M not in R:
        Lr = LINE_OF[R]
        if P in Lr:
            return 1 - int(a in R)
        if Q in Lr:
            return 1 - int(b in R)
        return 3 - int(a in R) - int(b in R)
    (c,) = R - {M}
    cm = PHI[(M, c)]
    return -1 + int(a == cm) + int(b == cm) + int(b in (c, PHI[(Q, c)])) + int(a in (c, PHI[(P, c)]))


def types(z):
    P, Q = sorted(blk(z)); M = PHI[(P, Q)]
    C4 = [c for c in range(7) if c not in (P, Q, M)]
    return [(a, b) for a in C4 for b in (PHI[(P, a)], PHI[(Q, a)])]


TV = [(z, ab) for z in PAIRS for ab in types(z)]
TI = {t: G.NV + i for i, t in enumerate(TV)}
NTOT = G.NV + len(TV)


def build(mode):
    rows, lo, hi = [], [], []
    def con(F, c0, l, h):
        rows.append(F); lo.append(l - c0); hi.append(h - c0)
    C, n0 = G.build(mode)       # K, B, L, D families on the sigma variables
    A0 = C.A.tolil()
    for i in range(A0.shape[0]):
        F = {k: v for k, v in zip(A0.rows[i], A0.data[i])}
        rows.append(F); lo.append(C.lb[i]); hi.append(C.ub[i])
    # linking t to the landing distributions
    for z in PAIRS:
        P, Q = sorted(blk(z))
        laP, laQ = G.LA(z, P), G.LA(z, Q)
        tz = types(z)
        for a in {ab[0] for ab in tz} | set(laP):
            F = {TI[(z, ab)]: 1 for ab in tz if ab[0] == a}
            for k, v in laP.get(a, {}).items():
                F[k] = F.get(k, 0) - v
            con(F, 0, 0, 0)
        for b in {ab[1] for ab in tz} | set(laQ):
            F = {TI[(z, ab)]: 1 for ab in tz if ab[1] == b}
            for k, v in laQ.get(b, {}).items():
                F[k] = F.get(k, 0) - v
            con(F, 0, 0, 0)
        con({TI[(z, ab)]: 1 for ab in tz}, 0, 1, 1)
    if 'P' in mode:
        for R, Rp in itertools.combinations_with_replacement(BLOCKS, 2):
            F = {}
            for z in PAIRS:
                for ab in types(z):
                    v = cnt_given(z, R, *ab) * cnt_given(z, Rp, *ab)
                    if v:
                        F[TI[(z, ab)]] = F.get(TI[(z, ab)], 0) + v
            rhs = 48 if R == Rp else 0
            for y in PAIRS:
                if blk(y) != R:
                    continue
                for w in PAIRS:
                    if blk(w) == Rp and w != y:
                        rhs += 2 - len(y & w)
            # - N(R,R') moved to the left:  + sum_{y in R} cnt(y, R')  (linear in t)
            if R != Rp:
                for y in PAIRS:
                    if blk(y) == R:
                        for ab in types(y):
                            v = cnt_given(y, Rp, *ab)
                            if v:
                                F[TI[(y, ab)]] = F.get(TI[(y, ab)], 0) + v
            con(F, 0, rhs, rhs)
    A = lil_matrix((len(rows), NTOT))
    for i, F in enumerate(rows):
        for k, v in F.items():
            if v:
                A[i, k] = v
    return LinearConstraint(A.tocsr(), np.array(lo, float), np.array(hi, float)), len(rows)


def check_cnt_given(seed=7):
    """cnt_given vs cnt_form on the KBLD solution (landings read from sigma)."""
    x = np.load('data/x15g_KBLD.npy')
    bad = 0
    for z in PAIRS:
        P, Q = sorted(blk(z))
        laP, laQ = G.LA(z, P), G.LA(z, Q)
        a = [c for c, F in laP.items() if sum(x[k] * v for k, v in F.items()) > 0.5][0]
        b = [c for c, F in laQ.items() if sum(x[k] * v for k, v in F.items()) > 0.5][0]
        for R in BLOCKS:
            if R == blk(z):
                continue
            F, c0 = G.cnt_form(z, R)
            val = c0 + sum(x[k] * v for k, v in F.items())
            bad += int(round(val) != cnt_given(z, R, a, b))
    return bad


if __name__ == '__main__':
    print('cnt_given vs cnt_form mismatches:', check_cnt_given(), flush=True)
    for mode in sys.argv[1:] or ['KBLD', 'KBLDP']:
        C, nrows = build(mode)
        t = time.time()
        res = milp(c=np.zeros(NTOT), constraints=[C], integrality=np.ones(NTOT), bounds=Bounds(0, 1),
                   options=dict(time_limit=290, disp=False))
        print(f'mode {mode}: {nrows} constraints, status {res.status} ({res.message}), {time.time() - t:.1f}s', flush=True)
        if res.x is not None:
            np.save(f'data/x15n_{mode}.npy', np.rint(res.x))
