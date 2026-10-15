"""Even-sector kernel of an h-invariant four-star structure, reduced modulo the side relations.
coords: a_y (u_y = 1_0y + 1_1y), b_y (g_y = 1_2y + 1_3y), y = 4..13, alpha (p = 1_02 + 1_13), beta (q = 1_03 + 1_12).
usage: python even_kernel_view.py <json>"""
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
OUT = list(range(4, 14))
names = ["a%d" % y for y in OUT] + ["b%d" % y for y in OUT] + ["al", "be"]
cols = []
for y in OUT: cols.append([idx[frozenset((0, y))], idx[frozenset((1, y))]])
for y in OUT: cols.append([idx[frozenset((2, y))], idx[frozenset((3, y))]])
cols.append([idx[frozenset((0, 2))], idx[frozenset((1, 3))]]); cols.append([idx[frozenset((0, 3))], idx[frozenset((1, 2))]])
A = [[sum(T[i][j] for i in ci for j in cj) for cj in cols] for ci in cols]
# parts of H_l / H_m from the two-star kernels (lines = mate pairs)
def parts(stars):
    lab = [i for i in range(n) if S[i] & set(stars)]
    Ns = nullspace([[T[i][j] for j in lab] for i in lab])
    return len(Ns) - 1
cl, cm = parts((0, 1)), parts((2, 3))
K = nullspace(A)
print(f, "c = (%d,%d), even nullity %d" % (cl, cm, len(K)))
# reorder: put one letter of each outer line first (a then b), so side relations take those pivots
first = [names.index("a%d" % y) for y in OUT[::2]] + [names.index("b%d" % y) for y in OUT[::2]]
rest = [i for i in range(22) if i not in first]
order = first + rest
Kp = [[v[i] for i in order] for v in K]
R, piv = rref(Kp)
print("      " + " ".join("%4s" % names[i] for i in order))
for row in R:
    print("      " + " ".join("%4s" % (str(x) if x != 0 else ".") for x in row))
print("A (even Gram, x2 normalisation):")
print("      " + " ".join("%5s" % nm for nm in names))
for i in range(22):
    print("%5s " % names[i] + " ".join("%5s" % (str(A[i][j]) if A[i][j] != 0 else ".") for j in range(22)))
