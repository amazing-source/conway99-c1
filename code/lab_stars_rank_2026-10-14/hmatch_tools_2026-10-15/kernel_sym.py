"""Symmetry group of a kernel class (LAB 15/10/2026, task T3: why does only the obj53 class contain broken structures?).

Frame group: letter permutations g preserving mates and the set {0,1,2,3} (so g permutes the two lines l = {0,1},
m = {2,3}: the dihedral group D4 of order 8) and acting on the five outer lines by any signed permutation (order
2^5 5! = 3840); total 30 720.  g acts on the 44 labels.  For a structure, the kernel N = ker 8T (exact) and the
structure itself: we count the g with gN = N (kernel symmetry) and the g with g Gamma g^-1 = Gamma (automorphisms).
A class can contain g Gamma for every kernel symmetry g, so a large kernel group beyond the structure's own group
produces many class members.
usage: python kernel_sym.py <json> [...]"""
import itertools
import json
import sys
from fractions import Fraction as Fr

sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int


def rref(vecs, n):
    A = [[Fr(x) for x in v] for v in vecs]
    r = 0
    for c in range(n):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        r += 1
    return tuple(tuple(row) for row in A[:r])


# D4 on the star letters (as permutations of 0..3 preserving the pairing {0,1},{2,3})
d4 = []
for p in itertools.permutations(range(4)):
    if {frozenset((p[0], p[1])), frozenset((p[2], p[3]))} == {frozenset((0, 1)), frozenset((2, 3))}:
        d4.append(p)
outer_lines = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
outer = []
for perm in itertools.permutations(range(5)):
    for flips in itertools.product((0, 1), repeat=5):
        g = {}
        for k, (a, b) in enumerate(outer_lines):
            ta, tb = outer_lines[perm[k]]
            if flips[k]:
                ta, tb = tb, ta
            g[a], g[b] = ta, tb
        outer.append(g)
group = []
for p in d4:
    for g in outer:
        full = dict(g)
        for i in range(4):
            full[i] = p[i]
        group.append(full)
assert len(group) == 30720
import numpy as np
for f in sys.argv[1:]:
    d = json.load(open(f))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    idx = {s: i for i, s in enumerate(S)}
    G = np.zeros((n, n), dtype=np.int64)
    for a, b in d["edges"]:
        G[a, b] = G[b, a] = 1
    K8 = np.array([[int(round(8 * kval(S[a], S[b]))) for b in range(n)] for a in range(n)], dtype=np.int64)
    M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
    N = np.array(nullspace_int(M8.tolist()), dtype=np.int64).T          # n x nullity, integer
    ksym = aut = 0
    kd4 = {}
    for g in group:
        perm = np.array([idx[frozenset(g[y] for y in s)] for s in S])  # label i -> label perm[i]
        inv = np.argsort(perm)
        if np.array_equal(G[np.ix_(inv, inv)], G):
            aut += 1
        gN = N[inv, :]                                                # (gv)[perm[i]] = v[i]
        if not np.any(M8 @ gN):
            ksym += 1
            t = tuple(g[i] for i in range(4))
            kd4[t] = kd4.get(t, 0) + 1
    print("%s: nullity %d, |Aut(structure) in frame group| = %d, |kernel symmetry group| = %d, star parts "
          "(D4 element: count): %s" % (f, N.shape[1], aut, ksym, sorted(kd4.items())), flush=True)
