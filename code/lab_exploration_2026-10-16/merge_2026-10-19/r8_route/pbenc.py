"""Pseudo-Boolean 'sum w_i x_i <= b' (integer weights of any sign) to CNF, reduced BDD with interval memoisation
(Een-Sorensson style; my own implementation, LAB 20/10/2026).  Sound and complete for the constraint: the clauses are
  root;  n(i,c) -> n(i+1,c);  n(i,c) and y_i -> n(i+1, c - w_i)   (terminals: false if c < 0, true if c >= rest)
which every assignment satisfying the constraint can satisfy (set n(i,c) := [sum_{j>=i} w_j y_j <= c], monotone in c),
and which force the constraint (induction from the root).  Verified by brute force in selftest()."""
import itertools
import random


def pb_le(new_var, lits, weights, bound):
    """Return (clauses, ok) encoding sum w_i [lit_i] <= bound.  ok=False if trivially unsatisfiable (empty clause
    added).  new_var() must return fresh variable numbers."""
    terms = []
    b = bound
    for l, w in zip(lits, weights):
        if w == 0:
            continue
        if w < 0:                      # w x = w + |w| (not x)
            terms.append((-l, -w))
            b -= w
        else:
            terms.append((l, w))
    terms.sort(key=lambda t: -t[1])
    if b < 0:
        return [[]], False
    rest = [0] * (len(terms) + 1)
    for i in range(len(terms) - 1, -1, -1):
        rest[i] = rest[i + 1] + terms[i][1]
    if rest[0] <= b:
        return [], True
    clauses = []
    memo = [[] for _ in range(len(terms) + 1)]      # per level: list of (lo, hi, node) ; node None = TRUE, 0 = FALSE

    def build(i, c):
        """node for 'sum_{j>=i} w_j y_j <= c'; returns (node, lo, hi) with the same function on [lo, hi]."""
        if c < 0:
            return 0, -10 ** 18, -1
        if c >= rest[i]:
            return None, rest[i], 10 ** 18
        for lo, hi, nd in memo[i]:
            if lo <= c <= hi:
                return nd, lo, hi
        y, w = terms[i]
        n0, lo0, hi0 = build(i + 1, c)            # y = 0
        n1, lo1, hi1 = build(i + 1, c - w)        # y = 1
        lo, hi = max(lo0, lo1 + w), min(hi0, hi1 + w)
        if n0 is None and n1 is None:
            nd = None
        else:
            nd = new_var()
            if n0 is not None:
                clauses.append([-nd, n0] if n0 != 0 else [-nd])
            if n1 is not None:
                clauses.append([-nd, -y, n1] if n1 != 0 else [-nd, -y])
        memo[i].append((lo, hi, nd))
        return nd, lo, hi

    root, _, _ = build(0, b)
    if root == 0:
        return [[]], False
    if root is not None:
        clauses.append([root])
    return clauses, True


def selftest(trials=300, seed=1):
    from pysat.solvers import Solver
    rng = random.Random(seed)
    for _ in range(trials):
        n = rng.randint(1, 7)
        lits = list(range(1, n + 1))
        ws = [rng.randint(-6, 9) for _ in range(n)]
        b = rng.randint(-8, 15)
        nv = [n]

        def nvar():
            nv[0] += 1
            return nv[0]

        cl, ok = pb_le(nvar, lits, ws, b)
        for bits in itertools.product((0, 1), repeat=n):
            truth = sum(w * x for w, x in zip(ws, bits)) <= b
            with Solver(name="minisat22", bootstrap_with=cl) as s:
                sat = s.solve(assumptions=[l if x else -l for l, x in zip(lits, bits)])
            assert sat == truth, (ws, b, bits, truth, sat)
    return True


if __name__ == "__main__":
    print("selftest", selftest())
