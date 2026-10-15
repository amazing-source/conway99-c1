"""Explicit absorbing kernel vectors (LAB 15/10/2026, task T3: absorption lemma behind the 13-wall).

Side m (base X_m = labels meeting {2,3}; l-odd e_z = 1_{0z} - 1_{1z}; l-even u_y = 1_{0y} + 1_{1y}, y = 4..13): for each
y, the exact rational solutions of T (u_y + sum_x a_x 1_x + sum_z b_z e_z) = 0 (x in X_m).  We print one solution per y
(reduced modulo the kernel vectors that live in span(X_m, e_z)), with its coefficients grouped by label type, so that
its combinatorial shape can be read.  usage: python absorbers.py <json> [side l|m] [letters y, e.g. 4,5]"""
import json
import sys
from fractions import Fraction as Fr

sys.path.insert(0, '.')
from stars_rank import kval


def rref(A):
    A = [r[:] for r in A]
    m, n = len(A), len(A[0])
    piv = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [x * inv for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    return A[:r], piv


def nullspace(A):
    R, piv = rref(A)
    n = len(A[0])
    out = []
    for f in [c for c in range(n) if c not in piv]:
        v = [Fr(0)] * n
        v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        out.append(v)
    return out


d = json.load(open(sys.argv[1]))
side = sys.argv[2] if len(sys.argv) > 2 else "m"
ys = [int(t) for t in sys.argv[3].split(",")] if len(sys.argv) > 3 else list(range(4, 14))
S = [frozenset(l) for l in d["labels"]]
n = len(S)
idx = {s: i for i, s in enumerate(S)}
E = {tuple(sorted(x)) for x in d["edges"]}
T = [[(3 if a == b else 0) - (1 if tuple(sorted((a, b))) in E else 0) - Fr(kval(S[a], S[b])).limit_denominator(8)
      for b in range(n)] for a in range(n)]
if side == "m":
    base_letters, odd_pair = {2, 3}, (0, 1)
else:
    base_letters, odd_pair = {0, 1}, (2, 3)
X = [i for i in range(n) if S[i] & base_letters]
a0, a1 = odd_pair
odd = []
for z in range(4, 14):
    v = [Fr(0)] * n
    v[idx[frozenset((a0, z))]] = Fr(1)
    v[idx[frozenset((a1, z))]] = Fr(-1)
    odd.append((z, v))
# basis of span(X, odd) as columns; kernel part inside it
cols = []
names = []
for i in X:
    v = [Fr(0)] * n
    v[i] = Fr(1)
    cols.append(v)
    names.append("x" + "".join(map(str, sorted(S[i]))))
for z, v in odd:
    cols.append(v)
    names.append("e%d" % z)
TB = [[sum(T[r][k] * cols[c][k] for k in range(n) if cols[c][k] != 0) for c in range(len(cols))] for r in range(n)]
inner = nullspace(TB)
print("%s side %s: dim(ker T within span(X, odd)) = %d" % (sys.argv[1], side, len(inner)))
for y in ys:
    u = [Fr(0)] * n
    u[idx[frozenset((a0, y))]] = Fr(1)
    u[idx[frozenset((a1, y))]] = Fr(1)
    Tu = [sum(T[r][k] * u[k] for k in range(n) if u[k] != 0) for r in range(n)]
    A = [row + [Tu[r]] for r, row in enumerate(TB)]
    sols = [v for v in nullspace(A) if v[-1] != 0]
    if not sols:
        print("  y = %d: NOT absorbed" % y)
        continue
    v = sols[0]
    lam = v[-1]
    coef = [c / lam for c in v[:-1]]
    # reduce modulo the inner kernel: zero the coefficients on the free columns of the inner kernel (canonical form)
    terms = [(names[k], coef[k]) for k in range(len(cols)) if coef[k] != 0]
    terms.sort(key=lambda t: t[0])
    print("  y = %d: u_y + sum = 0 with %d terms: %s" % (y, len(terms), ", ".join("%s:%s" % (a, b) for a, b in terms)))
