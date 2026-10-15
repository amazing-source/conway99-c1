"""Square class of 8T_S4 split along the rational eigenspaces of T (LAB 15/10/2026, SQ30 mechanism hunt).

T is symmetric, so Q^44 = (+) E_lambda (rational eigenvalues, exact eigenspaces) (+) E_rest (the sum of the eigenspaces of
the irrational eigenvalues, a rational subspace), orthogonal for the standard product and for T.  Hence, in Q*/Q*^2,
    class(T|range) = prod_{lambda != 0} [lambda^{m_lambda} * class(I|E_lambda)] * class(T|E_rest),
class(I|E) = class of the standard Gram determinant of a rational basis of E.  Printed: the rational eigenvalues with
multiplicity and class(I|E), the class of T on E_rest (deduced) and its dimension.
usage: python eig_class.py <bundle json> [max objects] [stride]"""
import json
import sys

import numpy as np

from stars_rank import kval
from cls_decomp import nonzero_class, nullspace_int, sqclass, fmt, mul


def gram_class(B):
    G = [[sum(x * y for x, y in zip(u, v)) for v in B] for u in B]
    return nonzero_class(G)[1]


def main():
    d = json.load(open(sys.argv[1]))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    structs = d["structures"] if "structures" in d else [d]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else len(structs)
    stride = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    K8 = [[int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)]
    tally = {}
    for k in range(0, min(mx * stride, len(structs)), stride):
        s = structs[k]
        G = [[0] * n for _ in range(n)]
        for i, j in s["edges"]:
            G[i][j] = G[j][i] = 1
        M = [[(24 if a == b else 0) - 8 * G[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
        rT, cT = nonzero_class(M)
        ev = np.linalg.eigvalsh(np.array(M, dtype=float) / 8)
        cands = sorted({round(8 * x) for x in ev if abs(8 * x - round(8 * x)) < 1e-6 and round(8 * x) > 0})
        parts = []
        acc = (1, (), 1)
        used = 0
        for c8 in cands:
            B = nullspace_int([[M[a][b] - (c8 if a == b else 0) for b in range(n)] for a in range(n)])
            if not B:
                continue
            m = len(B)
            used += m
            cE = gram_class(B)
            lam = c8 / 8
            contrib = mul(sqclass(c8) if m % 2 else (1, (), 1), cE)     # (8 lambda)^m: the 8^m is irrelevant only
            if m % 2:                                                    # for the full product (8^30 square), so
                contrib = mul(contrib, sqclass(8))                       # use lambda^m = (c8/8)^m
            acc = mul(acc, contrib)
            parts.append("%g^%d[E:%s]" % (lam, m, fmt(cE)))
        rest_dim = rT - used
        crest = mul(cT, acc)      # class(T on E_rest), using 8^30 = square and class(T) = class(8T)
        key = (" ".join(parts), fmt(crest), rest_dim)
        tally[key] = tally.get(key, 0) + 1
        print("%d c=%s | class(8T) %s | %s | rest dim %d class %s" % (k, s.get("c"), fmt(cT), " ".join(parts), rest_dim,
                                                                   fmt(crest)), flush=True)
    print("TALLY (rational eigenspaces, class of T on E_rest, dim E_rest):")
    for key, c in sorted(tally.items(), key=lambda t: -t[1]):
        print("  %4d  %s" % (c, key))


if __name__ == "__main__":
    main()
