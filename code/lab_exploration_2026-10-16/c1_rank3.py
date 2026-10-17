"""c = 1 cases with the RANK condition mod p (exploration, LAB 17/10/2026).
In a Conway graph rank_Q(T_S) <= 30 (nullity >= 14), hence rank_Fp(8 T_S mod p) <= 30 for every prime p.  For p = 3 and
p = 5, 8 T_S = 24 I - 8 Gamma - K8 is AFFINE in Gamma mod p.  The four star indicators z_0..z_3 are kernel vectors, so
Conway needs EXTRA kernel vectors y_1..y_k (k = 10) over F_p, independent of the stars.  Encoding (CP-SAT):
  y_j in F_p^44, zero at the star pivots (labels 04, 14, 24, 34; z_i is 1 at its own pivot, 0 at the others), reduced
  row echelon form: pivot pi_j = first nonzero position of y_j, y_j[pi_j] = 1, y_i[pi_j] = 0 (i != j), pi_1 < ... < pi_k;
  (8 T_S) y_j = 0 mod p: sum_i (24 d_ri - K8_ri) y_j[i] - 8 sum_{i != r} Gamma_ri y_j[i] = p t_{j,r}, products linearised.
This is a NON-convex condition (the averaging argument of c1_cases_avg.py does not apply to it).  Data: the 1 523 positive
blocks with a c = 1 side have rank_F3 >= 32, rank_F5 >= 33 (rankmod_data.py), i.e. none satisfies it.
Model = case model of c1_cases.py (axioms, c(l) = 1, E3, 2-cut lemma, rectangle profile) + this condition (no positivity).
usage: python c1_rank3.py <case index | -> <seconds> [k extra vectors=10] [p=3] [--fix structure.json] [--psd pool.json]"""
import json
import os
import random
import sys
import time

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402
import c1_cases as CS  # noqa: E402

ZPIV = [C.IDX[frozenset((s, 4))] for s in (0, 1, 2, 3)]


def add_rank_condition(m, e, k, p):
    n = C.n
    E = lambda i, j: e[C.pid(i, j)]
    free = [i for i in range(n) if i not in ZPIV]
    y = [[None] * n for _ in range(k)]
    for j in range(k):
        for i in range(n):
            y[j][i] = m.NewConstant(0) if i in ZPIV else m.NewIntVar(0, p - 1, "y%d_%d" % (j, i))
    # reduced row echelon form
    b = [[m.NewBoolVar("") for _ in free] for _ in range(k)]
    piv = []
    for j in range(k):
        m.AddExactlyOne(b[j])
        pv = m.NewIntVar(0, n - 1, "piv%d" % j)
        m.Add(pv == sum(i * b[j][a] for a, i in enumerate(free)))
        piv.append(pv)
        for a, i in enumerate(free):
            m.Add(y[j][i] == 1).OnlyEnforceIf(b[j][a])
            for jj in range(k):
                if jj != j:
                    m.Add(y[jj][i] == 0).OnlyEnforceIf(b[j][a])
            for a2, i2 in enumerate(free):
                if i2 < i:
                    m.Add(y[j][i2] == 0).OnlyEnforceIf(b[j][a])
    for j in range(k - 1):
        m.Add(piv[j] < piv[j + 1])
    # kernel equations mod p
    base = 24 * np.eye(n, dtype=np.int64) - C.K8
    for j in range(k):
        for r in range(n):
            terms = []
            for i in range(n):
                c0 = int(base[r, i]) % p
                if c0:
                    terms.append(c0 * y[j][i])
                if i != r:
                    z = m.NewIntVar(0, p - 1, "")
                    g = E(r, i)
                    m.Add(z == y[j][i]).OnlyEnforceIf(g)
                    m.Add(z == 0).OnlyEnforceIf(g.Not())
                    c1 = (-8) % p
                    if c1:
                        terms.append(c1 * z)
            hi = sum((p - 1) * (p - 1) for _ in terms) // p + 1
            t = m.NewIntVar(0, hi, "")
            m.Add(sum(terms) == p * t)
    return y


