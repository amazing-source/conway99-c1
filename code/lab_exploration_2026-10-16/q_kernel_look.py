"""Look at ker Q for one block (exploration, LAB 16/10/2026).
Y = {2s, 3s : s = 4..13} is a 2 x 10 array (rows r = 2, 3; columns s).  Prints an exact (rational) basis of ker Q in
reduced row echelon form, the components of G[N(l)] with the lines they contain, and simple invariants of ker Q:
dimension of the subspaces where the profile is constant along columns (x_2s = x_3s), antisymmetric (x_2s = -x_3s),
and supported on the columns of each line.
usage: python q_kernel_look.py <block json>"""
import itertools
import json
import sys

import sympy as sp

MATE = lambda i: i ^ 1
d = json.load(open(sys.argv[1]))
L = [frozenset(x) for x in d["labels"]]
E = set(frozenset((L[i], L[j])) for i, j in d["edges"])
S = [l for l in L if l & {0, 1, 2, 3}]
Nset = [("L", s) for s in range(2, 14)] + [l for l in S if l & {0, 1}]
Yset = [frozenset((r, s)) for r in (2, 3) for s in range(4, 14)]
W = Nset + Yset
pos = {x: i for i, x in enumerate(W)}
n = len(W)
A = sp.zeros(n, n)


def adj(a, b):
    if isinstance(a, tuple) and isinstance(b, tuple):
        return a[1] == MATE(b[1])
    if isinstance(a, tuple):
        return a[1] in b
    if isinstance(b, tuple):
        return b[1] in a
    return frozenset((a, b)) in E


for i, j in itertools.combinations(range(n), 2):
    if adj(W[i], W[j]):
        A[i, j] = A[j, i] = 1
M = A - 3 * sp.eye(n)
ker = M.nullspace()
print("mult_3(A_W) =", len(ker))
# split: component part (vanishing on Y) and profiles
Ymat = sp.Matrix([[v[pos[y]] for y in Yset] for v in ker])
prof = Ymat.rref()[0]
rk = Ymat.rank()
print("profile space dimension (= corank Q) =", rk)
names = ["%d%d" % tuple(sorted(y)) for y in Yset]
print("profiles (rref rows, columns 24..213 then 34..313):")
for i in range(rk):
    row = prof.row(i)
    print("   " + " ".join("%5s" % (str(row[j]) if row[j] != 0 else ".") for j in range(20)))
# components of G[N(l)]
NA = A[:36, :36]
seen, comps = set(), []
for i in range(36):
    if i in seen:
        continue
    st, comp = [i], []
    seen.add(i)
    while st:
        u = st.pop()
        comp.append(u)
        for w in range(36):
            if NA[u, w] and w not in seen:
                seen.add(w)
                st.append(w)
    comps.append(comp)
for c in comps:
    letters = sorted(W[u][1] for u in c if isinstance(W[u], tuple))
    print("component size %d, letters %s" % (len(c), letters))
# invariants
sym = sp.Matrix([[1 if (j % 10 == k) else 0 for j in range(20)] for k in range(10)])   # columns
P = prof[:rk, :]
D = sp.Matrix([[P[i, k] - P[i, k + 10] for k in range(10)] for i in range(rk)])
Sm = sp.Matrix([[P[i, k] + P[i, k + 10] for k in range(10)] for i in range(rk)])
print("rank of the antisymmetric parts x_2s - x_3s:", D.rank(), "; rank of x_2s + x_3s:", Sm.rank())
