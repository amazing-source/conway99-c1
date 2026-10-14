"""Kernel of T_S4 split into local (l-side, m-side) and mixed relations; letter values of each relation as a global
3-eigenvector (value on letter i = (t_i - w)/8, on v = -w/4; P14).  usage: python mixed_view.py <json>"""
import sys, json, itertools
from fractions import Fraction as Fr
from math import gcd
import ext4
d = json.load(open(sys.argv[1]))
S = [frozenset(l) for l in d["labels"]]; n = len(S)
Gl = [[0]*n for _ in range(n)]
for i, j in d["edges"]: Gl[i][j] = Gl[j][i] = 1
T = [[(3 if i == j else 0) - Gl[i][j] - ext4.kval(S[i], S[j]) for j in range(n)] for i in range(n)]
r, ker = ext4.rref_kernel(T)
print("rank", r, "nullity", len(ker))
Xl = [i for i in range(n) if S[i] & {0, 1}]
Xm = [i for i in range(n) if S[i] & {2, 3}]
def sub_kernel(idx):
    M = [[T[a][b] for b in idx] for a in idx]
    _, k = ext4.rref_kernel(M)
    out = []
    for v in k:
        w = [Fr(0)]*n
        for t, a in enumerate(idx): w[a] = v[t]
        out.append(w)
    return out
kl, km = sub_kernel(Xl), sub_kernel(Xm)
loc = kl + km
rl, _ = ext4.rref_kernel([list(x) for x in kl]) if kl else (0, None)
rloc, _ = ext4.rref_kernel([list(x) for x in loc])
print("dim ker_l", len(kl), "dim ker_m", len(km), "dim(ker_l + ker_m)", rloc, "-> mixed", len(ker) - rloc)
# mixed relations: complete a basis of ker modulo loc, choose primitive integer representatives with small support
def rank(rows):
    return ext4.rref_kernel([list(x) for x in rows])[0] if rows else 0
mixed = []
basis = list(loc)
cur = rank(basis)
for v in ker:
    if rank(basis + [v]) > cur:
        basis.append(v); cur += 1; mixed.append(v)
def prim(v):
    den = 1
    for x in v: den = den*x.denominator//gcd(den, x.denominator)
    w = [int(x*den) for x in v]; g = 0
    for x in w: g = gcd(g, abs(x))
    return [x//g for x in w]
for k, v in enumerate(mixed):
    p = prim(v)
    w = sum(p)
    dsum = {i: sum(p[j] for j in range(n) if i in S[j]) for i in range(14)}
    t = {i: 3*dsum[i] + dsum[i ^ 1] for i in range(14)}
    print("mixed relation %d: support %d, weight w = %d" % (k, sum(1 for x in p if x), w))
    print("   entries:", {"%d%d" % tuple(sorted(S[j])): p[j] for j in range(n) if p[j]})
    print("   letter values 8*g_i = t_i - w:", {i: t[i] - w for i in range(14)}, " value on v = -w/4 =", Fr(-w, 4))