def rank_mod(M, p):
    A = [[int(x) % p for x in row] for row in M]
    n = len(A)
    r = 0
    for c in range(len(A[0])):
        pv = next((i for i in range(r, n) if A[i][c]), None)
        if pv is None:
            continue
        A[r], A[pv] = A[pv], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(n):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(a - f * bb) % p for a, bb in zip(A[i], A[r])]
        r += 1
    return r


def main():
    args = [a for a in sys.argv[1:]]
    fix = None
    if "--fix" in args:
        fix = args[args.index("--fix") + 1]
        del args[args.index("--fix"):args.index("--fix") + 2]
    poolf = None
    if "--psd" in args:
        poolf = args[args.index("--psd") + 1]
        del args[args.index("--psd"):args.index("--psd") + 2]
    ci = None if args[0] == "-" else int(args[0])
    secs = float(args[1])
    k = int(args[2]) if len(args) > 2 else 10
    p = int(args[3]) if len(args) > 3 else 3
    rng = random.Random(1)
    pool = json.load(open(poolf)) if poolf else {}
    if "--bare" in args:                      # encoding test: edge variables only
        args.remove("--bare")
        m = cp_model.CpModel()
        e = [m.NewBoolVar("e%d" % kk) for kk in range(len(C.PAIRS))]
    elif ci is not None:
        m, e = CS.build(CS.all_cases()[ci], pool, rng, use_cuts=bool(poolf))
    else:
        m, e, _ = C.build_model({}, rng)
        m.ClearObjective()
    if fix:
        d = json.load(open(fix))
        lab = [frozenset(x) for x in d["labels"]]
        eset = {frozenset((lab[i], lab[j])) for i, j in d["edges"]}
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for kk, (i, j) in enumerate(C.PAIRS):
            v = 1 if frozenset((C.S[i], C.S[j])) in eset else 0
            m.Add(e[kk] == v)
            G[i, j] = G[j, i] = v
        T8 = 24 * np.eye(C.n, dtype=np.int64) - 8 * G - C.K8
        print("fixed structure: rank_F%d(8 T_S) = %d -> nullity %d, extra kernel vectors available %d" % (
            p, rank_mod(T8, p), C.n - rank_mod(T8, p), C.n - rank_mod(T8, p) - 4), flush=True)
    t0 = time.time()
    add_rank_condition(m, e, k, p)
    print("model built (%.0f s): %d extra kernel vectors mod %d" % (time.time() - t0, k, p), flush=True)
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 2
    sv.parameters.max_time_in_seconds = secs
    st = sv.Solve(m)
    print("status: %s (%.0f s)" % (sv.StatusName(st), time.time() - t0), flush=True)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        G = np.zeros((C.n, C.n), dtype=np.int64)
        for kk, (i, j) in enumerate(C.PAIRS):
            if sv.Value(e[kk]):
                G[i, j] = G[j, i] = 1
        T8 = 24 * np.eye(C.n, dtype=np.int64) - 8 * G - C.K8
        ev, _ = C.perp_eigs(T8 / 8.0)
        evU, _ = C.perp_eigs(7 * C.PiS - T8 / 8.0)
        print("found: rank_F%d %d, rank_Q %d, lambda_min T %.3f U %.3f" % (
            p, rank_mod(T8, p), np.linalg.matrix_rank(T8.astype(float), tol=1e-6), ev.min(), evU.min()), flush=True)
        fn = os.path.join(HERE, "unbiased_walks", "rank%d_case%s.json" % (p, ci))
        json.dump({"labels": [sorted(l) for l in C.S], "edges": [[i, j] for i, j in C.PAIRS if G[i, j]]}, open(fn, "w"))
        print("saved", fn)


if __name__ == "__main__":
    main()
