"""Where do the negative eigenvalues of T_S live? (three stars 0,1,2; 14/10/2026)
For random admissible structures: the most negative eigenvector, its mass on the label classes
A_E = {0,x}, A'_E = {1,x}, B_E = {2,x} (x >= 4), {0,2}, {1,2}, {0,3}, {1,3}; and the class-quotient form
(T restricted to class-constant vectors, star directions removed).
usage: python analyze_neg.py <samples> <seed>
"""
import random
import sys

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval

CLASSES = ["A_E", "A'_E", "B_E", "{0,2}", "{1,2}", "{0,3}", "{1,3}"]


def cls(l):
    s = set(l)
    if s == {0, 2}: return 3
    if s == {1, 2}: return 4
    if s == {0, 3}: return 5
    if s == {1, 3}: return 6
    if 0 in s: return 0
    if 1 in s: return 1
    return 2


def main():
    samples, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for k in range(samples):
        S, idx, e, F = build([0, 1, 2], rng)
        sol = Solver(options={"polar": "rnd", "seed": str(rng.randrange(1, 10 ** 9))})
        for c in F.clauses:
            sol.add_clause(c)
        ok, model = sol.solve()
        n = len(S)
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if model[v]:
                G[i, j] = 1
        T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
        ev, V = np.linalg.eigh(T)
        c = V[:, 0]
        mass = np.zeros(7)
        for i, l in enumerate(S):
            mass[cls(l)] += c[i] ** 2
        # class quotient: indicator vectors of the classes
        P = np.zeros((n, 7))
        for i, l in enumerate(S):
            P[i, cls(l)] = 1
        Wq = P.T @ T @ P
        Gq = P.T @ P
        # generalised eigenvalues of (Wq, Gq)
        L = np.linalg.cholesky(Gq)
        Li = np.linalg.inv(L)
        evq = np.linalg.eigvalsh(Li @ Wq @ Li.T)
        print("sample %d: lambda_min %.4f | mass of the min eigenvector by class %s | class-quotient eigenvalues %s"
              % (k, ev[0], " ".join("%s:%.2f" % (CLASSES[q], mass[q]) for q in range(7)),
                 " ".join("%.3f" % t for t in evq)), flush=True)


if __name__ == "__main__":
    main()
