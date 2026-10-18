"""Independent re-check of the integer Gram verdicts of cle3_gram.py (LAB, 18/10/2026).

Same mathematical system, written again from its statement (not from cle3_gram's code), solved by another solver
(HiGHS through scipy.optimize.milp) with another exact PSD test (own Fraction LDL^t, not Codex's psd_or_witness):
  R_ee in {4, 6, 8} (one-hot), R_ef integer; R_ef in [-8, 0] on a shared line inside one component, R_ef = 0 on a
  shared line across two components, R_ef in [-8, 4] on disjoint pairs; R_ef >= -floor(sqrt(R_ee R_ff));
  for every component node (r, S) and every rectangle f: sum_{j in S} R_{rj, f} = 0;
  every proper cut U of a component with |S| >= 3: sum_{e in U, f in S - U} R_ef <= -2;  trace R <= 28 dim ker C;
  lazily: R >= 0 and 28 I - R >= 0 by exact integer witness cuts.
A FEASIBLE answer is re-verified exactly in Python.  HiGHS works in floating point: an INFEASIBLE answer here is a
second opinion, not a certificate.
usage: py -3 cle3_gram_milp_check.py <seconds per template> <output.json> <file.jsonl>... [--limit n] [--seed s]"""
import json
import math
import random
import sys
import time
from fractions import Fraction
from itertools import combinations
from math import lcm

import numpy as np
from scipy.optimize import LinearConstraint, milp, Bounds

DIAG = (4, 6, 8)


def psd_witness(M):
    """None if the symmetric Fraction matrix M is PSD, else an integer vector q with q^t M q < 0."""
    n = len(M)
    A = [list(row) for row in M]
    basis = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    found = None
    for i in range(n):
        if A[i][i] < 0:
            found = basis[i]
            break
        if A[i][i] == 0:
            j = next((j for j in range(i + 1, n) if A[i][j] != 0), None)
            if j is not None:
                t = -(A[j][j] + 1) / (2 * A[i][j])
                found = [x + t * y for x, y in zip(basis[j], basis[i])]
                break
            continue
        p = A[i][i]
        for j in range(i + 1, n):
            f = A[i][j] / p
            if f:
                basis[j] = [x - f * y for x, y in zip(basis[j], basis[i])]
        for j in range(i + 1, n):
            for k in range(i + 1, n):
                A[j][k] = A[j][k] - A[j][i] * A[i][k] / p
    if found is None:
        return None
    d = lcm(*[x.denominator for x in found])
    q = [int(x * d) for x in found]
    val = sum(q[a] * M[a][b] * q[b] for a in range(n) for b in range(n))
    assert val < 0, "witness check failed"
    return q


def nullity(rows, m):
    A = [[Fraction(x) for x in r] for r in rows]
    rank, col = 0, 0
    for col in range(m):
        piv = next((i for i in range(rank, len(A)) if A[i][col] != 0), None)
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        for i in range(len(A)):
            if i != rank and A[i][col] != 0:
                f = A[i][col] / A[rank][col]
                A[i] = [x - f * y for x, y in zip(A[i], A[rank])]
        rank += 1
    return m - rank


