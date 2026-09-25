r"""X15g -- exact feasibility of the Fano-tight counting system (<= 5 min check, HiGHS via scipy.milp).

Unknowns: the 7 bijections sigma_P (tight: sigma_P(v) avoids the line through P and class v), as 0/1 variables.
Everything below is LINEAR in them (derivation: note E3):
  landing distributions LA_P(y, c) of every pair y via each of its classes;
  generic counts g_R'(y) (closed forms, checked here against the linear-system solution of X15);
  (K)  g_{M,c}(y) >= 0                          (equivalent to kappa: b != M_M(a));
  (B)  block balance  N(R,R') = N(R',R);
  (Lb) label balance  sum_{y containing u} cnt(y, R') = 8  for every block R' avoiding class(u).
Modes: 'K', 'KB', 'KBL' (which families are imposed).  Controls: K and KB must be feasible (X15 found such sigma).
"""
import sys, itertools, time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0, 'scripts')
from x15_fano_tight import FANO, PHI, LINE_OF, LAB, mate, BLOCKS, PAIRS, blk, allowed

VARS = [(P, v, w) for P in range(7) for v in LAB if v[0] != P for w in allowed(P, v)]
VI = {t: i for i, t in enumerate(VARS)}
NV = len(VARS)


def LA(y, P):
    """landing distribution of y via its class P: dict class -> sparse linear form {var: coef}."""
    e = next(l for l in y if l[0] == P); f = next(l for l in y if l[0] != P)
    out = {}
    if e[1] == 0:   # sigma_P(f)
        for w in allowed(P, f):
            out.setdefault(w[0], {})[VI[(P, f, w)]] = 1
    else:           # sigma_P^{-1}(f): v with sigma_P(v) = f
        for v in LAB:
            if v[0] != P and f in allowed(P, v):
                out.setdefault(v[0], {})[VI[(P, v, f)]] = 1
    return out


def add(*forms, const=0):
    res = {}
    for sgn, F in forms:
        for k, c in F.items():
            res[k] = res.get(k, 0) + sgn * c
    return res, const


def cnt_form(y, R):
    """linear form (dict, const) for the number of neighbours of y in block R (R != blk(y))."""
    P, Q = sorted(blk(y)); M = PHI[(P, Q)]
    la = {P: LA(y, P), Q: LA(y, Q)}
    if R & blk(y):
        (A_, d), = [(A_, d) for A_ in (P, Q) for d in R if A_ in R and d != A_]
        return add((1, la[A_].get(d, {})), const=int(d == M))
    # generic
    Rl = sorted(R)
    if M not in R:
        Lr = LINE_OF[frozenset(Rl)]
        if P in Lr:
            return add(*[(-1, la[P].get(c, {})) for c in Rl], const=1)
        if Q in Lr:
            return add(*[(-1, la[Q].get(c, {})) for c in Rl], const=1)
        assert M in Lr
        return add(*[(-1, la[A_].get(c, {})) for c in Rl for A_ in (P, Q)], const=3)
    c = Rl[0] if Rl[1] == M else Rl[1]
    cm = PHI[(M, c)]
    terms = [(1, la[P].get(cm, {})), (1, la[Q].get(cm, {})),
             (1, la[Q].get(c, {})), (1, la[Q].get(PHI[(Q, c)], {})),
             (1, la[P].get(c, {})), (1, la[P].get(PHI[(P, c)], {}))]
    return add(*terms, const=-1)


def check_closed_forms(seed=5):
    """compare cnt_form with X15's linear-system g on a random tight sigma."""
    import random
    from x15_fano_tight import fano_tau, random_sigma_tight, config_data
    rng = random.Random(seed)
    tau = fano_tau(rng)
    sigma = {P: random_sigma_tight(P, rng) for P in range(7)}
    D = config_data(tau, sigma)
    xval = np.zeros(NV)
    for P in range(7):
        for v, w in sigma[P].items():
            xval[VI[(P, v, w)]] = 1
    bad = 0
    for y in PAIRS:
        for R in BLOCKS:
            if R == blk(y):
                continue
            F, c0 = cnt_form(y, R)
            val = c0 + sum(cf * xval[k] for k, cf in F.items())
            if R & blk(y):
                ref = sum(1 for z in D['spec'][y] if blk(z) == R)
            else:
                ref = D['gen'][y][R] if D['ok'] else None
            if ref is not None and val != ref:
                bad += 1
    return bad, D['ok']


def build(mode):
    rows, lo, hi = [], [], []
    def con(F, c0, l, h):
        rows.append(F); lo.append(l - c0); hi.append(h - c0)
    for P in range(7):
        dom = [v for v in LAB if v[0] != P]
        for v in dom:
            con({VI[(P, v, w)]: 1 for w in allowed(P, v)}, 0, 1, 1)
        for w in dom:
            con({VI[(P, v, w)]: 1 for v in dom if w in allowed(P, v)}, 0, 1, 1)
    # (K): all generic counts >= 0 (only g_{M,c} can go negative)
    for y in PAIRS:
        for R in BLOCKS:
            if not (R & blk(y)):
                F, c0 = cnt_form(y, R)
                con(F, c0, 0, np.inf)
    if 'B' in mode:
        for R, Rp in itertools.combinations(BLOCKS, 2):
            F = {}; c0 = 0
            for y in PAIRS:
                if blk(y) == R:
                    f, c = cnt_form(y, Rp); c0 += c
                    for k, v in f.items(): F[k] = F.get(k, 0) + v
                elif blk(y) == Rp:
                    f, c = cnt_form(y, R); c0 -= c
                    for k, v in f.items(): F[k] = F.get(k, 0) - v
            con(F, c0, 0, 0)
    if 'L' in mode:
        for u in LAB:
            for R in BLOCKS:
                if u[0] in R:
                    continue
                F = {}; c0 = 0
                for y in PAIRS:
                    if u in y:
                        f, c = cnt_form(y, R); c0 += c
                        for k, v in f.items(): F[k] = F.get(k, 0) + v
                con(F, c0, 8, 8)
    if 'D' in mode:
        # (F5) from the diagonal of P2 (variance zero): g_R(y) = 2 for both type-A blocks R of every pair y
        for y in PAIRS:
            P, Q = sorted(blk(y)); M = PHI[(P, Q)]
            for R in BLOCKS:
                if not (R & {P, Q, M}) and M in LINE_OF[R]:
                    F, c0 = cnt_form(y, R)
                    con(F, c0, 2, 2)
    A = lil_matrix((len(rows), NV))
    for i, F in enumerate(rows):
        for k, v in F.items():
            if v:
                A[i, k] = v
    return LinearConstraint(A.tocsr(), np.array(lo, float), np.array(hi, float)), len(rows)


if __name__ == '__main__':
    bad, ok = check_closed_forms()
    print('closed forms vs linear system: mismatches', bad, '(config ok:', ok, ')', flush=True)
    for mode in sys.argv[1:] or ['K', 'KB', 'KBL']:
        C, nrows = build(mode)
        t = time.time()
        res = milp(c=np.zeros(NV), constraints=[C], integrality=np.ones(NV), bounds=Bounds(0, 1),
                   options=dict(time_limit=290, disp=False))
        print(f'mode {mode}: {nrows} constraints, status {res.status} ({res.message}), {time.time() - t:.1f}s', flush=True)
        if res.x is not None:
            np.save(f'data/x15g_{mode}.npy', np.rint(res.x))
