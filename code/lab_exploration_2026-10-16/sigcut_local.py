"""Is a sigma-sigma 2-cut with four distinct letters locally possible?  (exploration, LAB 17/10/2026)
Line l = {v,0,1}; G_l on letters 2..13 (mates x, x^1), L_0 = {0,x}, L_1 = {1,x}; unknowns mu_0, mu_1 (perfect matchings of
the 12 letters, giving the lines through 0 and 1) and sigma (permutation: {0,x} ~ {1,sigma x}).  Local caps (exact srg
counts can only be smaller inside G_l): for w != w' in G_l, common neighbours inside G_l <= [w ~ w' ? 1 : 2] - [same group].
2-cut: S = the letters of root lines 1..s (s = 2 or 3); mu_0, mu_1 preserve S; sigma maps S into S except a -> d (d not in
S), and non-S into non-S except b -> c (c in S); DISTINCT: a != c and b != d (i.e. sigma(b) != a, sigma(a) != b).
usage: python sigcut_local.py s seconds"""
import itertools
import sys
from ortools.sat.python import cp_model

s, secs = int(sys.argv[1]), float(sys.argv[2])
X = list(range(2, 14))
MATE = lambda x: x ^ 1
Sl = set(range(2, 2 + 2 * s))
m = cp_model.CpModel()
mu = {}
for r in (0, 1):
    for x, y in itertools.combinations(X, 2):
        mu[(r, x, y)] = mu[(r, y, x)] = m.NewBoolVar("")
    for x in X:
        m.AddExactlyOne([mu[(r, x, y)] for y in X if y != x])
sg = {(x, y): m.NewBoolVar("") for x in X for y in X}
for x in X:
    m.AddExactlyOne([sg[(x, y)] for y in X])
    m.AddExactlyOne([sg[(y, x)] for y in X])
# vertices of G_l
V = [("L", x) for x in X] + [(0, x) for x in X] + [(1, x) for x in X]
def adj(u, w):
    if u == w:
        return 0
    if u[0] == "L" and w[0] == "L":
        return 1 if MATE(u[1]) == w[1] else 0
    if u[0] == "L":
        return 1 if w[1] == u[1] else 0
    if w[0] == "L":
        return 1 if u[1] == w[1] else 0
    if u[0] == w[0]:
        return mu[(u[0], u[1], w[1])]
    if u[0] == 0:
        return sg[(u[1], w[1])]
    return sg[(w[1], u[1])]
def group(u):
    return u[0]
for u, w in itertools.combinations(V, 2):
    terms, const = [], 0
    for t in V:
        if t in (u, w):
            continue
        a, b = adj(u, t), adj(w, t)
        if isinstance(a, int) and isinstance(b, int):
            const += a * b
        elif isinstance(a, int):
            if a:
                terms.append(b)
        elif isinstance(b, int):
            if b:
                terms.append(a)
        else:
            q = m.NewBoolVar("")
            m.AddBoolOr([a.Not(), b.Not(), q]); m.AddImplication(q, a); m.AddImplication(q, b)
            terms.append(q)
    e = adj(u, w)
    same = 1 if group(u) == group(w) else 0
    cap_nonadj = 2 - same
    if isinstance(e, int):
        m.Add(sum(terms) + const <= (1 - same if e else cap_nonadj))
    else:
        # adjacent: <= 1 - same ; non-adjacent: <= 2 - same
        m.Add(sum(terms) + const <= cap_nonadj - e)
# cut structure
for r in (0, 1):
    for x in Sl:
        for y in X:
            if y not in Sl:
                m.Add(mu[(r, x, y)] == 0)
a, d, b, c = (m.NewIntVar(2, 13, n) for n in "adbc")
cross_out = [sg[(x, y)] for x in Sl for y in X if y not in Sl]
cross_in = [sg[(x, y)] for x in X if x not in Sl for y in Sl]
m.Add(sum(cross_out) == 1)
m.Add(sum(cross_in) == 1)
for x in Sl:
    for y in X:
        if y not in Sl:
            m.Add(a == x).OnlyEnforceIf(sg[(x, y)]); m.Add(d == y).OnlyEnforceIf(sg[(x, y)])
for x in X:
    if x not in Sl:
        for y in Sl:
            m.Add(b == x).OnlyEnforceIf(sg[(x, y)]); m.Add(c == y).OnlyEnforceIf(sg[(x, y)])
if "--shared" not in sys.argv:
    m.Add(a != c); m.Add(b != d)
sv = cp_model.CpSolver(); sv.parameters.num_search_workers = 2; sv.parameters.max_time_in_seconds = secs
st = sv.Solve(m)
print("s=%d %s: %s" % (s, "shared allowed" if "--shared" in sys.argv else "DISTINCT", sv.StatusName(st)))
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("a,d,b,c =", sv.Value(a), sv.Value(d), sv.Value(b), sv.Value(c))
    print("sigma:", {x: y for x in X for y in X if sv.Value(sg[(x, y)])})
    for r in (0, 1):
        print("mu%d:" % r, sorted({tuple(sorted((x, y))) for x, y in itertools.combinations(X, 2) if sv.Value(mu[(r, x, y)])}))