def check(t, seconds):
    edges = [tuple(e) for e in t["nongrid_edges"]]
    m = len(edges)
    comp = {}                                   # (root, other root) -> component id
    nodes = []
    for r, blocks in enumerate(t["nontrivial_component_groups"]):
        for B in blocks:
            for j in B:
                comp[(r, j)] = len(nodes)
            nodes.append((r, tuple(B)))
    eidx = {e: i for i, e in enumerate(edges)}
    # variable layout: 3 one-hot per diagonal, then one integer per pair e < f
    pairs = list(combinations(range(m), 2))
    pid = {p: 3 * m + i for i, p in enumerate(pairs)}
    nv = 3 * m + len(pairs)
    lb, ub = np.zeros(nv), np.ones(nv)
    for (e, f) in pairs:
        common = set(edges[e]) & set(edges[f])
        if common:
            r = next(iter(common))
            a, b = (set(edges[e]) - {r}).pop(), (set(edges[f]) - {r}).pop()
            lo, hi = (-8, 0) if comp[(r, a)] == comp[(r, b)] else (0, 0)
        else:
            lo, hi = -8, 4
        lb[pid[(e, f)]], ub[pid[(e, f)]] = lo, hi
    rows, rlo, rhi = [], [], []

    def entry(e, f):                            # linear form of R_ef as {var: coef}
        if e == f:
            return {3 * e + k: DIAG[k] for k in range(3)}
        return {pid[(min(e, f), max(e, f))]: 1}

    def add(form, lo, hi):
        row = np.zeros(nv)
        for v, c in form.items():
            row[v] += c
        rows.append(row)
        rlo.append(lo)
        rhi.append(hi)

    for e in range(m):                          # one-hot
        add({3 * e + k: 1 for k in range(3)}, 1, 1)
    for r, B in nodes:                          # C R = 0
        inc = [eidx[tuple(sorted((r, j)))] for j in B]
        for f in range(m):
            form = {}
            for e in inc:
                for v, c in entry(e, f).items():
                    form[v] = form.get(v, 0) + c
            add(form, 0, 0)
        if len(inc) >= 3:                       # connectivity cuts
            first = inc[0]
            for size in range(1, len(inc)):
                for U in combinations(inc, size):
                    if first not in U:
                        continue
                    rest = [f for f in inc if f not in U]
                    form = {}
                    for e in U:
                        for f in rest:
                            for v, c in entry(e, f).items():
                                form[v] = form.get(v, 0) + c
                    add(form, -np.inf, -2)
    inc_rows = []
    for r, B in nodes:
        row = [0] * m
        for j in B:
            row[eidx[tuple(sorted((r, j)))]] = 1
        inc_rows.append(row)
    dimker = nullity(inc_rows, m)
    form = {}
    for e in range(m):
        for v, c in entry(e, e).items():
            form[v] = form.get(v, 0) + c
    add(form, -np.inf, 28 * dimker)
    for (e, f) in pairs:                        # 2x2 minors, lower side (upper bounds are <= 4 <= sqrt(16))
        for a, p in enumerate(DIAG):
            for b, q in enumerate(DIAG):
                F = math.isqrt(p * q)
                if F >= 8:
                    continue
                add({pid[(e, f)]: 1, 3 * e + a: -8, 3 * f + b: -8}, -F - 16, np.inf)
    integrality = np.ones(nv)
    t0, cuts = time.monotonic(), 0
    while True:
        rem = seconds - (time.monotonic() - t0)
        if rem <= 0:
            return {"status": "UNKNOWN", "cuts": cuts, "dim_ker_C": dimker}
        res = milp(np.zeros(nv), integrality=integrality, bounds=Bounds(lb, ub),
                   constraints=LinearConstraint(np.array(rows), np.array(rlo), np.array(rhi)),
                   options={"time_limit": rem, "presolve": True})
        if res.status == 2:
            return {"status": "INFEASIBLE", "cuts": cuts, "dim_ker_C": dimker}
        if res.x is None:
            return {"status": "UNKNOWN", "cuts": cuts, "dim_ker_C": dimker, "highs": res.message}
        x = np.rint(res.x).astype(int)
        R = [[0] * m for _ in range(m)]
        for e in range(m):
            assert sum(x[3 * e:3 * e + 3]) == 1
            R[e][e] = sum(DIAG[k] * x[3 * e + k] for k in range(3))
        for (e, f) in pairs:
            R[e][f] = R[f][e] = int(x[pid[(e, f)]])
        # exact re-verification of the linear part on the rounded point
        for row, lo, hi in zip(rows, rlo, rhi):
            val = float(np.dot(row, x))
            assert lo - 1e-9 <= val <= hi + 1e-9, "rounded point violates a linear row"
        Rf = [[Fraction(v) for v in row] for row in R]
        q = psd_witness(Rf)
        if q is not None:
            form = {}
            for e in range(m):
                for f in range(m):
                    if q[e] and q[f]:
                        for v, c in entry(e, f).items():
                            form[v] = form.get(v, 0) + c * q[e] * q[f]
            add(form, 0, np.inf)
            cuts += 1
            continue
        U = [[Fraction(28 * (e == f)) - Rf[e][f] for f in range(m)] for e in range(m)]
        q = psd_witness(U)
        if q is not None:
            form = {}
            for e in range(m):
                for f in range(m):
                    if q[e] and q[f]:
                        for v, c in entry(e, f).items():
                            form[v] = form.get(v, 0) + c * q[e] * q[f]
            add(form, -np.inf, 28 * sum(z * z for z in q))
            cuts += 1
            continue
        return {"status": "FEASIBLE", "cuts": cuts, "dim_ker_C": dimker, "R": R}


def main():
    secs, out, files = float(sys.argv[1]), sys.argv[2], [a for a in sys.argv[3:] if a.endswith(".jsonl")]
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else None
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 0
    items = [(p, n, json.loads(line)) for p in files for n, line in enumerate(open(p))]
    if limit is not None and limit < len(items):
        items = random.Random(seed).sample(items, limit)
    counts, recs, t0 = {}, [], time.time()
    for p, n, t in items:
        r = check(t, secs) if t["nongrid_edges"] else {"status": "FEASIBLE", "note": "empty system"}
        counts[r["status"]] = counts.get(r["status"], 0) + 1
        recs.append({"file": p, "line": n, "canonical": t["canonical"], "graph_mask": t["graph_mask"], **r})
    json.dump({"counts": counts, "records": recs}, open(out, "w"), default=int)
    print(json.dumps({"counts": counts, "templates": len(items), "seconds": round(time.time() - t0, 1)}))


if __name__ == "__main__":
    main()
