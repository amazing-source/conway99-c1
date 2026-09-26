# Spanning-tree numbers (exact) and Laplacian nullity mod 7 for the 15 girth>=5 types of 6-label components.
import itertools, sys
from fractions import Fraction
sys.path.insert(0, '.')
labels = list(range(6)); mate = {i: i ^ 1 for i in labels}
def matchings(ls):
    if not ls: yield {}; return
    a = ls[0]
    for b in ls[1:]:
        if b == mate[a]: continue
        rest = [c for c in ls if c not in (a, b)]
        for m in matchings(rest):
            d = dict(m); d[a] = b; d[b] = a; yield d
M = list(matchings(labels))
good = []
for tu in M:
    for tb in M:
        for perm in itertools.permutations(labels):
            s = dict(zip(labels, perm))
            if all(s[v] not in (v, mate[v], tu[v], tb[v]) for v in labels) and all(tb[s[w]] != s[tu[w]] for w in labels):
                good.append((tu, tb, s))
def lap(tu, tb, s):
    idx = {}
    for L in 'xub':
        for v in labels: idx[(L, v)] = len(idx)
    n = len(idx); A = [[0] * n for _ in range(n)]
    def e(a, b): A[idx[a]][idx[b]] = A[idx[b]][idx[a]] = 1
    for v in labels:
        e(('x', v), ('x', mate[v])); e(('u', v), ('u', tu[v])); e(('b', v), ('b', tb[v]))
        e(('x', v), ('u', v)); e(('x', v), ('b', v)); e(('u', v), ('b', s[v]))
    return [[(3 if i == j else 0) - A[i][j] for j in range(n)] for i in range(n)]
def det_frac(Mx):
    Mx = [[Fraction(v) for v in r] for r in Mx]; n = len(Mx); d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if Mx[r][c] != 0), None)
        if p is None: return Fraction(0)
        if p != c: Mx[c], Mx[p] = Mx[p], Mx[c]; d = -d
        d *= Mx[c][c]
        for r in range(c + 1, n):
            f = Mx[r][c] / Mx[c][c]
            if f: Mx[r] = [a - f * b for a, b in zip(Mx[r], Mx[c])]
    return d
def rank_mod(Mx, p=7):
    Mx = [[v % p for v in r] for r in Mx]; n, m = len(Mx), len(Mx[0]); r = 0
    for c in range(m):
        piv = next((i for i in range(r, n) if Mx[i][c]), None)
        if piv is None: continue
        Mx[r], Mx[piv] = Mx[piv], Mx[r]; inv = pow(Mx[r][c], p - 2, p); Mx[r] = [(v * inv) % p for v in Mx[r]]
        for i in range(n):
            if i != r and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [(a - f * b) % p for a, b in zip(Mx[i], Mx[r])]
        r += 1
    return r
from collections import Counter
cnt = Counter()
for tu, tb, s in good:
    L = lap(tu, tb, s)
    tau = det_frac([row[1:] for row in L[1:]])
    null7 = 18 - rank_mod(L)
    cnt[(int(tau), int(tau) % 7, null7)] += 1
for (tau, r7, n7), c in sorted(cnt.items()):
    print(f'tau = {tau:>8}  tau mod 7 = {r7}  nullity_7(Laplacian) = {n7}   ({c} labeled components)')
