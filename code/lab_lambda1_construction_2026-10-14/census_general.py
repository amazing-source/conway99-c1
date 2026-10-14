"""Exact boundary census for ANY strongly regular graph parameters (v,k,lambda,mu) (14/10/2026).
Generalisation of work/spreadfree_243_2026-10-12/boundary_census.py (written for (243,22,1,2)): given a graph A0 and a
set R of kept vertices (all pairs meeting R kept), list all srg completions of the pairs inside F = V - R.
1. candidate rows of each free vertex f (its neighbourhood inside F): CryptoMiniSat with the linear conditions coming
   from the kept vertices r (number of common neighbours of f and r), the degree of f, and the exclusion of pairs of
   free vertices that already have all their common neighbours in R;
2. a completion = one row per free vertex, pairwise compatible (symmetry, and the number of common neighbours of two
   free vertices = lambda or mu according to their adjacency); depth-first search with propagation.
Every completion is checked afterwards (A^2 = (k-mu) I + (lambda-mu) A + mu J) by the caller.
Environment PYLIB = directory of pycryptosat."""
import collections
import itertools
import os
import sys
import time

import numpy as np

if os.environ.get("PYLIB"):
    sys.path.insert(0, os.environ["PYLIB"])
import pycryptosat

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import row_census as RC


def rows_of(adj, R, Rs, F, f0, cap, k, lam, mu):
    var = {g: i + 1 for i, g in enumerate(v for v in F if v != f0)}
    nv = [len(var)]
    cls = []

    def new():
        nv[0] += 1
        return nv[0]
    for r in R:
        lits = [var[g] for g in sorted(adj[r] - Rs) if g != f0]
        RC.counter(cls.append, new, lits, (lam if f0 in adj[r] else mu) - len(adj[r] & adj[f0] & Rs))
    RC.counter(cls.append, new, list(var.values()), k - len(adj[f0] & Rs))
    for g, h in itertools.combinations(sorted(var), 2):
        c = len(adj[g] & adj[h] & Rs)
        if c >= max(lam, mu) or (c > lam and c == mu):
            cls.append([-var[g], -var[h]])
    s = pycryptosat.Solver()
    s.add_clauses(cls)
    rows = []
    while len(rows) <= cap:
        sat, sol = s.solve()
        if not sat:
            return rows
        N = [g for g in var if sol[var[g]]]
        rows.append(N)
        s.add_clause([-var[g] for g in N])
    return None


def completions(A0, R, seconds, k, lam, mu, maxsol=5000, rowcap=6000, log=None):
    n = len(A0)
    Rs = set(R)
    F = [v for v in range(n) if v not in Rs]
    NF = len(F)
    pos = {v: i for i, v in enumerate(F)}
    adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]
    t0 = time.time()
    cand = []
    for f in F:
        rows = rows_of(adj, R, Rs, F, f, rowcap, k, lam, mu)
        if rows is None:
            return [], "too many candidate rows (more than %d at vertex %d)" % (rowcap, f), {}
        cand.append([sum(1 << pos[g] for g in N) for N in rows])
        if log:
            log("   row list of vertex %d: %d rows (%.0f s)" % (f, len(rows), time.time() - t0))
        if not rows:
            return [], "complete", {"rows": 0}
    info = {"rows": sum(len(c) for c in cand), "rows_max": max(len(c) for c in cand), "rows_seconds": time.time() - t0}
    K = [[len(adj[F[p]] & adj[F[q]] & Rs) for q in range(NF)] for p in range(NF)]
    deadline = time.time() + seconds
    sols = []
    stats = collections.Counter()

    def propagate(lists, fixed, p, N):
        queue = [(p, N)]
        while queue:
            p, N = queue.pop()
            fixed[p] = N
            lists[p] = [N]
            for q in range(NF):
                if q == p:
                    continue
                a = (N >> q) & 1
                need = (lam if a else mu) - K[p][q]
                if q in fixed:
                    M = fixed[q]
                    if ((M >> p) & 1) != a or (N & M).bit_count() != need:
                        return False
                    continue
                L = [M for M in lists[q] if ((M >> p) & 1) == a and (N & M).bit_count() == need]
                if not L:
                    return False
                if len(L) < len(lists[q]):
                    lists[q] = L
                    if len(L) == 1 and all(qq != q for qq, _ in queue):
                        queue.append((q, L[0]))
        return True

    def search(lists, fixed):
        if stats["stop"]:
            return
        if time.time() > deadline or len(sols) >= maxsol:
            stats["stop"] = 1
            return
        if len(fixed) == NF:
            sols.append(dict(fixed))
            return
        stats["nodes"] += 1
        q = min((len(lists[v]), v) for v in range(NF) if v not in fixed)[1]
        for M in lists[q]:
            l2 = list(lists)
            f2 = dict(fixed)
            if propagate(l2, f2, q, M):
                search(l2, f2)
            if stats["stop"]:
                return
    lists = list(cand)
    fixed = {}
    ok = True
    for p in range(NF):
        if len(lists[p]) == 1 and p not in fixed:
            if not propagate(lists, fixed, p, lists[p][0]):
                ok = False
                break
    if ok:
        search(lists, fixed)
    out = []
    for sol in sols:
        A = A0.copy()
        for p, M in sol.items():
            for q in range(NF):
                A[F[p], F[q]] = (M >> q) & 1
        out.append(A)
    info["nodes"] = stats["nodes"]
    info["search_seconds"] = time.time() - t0 - info["rows_seconds"]
    return out, ("NOT FINISHED (limit)" if stats["stop"] else "complete"), info
