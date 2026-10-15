"""Shape of the ten forced relations (LAB 15/10/2026, task T3, exact).

For a structure with ker T = 12 h-even + 2 h-odd dimensions, write the even kernel in the orbit basis of E_+:
u_y = 1_{0y} + 1_{1y} (y = 4..13, l-side), g_z = 1_{2z} + 1_{3z} (z = 4..13, m-side), c1 = 1_{02} + 1_{13},
c2 = 1_{03} + 1_{12}.  Modulo the two even star sums (1_{L0} + 1_{L1} = sum u + c1 + c2, 1_{L2} + 1_{L3} = sum g + c1 + c2)
the even kernel is 10-dimensional; we print it in reduced row echelon form with the u-columns first, i.e. as the graph
of a map u_y -> sum_z Phi_yz g_z + alpha_y c1 + beta_y c2 when the u-part has rank 10.  Exact rationals.
usage: python kernel_shape.py <json with labels, edges>"""
import json
import sys
from fractions import Fraction as Fr

sys.path.insert(0, '.')
from stars_rank import kval
from cls_decomp import nullspace_int

d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]
n = len(S)
idx = {s: i for i, s in enumerate(S)}
E = {tuple(sorted(x)) for x in d["edges"]}
M8 = [[(24 if a == b else 0) - 8 * (1 if tuple(sorted((a, b))) in E else 0) - int(round(8 * kval(S[a], S[b])))
       for b in range(n)] for a in range(n)]
N = nullspace_int(M8)
print("nullity", len(N))
L = lambda a, b: idx[frozenset((a, b))]
basis, names = [], []
for y in range(4, 14):
    v = [0] * n; v[L(0, y)] = v[L(1, y)] = 1; basis.append(v); names.append("u%d" % y)
for z in range(4, 14):
    v = [0] * n; v[L(2, z)] = v[L(3, z)] = 1; basis.append(v); names.append("g%d" % z)
v = [0] * n; v[L(0, 2)] = v[L(1, 3)] = 1; basis.append(v); names.append("c1")
v = [0] * n; v[L(0, 3)] = v[L(1, 2)] = 1; basis.append(v); names.append("c2")
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
even = [vec for vec in N if all(vec[i] == vec[hp[i]] for i in range(n))]
# the even part of ker T: project every kernel vector on E_+ and keep the ones that are kernel vectors (they all are
# when ker T is h-invariant); coordinates in the orbit basis: coefficient of u_y = value at {0,y}, etc.
proj = []
for vec in N:
    pv = [Fr(vec[i] + vec[hp[i]], 2) for i in range(n)]
    proj.append(pv)
# check that projections are kernel vectors
ok = all(sum(M8[i][j] * pv[j] for j in range(n)) == 0 for pv in proj for i in range(n))
print("ker T h-invariant (even projections are kernel vectors):", ok)
coords = []
for pv in proj:
    c = [pv[L(0, y)] for y in range(4, 14)] + [pv[L(2, z)] for z in range(4, 14)] + [pv[L(0, 2)], pv[L(0, 3)]]
    # consistency: pv equals sum c_k basis_k
    rec = [sum(c[k] * basis[k][i] for k in range(22)) for i in range(n)]
    assert rec == pv
    coords.append(c)
# add the two star sums and reduce: RREF over the 22 coordinates
R = [row[:] for row in coords]
m = len(R)
piv = []
r = 0
for col in range(22):
    p = next((i for i in range(r, m) if R[i][col] != 0), None)
    if p is None:
        continue
    R[r], R[p] = R[p], R[r]
    inv = 1 / R[r][col]
    R[r] = [x * inv for x in R[r]]
    for i in range(m):
        if i != r and R[i][col] != 0:
            f = R[i][col]
            R[i] = [a - f * b for a, b in zip(R[i], R[r])]
    piv.append(col)
    r += 1
R = R[:r]
print("even kernel dimension:", r, "; pivot columns:", [names[c] for c in piv])
for row, c in zip(R, piv):
    terms = ["%s%s" % ("" if x == 1 else ("-" if x == -1 else str(x) + "*"), names[k]) for k, x in enumerate(row) if x != 0]
    print("  ", " + ".join(terms).replace("+ -", "- "))
