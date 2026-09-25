"""notes/109: second-order slot identities.  For class pairs P, R (d_P(v) = |N(v) cap Q_P| for v in Gamma_2(x)):
    sum_v d_P(v) d_R(v) = 32 - e_PR (P, R disjoint) ; 24 - e_PR (|P cap R| = 1) ; 64 - 2 e_PP (P = R),
where e_PR = number of edges between Q_P and Q_R (e_PP internal).  These are (H^2) summed over Q_P x Q_R.
d_P(v) is known when v's pair shares a class with P (special edges) and is the slot variable n_P(v) otherwise.
Test: after first-order propagation, enumerate the integer solutions of the linear system in the remaining free
variables and check the quadratic identities."""
import itertools, sys
from collections import defaultdict
from slot_calculus import build, propagate, PAIRS, VERT, cls
from slot_tests import configs

def special_d(cfg, v, P):
    """number of neighbours of v in Q_P through special edges (v's pair shares a class with P or equals P)"""
    return sum(1 for z in cfg.specials(v) if cls(z) == P)

def analyse(cfg, verbose=False):
    var, lo, hi, eqs, inc = build(cfg)
    ok, lo, hi, log = propagate(lo, hi, eqs)
    if not ok:
        return 'first order refutes'
    free = [j for j in range(len(lo)) if lo[j] < hi[j]]
    idx = {j: k for k, j in enumerate(free)}
    # linear system restricted to free vars
    rows = []
    for coef, rhs, lab in eqs:
        r = {}
        c = rhs
        for j, a in coef.items():
            if j in idx:
                r[j] = a
            else:
                c -= a * lo[j]
        if r:
            rows.append((r, c))
    # enumerate solutions by backtracking with interval pruning
    sols = []
    order = sorted(free, key=lambda j: -sum(1 for r, c in rows if j in r))
    cur = {}
    def feasible_partial():
        for r, c in rows:
            s_lo = s_hi = 0
            for j, a in r.items():
                if j in cur:
                    s_lo += a * cur[j]; s_hi += a * cur[j]
                else:
                    s_lo += a * (lo[j] if a > 0 else hi[j]); s_hi += a * (hi[j] if a > 0 else lo[j])
            if not (s_lo <= c <= s_hi):
                return False
        return True
    def rec(k):
        if len(sols) > 200000:
            return
        if k == len(order):
            sols.append(dict(cur)); return
        j = order[k]
        for val in range(lo[j], hi[j] + 1):
            cur[j] = val
            if feasible_partial():
                rec(k + 1)
            del cur[j]
    rec(0)
    if verbose:
        print('  free variables', len(free), ' integer solutions of the linear system:', len(sols))
    # quadratic identities
    inv = {j: key for key, j in var.items()}
    def dvec(sol, P):
        d = {}
        for v in VERT:
            S = cls(v)
            if S == P or (S & P):
                d[v] = special_d(cfg, v, P)
            else:
                j = var[(v, P)]
                d[v] = sol.get(j, lo[j])
        return d
    good = 0
    for sol in sols:
        D = {P: dvec(sol, P) for P in PAIRS}
        e = {}
        okq = True
        for P in PAIRS:
            for R in PAIRS:
                eP = sum(D[R][v] for v in VERT if cls(v) == P)
                e[(P, R)] = eP
        for P in PAIRS:
            for R in PAIRS:
                lhs = sum(D[P][v] * D[R][v] for v in VERT)
                if P == R:
                    rhs = 64 - e[(P, P)]          # e[(P,P)] counts ordered internal adjacencies = 2 e_PP
                elif not (P & R):
                    rhs = 32 - e[(P, R)]
                else:
                    rhs = 24 - e[(P, R)]
                if lhs != rhs:
                    okq = False; break
            if not okq:
                break
        if okq:
            good += 1
    return f'linear solutions {len(sols)}, passing the quadratic identities {good}'

if __name__ == '__main__':
    tw = {(0, 0): {2, 3}, (1, 0): {2, 3}}
    for k, cfg in enumerate(configs(tw)):
        print('L14 |C|=2 config', k, ':', analyse(cfg, verbose=True), flush=True)
