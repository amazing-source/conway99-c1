"""For each outer line n = {y, y'}: the functional on the 4 m-block labels (2y, 2y', 3y, 3y') that annihilates all
profiles of ker T_S (exact), together with the local adjacency among those 4 labels and to the C4 / l-block of n.
usage: python block_functional.py <json>"""
import json, sys
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
nm = lambda s: "".join(format(c, 'x') for c in sorted(s))
adj = lambda s, t: (idx[frozenset(s)], idx[frozenset(t)]) in E
for (a, b) in ((2, 3), (0, 1)):
    print("side stars %d,%d:" % (a, b))
    for (y, z) in LINES:
        labs = [frozenset((a, y)), frozenset((a, z)), frozenset((b, y)), frozenset((b, z))]
        P = [[v[idx[s]] for s in labs] for v in Kb]
        R, piv = rref(P)
        ann = nullspace(R) if R else [[F(1) if i == j else F(0) for i in range(4)] for j in range(4)]
        edges = [(nm(p), nm(q)) for i, p in enumerate(labs) for q in labs[i + 1:] if adj(p, q)]
        print("   line %d%d: profile dim %d, annihilator %s, block edges %s" % (y, z, len(R), [[str(x) for x in w] for w in ann], edges))
