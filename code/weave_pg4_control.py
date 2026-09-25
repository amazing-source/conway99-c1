# Positive control of the "weave <-> polarity" mechanism at order q = 4.
# PG(2,4) with the polarity x -> x^perp for B(x,y) = x0y0 + x1y1 + x2y2 (char 2):
# absolute points form the line L: x0+x1+x2 = 0, whose pole is P = (1,1,1).
# Remove L and P; group the q^2-1 = 15 points by the lines through P (groups of q-1 = 3);
# graph = (clique on each group) + (x ~ y iff B(x,y) = 0).  Expected: srg(15,6,1,3) (the analogue
# of the 99 computation with K3 blocks instead of 3x3 grids: e = 1 everywhere, g = 2 on cross pairs).
import itertools
# GF(4) = {0,1,w,w^2} as 0,1,2,3 ; addition = xor, multiplication via log table
LOG = {1: 0, 2: 1, 3: 2}; EXP = [1, 2, 3]
def mul(a, b):
    if a == 0 or b == 0: return 0
    return EXP[(LOG[a] + LOG[b]) % 3]
def inv(a): return EXP[(-LOG[a]) % 3]
def norm(v):
    for c in v:
        if c: return tuple(mul(inv(c), x) for x in v)
pts = sorted({norm(v) for v in itertools.product(range(4), repeat=3) if any(v)})
assert len(pts) == 21
def B(x, y):
    s = 0
    for a, b in zip(x, y): s ^= mul(a, b)
    return s
P = norm((1, 1, 1))
absolute = [x for x in pts if B(x, x) == 0]
assert all((x[0] ^ x[1] ^ x[2]) == 0 for x in absolute) and len(absolute) == 5 and B(P, P) != 0
V = [x for x in pts if x not in absolute and x != P]
assert len(V) == 15
def collinear(a, b, c):  # det over GF(4)
    d = 0
    for (i, j, k), sgn in [((0,1,2),1), ((1,2,0),1), ((2,0,1),1), ((0,2,1),1), ((1,0,2),1), ((2,1,0),1)]:
        d ^= mul(mul(a[i], b[j]), c[k])
    return d == 0
group = {}
for x in V:
    group[x] = next(i for i, g in enumerate(sorted({frozenset(y for y in V if y == x or collinear(P, x, y)) for x in V}, key=sorted)) if x in g)
n = len(V); idx = {x: i for i, x in enumerate(V)}
A = [[0]*n for _ in range(n)]
for x, y in itertools.combinations(V, 2):
    if group[x] == group[y] or B(x, y) == 0:
        A[idx[x]][idx[y]] = A[idx[y]][idx[x]] = 1
deg = {sum(r) for r in A}
lam, mu = set(), set()
for i, j in itertools.combinations(range(n), 2):
    c = sum(A[i][k] and A[j][k] for k in range(n))
    (lam if A[i][j] else mu).add(c)
print("groups:", sorted({sum(1 for x in V if group[x] == g) for g in set(group.values())}), "count", len(set(group.values())))
print("degrees", deg, "lambda", lam, "mu", mu)
