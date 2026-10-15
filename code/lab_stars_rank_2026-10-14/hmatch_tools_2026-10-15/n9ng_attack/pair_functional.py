"""Annihilators of the kernel profiles restricted to the m-blocks of two outer lines (8 labels), modulo the two DO
functionals; printed in the basis (2y,2y',3y,3y',2z,2z',3z,3z').  usage: python pair_functional.py <json>"""
import json, sys, itertools
from fractions import Fraction as F
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
from exact_lin import rref, nullspace
f = sys.argv[1]
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
E = set()
for a, b in d["edges"]: E.add((a, b)); E.add((b, a))
T = [[(3 if i == j else 0) - (1 if (i, j) in E else 0) - F(int(round(8 * kval(S[i], S[j]))), 8) for j in range(n)] for i in range(n)]
Kb = nullspace(T)
LINES = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
a, b = 2, 3
for i1, i2 in itertools.combinations(range(5), 2):
    (y, yp), (z, zp) = LINES[i1], LINES[i2]
    labs = [frozenset(p) for p in ((a, y), (a, yp), (b, y), (b, yp), (a, z), (a, zp), (b, z), (b, zp))]
    P = [[v[idx[s]] for s in labs] for v in Kb]
    R, piv = rref(P)
    ann = nullspace(R)
    # reduce modulo DO functionals: put DO first and RREF
    do1 = [F(1), F(-1), F(-1), F(1), 0, 0, 0, 0]; do2 = [0, 0, 0, 0, F(1), F(-1), F(-1), F(1)]
    red = []
    for v in ann:
        v2 = [v[k] - v[0] * do1[k] - v[4] * do2[k] for k in range(8)]
        if any(x != 0 for x in v2): red.append(v2)
    extra, _ = rref(red) if red else ([], [])
    # make the extra ones orthogonal-ish: print as is
    print("lines %d%d,%d%d: profile dim %d; extra annihilators %s" % (y, yp, z, zp, len(R), [[str(x) for x in r] for r in extra]))
