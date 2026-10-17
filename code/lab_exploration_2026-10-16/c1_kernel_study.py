"""Where does the kernel of a c = 1 four-star block come from? (exploration, LAB 17/10/2026)
For c(l) = 1 the root block T_l (24 labels of l) has kernel span(z_0, z_1), rank 22, so
    nu(T_S) = 2 + dim ker S_Q,   S_Q = T_QQ - T_Ql T_l^+ T_lQ  (Q = the 20 labels 2x, 3x, x in 4..13),
and Conway needs nu >= 14, i.e. dim ker S_Q >= 12 (rank S_Q <= 8).  ker S_Q always contains 1_{2*}, 1_{3*} (images
of the stars z_2, z_3).  For the positive data blocks with a c = 1 side, this script reports nu, dim ker S_Q, c(m), the
rectangle profiles, and an integral basis of ker T_S (exact, sympy) with the structure of each extra vector:
support size, values, support on root l / root m / cross labels, letters, invariance under (0 1), (2 3).
usage: python c1_kernel_study.py <distinct cache.jsonl> [min nullity] [max blocks]"""
import itertools
import json
import os
import sys
from collections import Counter

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "stars_rank_2026-10-14"))
from stars_rank import kval  # noqa: E402
from gg_test import orient, line_graph, components  # noqa: E402

nm = lambda l: "".join("%x" % t for t in sorted(l))


def profile(L, EE, a0, a1, roots):
    out = []
    for rt in roots:
        q = [frozenset((r, t)) for r in (a0, a1) for t in rt]
        out.append(sum(1 for x, y in itertools.combinations(q, 2) if frozenset((x, y)) in EE))
    return out


def main():
    minnu = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    maxb = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    found = 0
    stats = Counter()
    for line in open(sys.argv[1]):
        d = json.loads(line)
        if len(d["labels"]) != 44:
            continue
        S0 = [frozenset(x) for x in d["labels"]]
        for side in (0, 1):
            L, EE = orient(S0, d["edges"], side)
            V, pos, A = line_graph(L, EE)
            if not all(sum(r) == 3 for r in A) or components(A) != 1:
                continue
            S = sorted(L, key=lambda l: (min(l), max(l)))
            n = len(S)
            G = np.zeros((n, n), dtype=np.int64)
            for i, j in itertools.combinations(range(n), 2):
                if frozenset((S[i], S[j])) in EE:
                    G[i, j] = G[j, i] = 1
            K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
            T8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
            if np.linalg.eigvalsh(T8 / 8.0)[0] < -1e-9:
                continue
            nu = n - np.linalg.matrix_rank(T8.astype(float), tol=1e-6)
            stats[nu] += 1
            if nu < minnu or found >= maxb:
                continue
            found += 1
            # c(m)
            Lm, EEm = orient(S0, d["edges"], 1 - side)
            Vm, posm, Am = line_graph(Lm, EEm)
            cm = components(Am) if all(sum(r) == 3 for r in Am) else -1
            el = profile(L, EE, 0, 1, [(2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)])
            em = profile(L, EE, 2, 3, [(0, 1), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13)])
            print("block %d (side %d): nu %d, c(m) %d, e at l %s, e at m %s" % (found, side, nu, cm, el, em))
            Ker = sp.Matrix(T8.tolist()).nullspace()
            # integral basis, reduced against stars
            stars = [np.array([1 if y in l else 0 for l in S]) for y in (0, 1, 2, 3)]
            vecs = []
            for v in Ker:
                den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
                w = np.array([int(x * den) for x in v], dtype=np.int64)
                g = np.gcd.reduce(np.abs(w[w != 0])) if np.any(w) else 1
                vecs.append(w // g)
            # greedy small-support basis: LLL-like via sympy is heavy; print the given basis with descriptors
            rootl = [i for i, l in enumerate(S) if l & {0, 1}]
            rootm = [i for i, l in enumerate(S) if l & {2, 3}]
            cross = [i for i, l in enumerate(S) if (l & {0, 1}) and (l & {2, 3})]
            sw01 = [S.index(frozenset({0: 1, 1: 0}.get(t, t) for t in l)) for l in S]
            sw23 = [S.index(frozenset({2: 3, 3: 2}.get(t, t) for t in l)) for l in S]
            M = np.array(vecs).T.astype(float)
            Ms = np.array(stars).T.astype(float)
            extra_rank = np.linalg.matrix_rank(np.hstack([M, Ms])) - np.linalg.matrix_rank(Ms)
            print("   kernel dim %d = 4 stars + %d extra" % (len(vecs), extra_rank))
            for k, w in enumerate(vecs):
                sup = np.nonzero(w)[0]
                inl = sum(1 for i in sup if i in rootl and i not in cross)
                inm = sum(1 for i in sup if i in rootm and i not in cross)
                inc = sum(1 for i in sup if i in cross)
                e01 = "even" if all(w[sw01[i]] == w[i] for i in range(n)) else ("odd" if all(w[sw01[i]] == -w[i] for i in range(n)) else "mixed")
                e23 = "even" if all(w[sw23[i]] == w[i] for i in range(n)) else ("odd" if all(w[sw23[i]] == -w[i] for i in range(n)) else "mixed")
                vals = Counter(int(x) for x in w[sup])
                print("    v%d: |supp| %d (l-only %d, m-only %d, cross %d), values %s, (0 1) %s, (2 3) %s" % (
                    k, len(sup), inl, inm, inc, dict(vals), e01, e23))
                if len(sup) <= 16:
                    print("        " + " ".join("%s:%+d" % (nm(S[i]), w[i]) for i in sup))
    print("nullity distribution of positive c = 1 sides:", dict(sorted(stats.items())))


if __name__ == "__main__":
    main()
