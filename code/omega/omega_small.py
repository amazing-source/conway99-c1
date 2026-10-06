"""End-to-end control of the star-complement route on small srg (exact rational arithmetic).

For srg(n,k,lam,mu) with eigenvalue r of multiplicity m, h = n - m:
  1. enumerate every graph H on h vertices (nauty geng), keep those with r not an eigenvalue, max degree <= k,
     common neighbours inside H <= lam (adjacent) / mu (non adjacent);
  2. R = (rI - A_H)^{-1}; candidate columns b in {0,1}^h with b^T R b = r, b^T R 1 = -1, |b| <= k, local lam/mu caps;
  3. compatibility: b^T R b' in {0,-1} (gives the adjacency -b^T R b');
  4. cliques of size m; build A, keep the srg; report the graphs found up to isomorphism.
"""
import itertools, subprocess, sys
from fractions import Fraction
import numpy as np
import networkx as nx
from graphs_test import paley9, petersen, clebsch, is_srg

GENG = "/tmp/solvers/nauty_src/nauty2_8_8/geng"


def inv_frac(M):
    n = len(M)
    A = [[Fraction(int(M[i][j])) for j in range(n)] + [Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for c in range(n):
        p = next((r for r in range(c, n) if A[r][c] != 0), None)
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [row[n:] for row in A]


def run(n, k, lam, mu, r, m):
    h = n - m
    out = subprocess.run([GENG, "-q", str(h), f"-D{k}"], capture_output=True, text=True).stdout.split()
    found = []
    stats = {"H": 0, "H_ok": 0, "cols": 0}
    for g6 in out:
        stats["H"] += 1
        G = nx.from_graph6_bytes(g6.encode())
        AH = nx.to_numpy_array(G, nodelist=range(h), dtype=int)
        C2 = AH @ AH
        if any(C2[i, j] > (lam if AH[i, j] else mu) for i in range(h) for j in range(i + 1, h)):
            continue
        R = inv_frac(r * np.eye(h, dtype=int) - AH)
        if R is None:
            continue
        stats["H_ok"] += 1
        R1 = [sum(row) for row in R]
        cols = []
        for bits in itertools.product((0, 1), repeat=h):
            b = [i for i in range(h) if bits[i]]
            if len(b) > k:
                continue
            if sum(R1[i] for i in b) != -1:
                continue
            if sum(R[i][j] for i in b for j in b) != r:
                continue
            # local caps: new vertex x adjacent to b: common neighbours of x and i in H
            ok = True
            for i in range(h):
                c = sum(AH[i, j] for j in b)
                if c > (lam if i in b else mu):
                    ok = False; break
            if ok:
                cols.append(b)
        stats["cols"] += len(cols)
        # compatibility graph
        Cg = nx.Graph(); Cg.add_nodes_from(range(len(cols)))
        adjv = {}
        for a, c in itertools.combinations(range(len(cols)), 2):
            val = sum(R[i][j] for i in cols[a] for j in cols[c])
            if val in (0, -1):
                Cg.add_edge(a, c); adjv[(a, c)] = -val
        for cl in nx.find_cliques(Cg):
            if len(cl) < m:
                continue
            for sub in itertools.combinations(cl, m):
                A = np.zeros((n, n), dtype=int); A[:h, :h] = AH
                for t, a in enumerate(sub):
                    for i in cols[a]:
                        A[h + t, i] = A[i, h + t] = 1
                for (t1, a), (t2, c) in itertools.combinations(enumerate(sub), 2):
                    e = adjv[(min(a, c), max(a, c))]
                    A[h + t1, h + t2] = A[h + t2, h + t1] = e
                if is_srg(A, n, k, lam, mu):
                    found.append(nx.from_numpy_array(A))
    reps = []
    for F in found:
        if not any(nx.is_isomorphic(F, E) for E in reps):
            reps.append(F)
    return stats, reps


if __name__ == "__main__":
    for name, params, ref in (("Petersen srg(10,3,0,1), r=1", (10, 3, 0, 1, 1, 5), petersen()),
                              ("Paley9 srg(9,4,1,2), r=1", (9, 4, 1, 2, 1, 4), paley9()),
                              ("Clebsch srg(16,5,0,2), r=1", (16, 5, 0, 2, 1, 10), clebsch())):
        st, reps = run(*params)
        same = [nx.is_isomorphic(F, nx.from_numpy_array(ref)) for F in reps]
        print(name, st, "graphs found up to iso:", len(reps), "isomorphic to the reference:", same, flush=True)
