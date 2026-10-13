"""Lab session, 2026-10-13. Mission "C2 without computation", step 2: linear programme with one vector h, averaged
over the seven vectors h_c of the frame.

Unknown: the average over c = 1..7 of the coefficient tables of (U; y1, y2, h_c). Each of the seven tables lies in
the space spanned by the generators of h1_tables_<DMAX>.pkl, so does their average, and it satisfies:
  N   coefficient (integral, class 0, D = 0) = 1;
  I   no integral vector with 1 <= E <= T                       (A.5: T = 7; with T16, T18, T20: T = 10);
  S1  shadow vectors b, t = (b,h): E >= 10.5 + t^2 + [t even]   (the six other products have an odd square sum if t is even);
  P   all coefficients >= 0;
  H1  for every shadow energy E:  sum over the seven h of t^2 <= E - 10.5 for each vector, so
      sum_t t^2 n_S(E,t) <= ((E - 10.5)/7) sum_t n_S(E,t);
  H2  at least one of the seven products is odd:  sum_{t odd} n_S(E,t) >= (1/7) sum_t n_S(E,t);
  H3  for every integral energy E: sum over the seven h of t^2 <= 4E/7, and it is even:
      sum_t t^2 n_I(E,t) <= (K_E/7) sum_t n_I(E,t),  K_E = largest even integer <= 4E/7.
Here n_S(E,t), n_I(E,t) = number of shadow / integral vectors modulo J with energy E and product t with h
  = sum over the 49 classes of (A, B) of the coefficient at (class, t mod 4, D = 4E - 7 t^2).
Options: NOHEPTAD=1 drops H1, H2, H3.
python heptad1_lp.py <DMAX> <T>       scipy (HiGHS), under a minute, < 2 GB.  Floating-point verdict."""
import sys, os, pickle, itertools
import numpy as np
from scipy.optimize import linprog
import heptad1 as H

DMAX, T = int(sys.argv[1]), int(sys.argv[2])
desc, tabs = pickle.load(open("h1_tables_%d.pkl" % DMAX, "rb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
kidx = {k: i for i, k in enumerate(keys)}
M = np.array([[float(t.get(k, 0)) for k in keys] for t in tabs])
scale = np.maximum(1.0, np.abs(M).max(axis=0))
Ms = M / scale
# basis by QR with column pivoting on the transposed matrix
from scipy.linalg import qr
Q, R, piv = qr(Ms.T, mode="economic", pivoting=True)
rank = int((np.abs(np.diag(R)) > 1e-9 * abs(R[0, 0])).sum())
basis = sorted(piv[:rank].tolist())
Bm = M[basis]
nb = len(basis)
print("generators %d, basis %d, entries %d" % (len(tabs), nb, len(keys)), flush=True)


def col(kind, a7, b7, t, D):
    k = H.key_of(a7, b7, t, D, kind)
    return Bm[:, kidx[k]] if k in kidx else np.zeros(nb)


def n_vec(kind, e4, t):
    """coefficient vector (on the basis) of n_kind(E, t), E = e4 / 4"""
    D = e4 - 7 * t * t
    if D < 0:
        return None
    out = np.zeros(nb)
    for a7, b7 in itertools.product(range(7), repeat=2):
        out += col(kind, a7, b7, t, D)
    return out


Aeq, beq, Aub, bub = [], [], [], []
tmin = {0: 0, 1: 1, 3: 1, 2: 2}
for k in keys:
    kind, (a7, b7, t4), D = k
    c = Bm[:, kidx[k]]
    if kind == "I":
        if (a7, b7, t4) == (0, 0, 0) and D == 0:
            Aeq.append(c); beq.append(1.0); continue
        e4 = D + 7 * tmin[t4] ** 2
        if e4 <= 4 * T:
            Aeq.append(c); beq.append(0.0); continue
    else:
        bound = {0: 46, 1: 39, 3: 39, 2: 34}[t4]
        if D < bound:
            Aeq.append(c); beq.append(0.0); continue
    Aub.append(-c / scale[kidx[k]]); bub.append(0.0)
nrows_plain = len(Aub)
if os.environ.get("NOHEPTAD") is None:
    for e4 in range(4 * (T + 1), DMAX + 1):
        for kind in ("I", "S"):
            if kind == "I" and e4 % 4:
                continue
            if kind == "S" and e4 % 8 != 6:
                continue
            terms = [(t, n_vec(kind, e4, t)) for t in range(-6, 7)]
            terms = [(t, v) for t, v in terms if v is not None]
            tot = sum(v for t, v in terms)
            if not np.abs(tot).any():
                continue
            sq = sum(t * t * v for t, v in terms)
            if kind == "S":
                row = sq - ((e4 / 4 - 10.5) / 7.0) * tot                 # H1: <= 0
                odd = sum(v for t, v in terms if t % 2)
                row2 = tot / 7.0 - odd                                    # H2: <= 0
                for r in (row, row2):
                    s = np.abs(r).max()
                    if s > 0:
                        Aub.append(r / s); bub.append(0.0)
            else:
                K = 2 * int((e4 / 7.0) // 2)                              # largest even integer <= 4E/7 = e4/7
                r = sq - (K / 7.0) * tot                                  # H3: <= 0
                s = np.abs(r).max()
                if s > 0:
                    Aub.append(r / s); bub.append(0.0)
Aeq = np.array(Aeq); beq = np.array(beq); Aub = np.array(Aub); bub = np.array(bub)
eqs = np.maximum(1.0, np.abs(Aeq).max(axis=1))
print("T = %d: %d equalities (rank %d), %d positivity rows, %d heptad rows" % (T, len(beq), np.linalg.matrix_rank(Aeq / eqs[:, None], tol=1e-9), nrows_plain, len(bub) - nrows_plain), flush=True)
res = linprog(c=np.zeros(nb), A_ub=Aub, b_ub=bub, A_eq=Aeq / eqs[:, None], b_eq=beq / eqs, bounds=[(None, None)] * nb, method="highs")
print("linear programme: status %d  ->  %s" % (res.status, {0: "FEASIBLE", 2: "INFEASIBLE"}.get(res.status, str(res.message)[:60])))
if res.status == 0:
    def rng(vec):
        sc = np.abs(vec).max()
        out = []
        for sign in (1, -1):
            r = linprog(c=sign * vec / sc, A_ub=Aub, b_ub=bub, A_eq=Aeq / eqs[:, None], b_eq=beq / eqs, bounds=[(None, None)] * nb, method="highs")
            out.append(sign * r.fun * sc if r.status == 0 else float("nan"))
        return out
    tot = lambda kind, e4: sum(v for t in range(-6, 7) for v in [n_vec(kind, e4, t)] if v is not None)
    for name, vec in (("integral, E = 11 (all vectors modulo J; pairs = half)", tot("I", 44)),
                      ("shadow, E = 11.5", tot("S", 46)),
                      ("integral, E = 12", tot("I", 48)),
                      ("integral, E = 13", tot("I", 52)),
                      ("shadow, E = 11.5 with t = +-1", n_vec("S", 46, 1) + n_vec("S", 46, -1)),
                      ("integral, E = 11 with t = +-2", n_vec("I", 44, 2) + n_vec("I", 44, -2)),
                      ("integral, E = 11 with t = +-1", n_vec("I", 44, 1) + n_vec("I", 44, -1)),
                      ("integral, E = 12 with t = +-2", n_vec("I", 48, 2) + n_vec("I", 48, -2))):
        lo, hi = rng(vec)
        print("   %-55s between %8.2f and %8.2f" % (name, lo, hi), flush=True)
