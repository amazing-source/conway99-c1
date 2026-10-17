"""Is the obstruction carried by the two root graphs? (exploration, LAB 17/10/2026)
Decomposition test for the c = 1 case list.  A four-star structure = H_l (all pairs of labels containing 0 or 1),
H_m (all pairs of labels containing 2 or 3) and the 400 pairs P x Q (P = labels with 0 or 1 but not 2, 3; Q = the
converse).  E3, the 2-cut lemma and c(l) = 1 only involve H_l and H_m.  Here H_l, H_m are taken from an integral
solution of the case model (c1_cases.build, stage 0) and FIXED; the P x Q pairs are RELAXED to [0, 1] with the linear
axioms (exact star counts, letter caps, pair caps with q >= e + e' - 1).  LP cutting planes (GLOP) for
    tau* = max over the relaxed P x Q of  min(8 lambda_min T_S, 8 lambda_min U_S)   (complement of the stars).
tau* < 0 (an LP value, i.e. a dual certificate) => NO completion of this (H_l, H_m) is positive, integral or not.
usage: python c1_hfix_lp.py <case index> <number of integral starts> [seconds per CP-SAT start] [LP rounds]"""
import itertools
import os
import random
import sys
import time

import numpy as np
from ortools.linear_solver import pywraplp
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c1_sv1_cuts as C  # noqa: E402
import c1_cases as CS  # noqa: E402

n = C.n
ROOTL = [i for i, l in enumerate(C.S) if l & {0, 1}]
ROOTM = [i for i, l in enumerate(C.S) if l & {2, 3}]
P = [i for i in ROOTL if not C.S[i] & {2, 3}]
Q = [i for i in ROOTM if not C.S[i] & {0, 1}]
SL, SM = set(ROOTL), set(ROOTM)
FIXED = [k for k, (i, j) in enumerate(C.PAIRS) if (i in SL and j in SL) or (i in SM and j in SM)]
FREE = [k for k, (i, j) in enumerate(C.PAIRS) if k not in set(FIXED)]
I24K = 24 * np.eye(n) - C.K8


def integral_start(ci, secs, seed):
    case = CS.all_cases()[ci]
    rng = random.Random(seed)
    m, e = CS.build(case, {}, rng, use_cuts=False)
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 2
    sv.parameters.max_time_in_seconds = secs
    sv.parameters.random_seed = seed
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    return np.array([sv.Value(x) for x in e], dtype=np.int64)


def lam8(gvec):
    G = np.zeros((n, n))
    for k, (i, j) in enumerate(C.PAIRS):
        G[i, j] = G[j, i] = gvec[k]
    T = (I24K - 8 * G) / 8.0
    U = 7 * C.PiS - T
    eT, VT = C.perp_eigs(T)
    eU, VU = C.perp_eigs(U)
    return T, U, eT, VT, eU, VU


def hfix_lp(gint, rounds, verbose=False):
    lp = pywraplp.Solver.CreateSolver("GLOP")
    var = {}
    for k in FREE:
        var[k] = lp.NumVar(0.0, 1.0, "e%d" % k)
    val = lambda k: var[k] if k in var else float(gint[k])
    tau = lp.NumVar(-1000.0, 100.0, "tau")
    # exact star counts and letter caps
    for i, l in enumerate(C.S):
        for y in range(14):
            terms = [C.pid(i, t) for t, w in enumerate(C.S) if y in w and t != i]
            if not terms:
                continue
            c = 1 if (y in l or C.MATE(y) in l) else 2
            lin = sum(val(k) for k in terms)
            if isinstance(lin, (int, float)):
                continue
            lp.Add(lin == c) if y in C.STARS else lp.Add(lin <= c)
    # pair caps
    nq = 0
    for i, j in C.PAIRS:
        s = len(C.S[i] & C.S[j])
        terms = []
        const = s + 0.0
        kij = C.pid(i, j)
        lin = val(kij)
        for t in range(n):
            if t in (i, j):
                continue
            a, b = C.pid(i, t), C.pid(j, t)
            fa, fb = a not in var, b not in var
            if fa and fb:
                const += gint[a] * gint[b]
            elif fa:
                if gint[a]:
                    terms.append(var[b])
            elif fb:
                if gint[b]:
                    terms.append(var[a])
            else:
                q = lp.NumVar(0.0, 1.0, "")
                lp.Add(q >= var[a] + var[b] - 1)
                terms.append(q)
                nq += 1
        if not terms and not isinstance(lin, pywraplp.Variable):
            continue
        lp.Add(sum(terms) + lin + const <= 2)
    lp.Maximize(tau)
    hist = []
    for r in range(rounds):
        st = lp.Solve()
        if st != pywraplp.Solver.OPTIMAL:
            return ("LP status %d" % st, hist)
        tv = tau.solution_value()
        g = np.array([var[k].solution_value() if k in var else gint[k] for k in range(len(C.PAIRS))])
        T, U, eT, VT, eU, VU = lam8(g)
        true8 = 8 * min(eT.min(), eU.min())
        hist.append((round(tv, 3), round(true8, 3)))
        if verbose and r % 10 == 0:
            print("    LP round %d: tau_LP %.3f, true %.3f" % (r, tv, true8), flush=True)
        if tv < -1e-6:
            return ("NO POSITIVE COMPLETION (LP bound %.3f < 0)" % tv, hist)
        if tv - true8 < 1e-3:
            return ("POSITIVE COMPLETION FOUND (relaxed), margin %.3f" % true8, hist)
        for M, ev, V, typ in ((T, eT, VT, "T"), (U, eU, VU, "U")):
            for idx in np.argsort(ev)[:4]:
                if 8 * ev[idx] > tv - 1e-6:
                    break
                x = V[:, idx]
                # 8 x^t T x = x^t (24 I - K8) x - 16 sum_{i<j} x_i x_j Gamma_ij
                lin = []
                const = float(x @ I24K @ x)
                for k, (i, j) in enumerate(C.PAIRS):
                    cij = 16.0 * x[i] * x[j]
                    if abs(cij) < 1e-12:
                        continue
                    if k in var:
                        lin.append((var[k], cij))
                    else:
                        const -= cij * gint[k]
                expr = sum(v * c for v, c in lin)
                if typ == "T":
                    lp.Add(const - expr >= tau * float(x @ x))
                else:
                    lp.Add(56.0 * float(x @ C.PiS @ x) - const + expr >= tau * float(x @ x))
    return ("UNDECIDED after %d LP rounds" % rounds, hist)


def main():
    ci, nstart = int(sys.argv[1]), int(sys.argv[2])
    secs = float(sys.argv[3]) if len(sys.argv) > 3 else 20.0
    rounds = int(sys.argv[4]) if len(sys.argv) > 4 else 200
    case = CS.all_cases()[ci]
    print("case %d %s: |P| %d |Q| %d, fixed pairs %d, relaxed pairs %d" % (ci, case, len(P), len(Q), len(FIXED), len(FREE)))
    for s in range(nstart):
        t0 = time.time()
        g = integral_start(ci, secs, 1000 + s)
        if g is None:
            print("  start %d: no integral structure" % s)
            continue
        _, _, eT, _, eU, _ = lam8(g)
        res, hist = hfix_lp(g, rounds, verbose=bool(os.environ.get("VERB")))
        print("  start %d: integral 8 lambda_min T %.3f U %.3f ; %s ; LP rounds %d ; %.0f s" % (
            s, 8 * eT.min(), 8 * eU.min(), res, len(hist), time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
