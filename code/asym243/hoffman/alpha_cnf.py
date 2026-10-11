"""CNF: srg(v,k,lam,mu) whose vertices 0..c-1 form a Hoffman coclique (c = v(-s)/(k-s)); every other vertex then has
exactly t = k c/(v-c) neighbours in it (added as redundant cardinality constraints).
Exact encoding: x_ij edge variables; for each pair {i,j} and third vertex k, y = x_ik & x_jk (Tseitin); the number of
y's is lam if x_ij else mu (sequential counters capped at max(lam,mu)+1); degrees = k.
Symmetry breaking (all WLOG, see note 171): vertex 0 of the coclique has neighbours c..c+k-1, in that order, and if
lam = 1 the neighbourhood matching is (c,c+1),(c+2,c+3),...  Optional: units file "i j b" lines.
  python3 alpha_cnf.py v k lam mu c OUT [units]"""
import sys, itertools
v, k, lam, mu, c = map(int, sys.argv[1:6]); out = sys.argv[6]; units = sys.argv[7] if len(sys.argv) > 7 else None
nv = 0; cls = []
def new():
    global nv; nv += 1; return nv
X = {}
for i in range(v):
    for j in range(i + 1, v): X[(i, j)] = new()
x = lambda i, j: X[(min(i, j), max(i, j))]
def counter_eq(lits, target, cap):
    """sequential counter; returns ge[1..cap] with ge[j] <-> sum >= j"""
    prev = [None] * (cap + 1)
    for l in lits:
        cur = [None] * (cap + 1)
        for j in range(1, cap + 1):
            vv = new(); cur[j] = vv
            if prev[j] is not None: cls.append([-prev[j], vv])
            if j == 1: cls.append([-l, vv])
            elif prev[j - 1] is not None: cls.append([-prev[j - 1], -l, vv])
            a = [] if prev[j] is None else [prev[j]]
            if j == 1: cls.append([-vv] + a + [l])
            elif prev[j - 1] is None: cls.append([-vv] + a)
            else: cls.append([-vv] + a + [l]); cls.append([-vv] + a + [prev[j - 1]])
        prev = cur
    return prev
def exactly(lits, t):
    ge = counter_eq(lits, t, t + 1)
    if t >= 1: cls.append([ge[t]])
    cls.append([-ge[t + 1]])
# coclique
for i in range(c):
    for j in range(i + 1, c): cls.append([-x(i, j)])
# degrees
for i in range(v): exactly([x(i, j) for j in range(v) if j != i], k)
t = k * c // (v - c)
for w in range(c, v): exactly([x(w, s) for s in range(c)], t)
# pair conditions
cap = max(lam, mu) + 1
for i in range(v):
    for j in range(i + 1, v):
        ys = []
        for kk in range(v):
            if kk in (i, j): continue
            y = new(); a, b = x(i, kk), x(j, kk)
            cls.append([-y, a]); cls.append([-y, b]); cls.append([y, -a, -b]); ys.append(y)
        ge = counter_eq(ys, None, cap); e = x(i, j)
        # if edge: sum == lam ; else sum == mu
        if lam >= 1: cls.append([-e, ge[lam]])
        cls.append([-e, -ge[lam + 1]])
        if mu >= 1: cls.append([e, ge[mu]])
        cls.append([e, -ge[mu + 1]])
# symmetry breaking at vertex 0
for j in range(c, v): cls.append([x(0, j)] if j < c + k else [-x(0, j)])
if lam == 1:
    for a in range(c, c + k):
        for b in range(a + 1, c + k):
            mate = (a - c) // 2 == (b - c) // 2
            cls.append([x(a, b)] if mate else [-x(a, b)])
if units:
    for l in open(units):
        if l.strip():
            i, j, bb = map(int, l.split()); cls.append([x(i, j)] if bb else [-x(i, j)])
with open(out, "w") as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for cl in cls: f.write(" ".join(map(str, cl)) + " 0\n")
import pickle; pickle.dump(X, open(out + ".map", "wb"))
print("vars", nv, "clauses", len(cls))
