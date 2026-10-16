"""Exact determinant of 3I - A_H for H = N(l) u Y_r' (46 vertices) on c(l) = 1 sides, with the number of spanning trees
tau(G_l) of the cubic graph, and factorisations; checks mod small primes.
usage: python h46_det.py <distinct cache.jsonl> <cle3_sides.jsonl> [max]"""
import json, sys, collections
import numpy as np
import sympy as sp
MATE = lambda i: i ^ 1


def hmat(S, E, p, q, rr):
    letters = [("L", s) for s in range(14) if s not in (p, q)]
    Gv = letters + [l for l in S if l & {p, q}]
    Y = [l for l in S if rr in l and not (l & {p, q})]
    V = Gv + Y
    def adj(a, b):
        if isinstance(a, tuple) and isinstance(b, tuple): return MATE(a[1]) == b[1]
        if isinstance(a, tuple): return a[1] in b
        if isinstance(b, tuple): return b[1] in a
        return frozenset((a, b)) in E
    return np.array([[1 if i != j and adj(a, b) else 0 for j, b in enumerate(V)] for i, a in enumerate(V)])


if __name__ == "__main__":
    want = {json.loads(x)["src"] for x in open(sys.argv[2]) if json.loads(x)["c"] == 1}
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    seen, n = set(), 0
    mods = collections.Counter()
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if d["src"] not in want or n >= mx:
            continue
        L = [frozenset(x) for x in d["labels"]]
        E = set(frozenset((frozenset(a), frozenset(b))) for a, b in d["edges"])
        S = [l for l in L if l & {0, 1, 2, 3}]
        for (p, q), (rA, rB) in (((0, 1), (2, 3)), ((2, 3), (0, 1))):
            A = hmat(S, E, p, q, rA)
            AG = A[:36, :36]
            if np.sum(np.linalg.eigvalsh(3 * np.eye(36) - AG) < 1e-9) != 1:
                continue
            for rr in (rA, rB):
                AH = sp.Matrix(hmat(S, E, p, q, rr).tolist())
                det = (3 * sp.eye(46) - AH).det()
                Lg = sp.Matrix((3 * np.eye(36, dtype=int) - AG).tolist())
                tau = Lg[1:, 1:].det()
                key = (int(det), int(tau))
                if key in seen:
                    continue
                seen.add(key)
                n += 1
                f = sp.factorint(int(det))
                ft = sp.factorint(int(tau))
                print("det(3I - A_H) = %d = %s ; tau(G_l) = %s ; det/tau = %s" % (det, f, ft, sp.Rational(int(det), int(tau))))
                for pr in (2, 3, 5, 7, 11, 13):
                    mods[(pr, int(det) % pr == 0)] += 1
    print("distinct (det, tau) pairs:", n)
    print("divisibility of det by p (p, divisible?): count", dict(sorted(mods.items())))
