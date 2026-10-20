"""How local is the spectral violation of the R7 SAT witnesses?  (LAB, 20/10/2026, NOTE_BORNE_RANG section 7.)

For a witness (labels X, all adjacencies among X decided), H = 7 P_v[X, X] must satisfy 0 <= H <= 7 I and rank <= 30
in any srg(99,14,1,2) (any 7-rank).  A principal sub-block H[Y, Y] depends only on the labels of Y and the edges inside
Y, so a sub-block that is not PSD (or not <= 7I) is an exact FORBIDDEN PATTERN: a no-good clause on the edges inside Y.
This script looks for small such Y: greedy growth along the most negative eigenvector, then greedy shrinking
(remove a label while the block stays bad).  It also reports the smallest bad blocks found by exhaustive search over
all subsets of size <= smax (if cheap).
usage: python minimal_nonpsd.py <smax_exhaustive> <witness.json> ...
"""
import itertools
import json
import sys

import numpy as np

sys.path.insert(0, ".")
from borne_rang_vertex_block import local_H  # noqa: E402

TOL = 1e-9


def bad(Hs, t):
    ev = np.linalg.eigvalsh(Hs)
    return ev.min() < -TOL or ev.max() > t + TOL, ev.min(), ev.max()


def shrink(H, Y, t):
    Y = list(Y)
    changed = True
    while changed:
        changed = False
        for y in list(Y):
            Z = [z for z in Y if z != y]
            if len(Z) >= 1 and bad(H[np.ix_(Z, Z)], t)[0]:
                Y = Z
                changed = True
                break
    return Y


def main():
    smax = int(sys.argv[1])
    for path in sys.argv[2:]:
        d = json.load(open(path))
        labels = [tuple(l) for l in d["labels"]]
        m = len(labels)
        A = np.zeros((m, m))
        for i, j in d["edges"]:
            A[i, j] = A[j, i] = 1
        H, t = local_H(labels, lambda i: i ^ 1, A, 14)
        ev, V = np.linalg.eigh(H)
        z = V[:, 0]
        order = list(np.argsort(-np.abs(z)))
        Y = []
        for y in order:
            Y.append(int(y))
            if bad(H[np.ix_(Y, Y)], t)[0]:
                break
        grown = len(Y)
        Ymin = shrink(H, Y, t)
        b, lo, hi = bad(H[np.ix_(Ymin, Ymin)], t)
        # several restarts from the other negative eigenvectors
        best = Ymin
        for kv in range(1, int((ev < -TOL).sum())):
            z = V[:, kv]
            order = list(np.argsort(-np.abs(z)))
            Y = []
            for y in order:
                Y.append(int(y))
                if bad(H[np.ix_(Y, Y)], t)[0]:
                    break
            Y2 = shrink(H, Y, t)
            if len(Y2) < len(best):
                best = Y2
        b, lo, hi = bad(H[np.ix_(best, best)], t)
        ex = None
        for s in range(1, smax + 1):
            found = None
            for Y in itertools.combinations(range(m), s):
                if bad(H[np.ix_(Y, Y)], t)[0]:
                    found = Y
                    break
            if found:
                ex = (s, found)
                break
        print("%s: greedy bad block after %d labels, shrunk to %d labels (eigen min %.4f max %.4f): %s ; "
              "exhaustive search up to size %d: %s"
              % (path.replace("\\", "/").split("/")[-1], grown, len(best), lo, hi,
                 [labels[i] for i in sorted(best)], smax,
                 "none" if ex is None else "size %d %s" % (ex[0], [labels[i] for i in ex[1]])), flush=True)


if __name__ == "__main__":
    main()
