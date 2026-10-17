"""Case I of c = 1 (sigma-sigma 2-cut with four distinct letters): far design + co-Heawood vector, line type fixed
(exploration, LAB 17/10/2026).
Root l = {v,0,1}; S = letters of the root lines 1..s; cut edges {0,a}-{1,d} (d = sigma a), {0,b}-{1,c} (c = sigma b).
h = T 1_{Q_0S}: +1 on {0,a}, {1,c} and on 5 far labels, -1 on {0,b}, {1,d} and on 5 far labels (Codex's lemma, norm 14),
with h(w) = s - |name(w) n S| - |L_0-pair(w) n S| - |L_1-pair(w) n S| on far labels w.  Necessary constraints:
  (GG) far design exact (bijections to non-mu pairs, letter/label and L_0/L_1 counts, caps G-D);
  values h in {-1,0,1} on all far labels, exactly 5 + 5 nonzero, same-sign names pairwise disjoint (perfect matchings);
  eigen-equation Gamma h = -4 h on the 24 labels of L_0 u L_1 and on the 60 far labels (far-far edges as variables,
  far degree 8), same-sign support labels non-adjacent.
UNSAT for a line type = no Conway graph has this line with this cut.  Line types: the two CP-SAT witnesses of
sigcut_local.py (s = 2, 3).
usage: python gg_case1.py <s> <seconds> [workers]"""
import itertools
import sys
import time

from ortools.sat.python import cp_model

s, secs = int(sys.argv[1]), float(sys.argv[2])
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 2
MATE = lambda x: x ^ 1
X = list(range(2, 14))
WIT = {2: dict(a=4, d=7, b=8, c=3, sigma={2: 4, 3: 5, 4: 7, 5: 2, 6: 10, 7: 9, 8: 3, 9: 13, 10: 11, 11: 12, 12: 6, 13: 8},
               mu0=[(2, 3), (4, 5), (6, 7), (8, 13), (9, 10), (11, 12)], mu1=[(2, 3), (4, 5), (6, 10), (7, 9), (8, 11), (12, 13)]),
       3: dict(a=2, d=9, b=8, c=3, sigma={2: 9, 3: 4, 4: 6, 5: 2, 6: 5, 7: 7, 8: 3, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12},
               mu0=[(2, 3), (4, 5), (6, 7), (8, 10), (9, 13), (11, 12)], mu1=[(2, 3), (4, 7), (5, 6), (8, 10), (9, 13), (11, 12)])}
w = WIT[s]
a, d, b, c, sig = w["a"], w["d"], w["b"], w["c"], w["sigma"]
mu = {0: {}, 1: {}}
for r in (0, 1):
    for x, y in w["mu%d" % r]:
        mu[r][x], mu[r][y] = y, x
Sl = set(range(2, 2 + 2 * s))
assert sig[a] == d and sig[b] == c and a in Sl and c in Sl and b not in Sl and d not in Sl
# G_l vertices: ("L", x), (0, x), (1, x)
G = [("L", x) for x in X] + [(0, x) for x in X] + [(1, x) for x in X]
def gadj(u, v):
    if u == v:
        return 0
    if u[0] == "L" and v[0] == "L":
        return int(MATE(u[1]) == v[1])
    if u[0] == "L" or v[0] == "L":
        return int(u[1] == v[1])
    if u[0] == v[0]:
        return int(mu[u[0]][u[1]] == v[1])
    if u[0] == 0:
        return int(sig[u[1]] == v[1])
    return int(sig[v[1]] == u[1])
A2 = {(u, v): sum(gadj(u, t) * gadj(t, v) for t in G) for u in G for v in G}
group = lambda u: u[0]
D = [frozenset((x, y)) for x, y in itertools.combinations(X, 2) if y != MATE(x)]
m = cp_model.CpModel()
U = {}
for r in (0, 1):
    E = [(p, q) for p, q in itertools.combinations(X, 2) if mu[r][p] != q]
    y = {(k, e): m.NewBoolVar("") for k in range(60) for e in range(60)}
    for k in range(60):
        m.AddExactlyOne([y[(k, e)] for e in range(60)])
    for e in range(60):
        m.AddExactlyOne([y[(k, e)] for k in range(60)])
    for k in range(60):
        for x in X:
            bv = m.NewBoolVar("")
            m.Add(bv == sum(y[(k, e)] for e, (p, q) in enumerate(E) if x in (p, q)))
            U[(r, x, k)] = bv
def att(u, k):
    if u[0] == "L":
        return 1 if u[1] in D[k] else 0
    return U[(u[0], u[1], k)]
# (GG) letter / label and L_0 / L_1 counts
GI = {u: i for i, u in enumerate(G)}
for u in G:
    for v in G:
        if GI[u] >= GI[v] or (u[0] == "L" and v[0] == "L"):
            continue
        tgt = (1 if gadj(u, v) else 2) - (1 if group(u) == group(v) else 0) - A2[(u, v)]
        if u[0] != "L" and v[0] != "L" and u[0] == v[0]:
            continue                       # same star: guaranteed by the bijection
        terms = []
        for k in range(60):
            p, q = att(u, k), att(v, k)
            if isinstance(p, int) and isinstance(q, int):
                tgt -= p * q
            elif isinstance(p, int):
                if p:
                    terms.append(q)
            elif isinstance(q, int):
                if q:
                    terms.append(p)
            else:
                z = m.NewBoolVar("")
                m.AddBoolOr([p.Not(), q.Not(), z]); m.AddImplication(z, p); m.AddImplication(z, q)
                terms.append(z)
        m.Add(sum(terms) == tgt)
# caps G-D: common neighbours inside G_l
for u in G:
    nb = [t for t in G if gadj(u, t)]
    for k in range(60):
        e = att(u, k)
        sm = sum(att(t, k) for t in nb)
        m.Add(sm <= 2 - e)
# h on far labels
pos = [m.NewBoolVar("p%d" % k) for k in range(60)]
neg = [m.NewBoolVar("n%d" % k) for k in range(60)]
for k, z in enumerate(D):
    kv = len(z & Sl)
    hk = s - kv - sum(U[(r, x, k)] for r in (0, 1) for x in Sl)
    m.Add(hk == pos[k] - neg[k])
    m.AddBoolOr([pos[k].Not(), neg[k].Not()])
m.Add(sum(pos) == 5)
m.Add(sum(neg) == 5)
for x in X:
    m.Add(sum(pos[k] for k, z in enumerate(D) if x in z) == (0 if x in (a, c) else 1))
    m.Add(sum(neg[k] for k, z in enumerate(D) if x in z) == (0 if x in (b, d) else 1))
hL = {u: 0 for u in G}
hL[(0, a)] = hL[(1, c)] = 1
hL[(0, b)] = hL[(1, d)] = -1
# eigen-equation on L_0 u L_1, and no same-sign neighbour of the four L01 support labels
for u in G:
    if u[0] == "L":
        continue
    pp, nn = [], []
    for k in range(60):
        e = U[(u[0], u[1], k)]
        zp, zn = m.NewBoolVar(""), m.NewBoolVar("")
        m.AddBoolOr([e.Not(), pos[k].Not(), zp]); m.AddImplication(zp, e); m.AddImplication(zp, pos[k])
        m.AddBoolOr([e.Not(), neg[k].Not(), zn]); m.AddImplication(zn, e); m.AddImplication(zn, neg[k])
        pp.append(zp); nn.append(zn)
    loc = sum(hL[t] for t in G if gadj(u, t) and t[0] != "L")
    m.Add(sum(pp) - sum(nn) + loc == -4 * hL[u])
    if hL[u] == 1:
        m.Add(sum(pp) == 0)
    if hL[u] == -1:
        m.Add(sum(nn) == 0)
# far-far edges (degree 8), eigen-equation on far labels, same-sign far support non-adjacent
F = {}
for i, j in itertools.combinations(range(60), 2):
    F[(i, j)] = F[(j, i)] = m.NewBoolVar("")
for i in range(60):
    m.Add(sum(F[(i, j)] for j in range(60) if j != i) == 8)
for i in range(60):
    pp, nn = [], []
    for j in range(60):
        if j == i:
            continue
        zp, zn = m.NewBoolVar(""), m.NewBoolVar("")
        m.AddBoolOr([F[(i, j)].Not(), pos[j].Not(), zp]); m.AddImplication(zp, F[(i, j)]); m.AddImplication(zp, pos[j])
        m.AddBoolOr([F[(i, j)].Not(), neg[j].Not(), zn]); m.AddImplication(zn, F[(i, j)]); m.AddImplication(zn, neg[j])
        pp.append(zp); nn.append(zn)
    loc = sum(hL[u] * U[(u[0], u[1], i)] for u in G if u[0] != "L" and hL[u])
    m.Add(sum(pp) - sum(nn) + loc == -4 * (pos[i] - neg[i]))
    # same-sign: no positive neighbour of a positive (far or L01), idem negative
    m.Add(sum(pp) + sum(U[(u[0], u[1], i)] for u in G if u[0] != "L" and hL[u] == 1) == 0).OnlyEnforceIf(pos[i])
    m.Add(sum(nn) + sum(U[(u[0], u[1], i)] for u in G if u[0] != "L" and hL[u] == -1) == 0).OnlyEnforceIf(neg[i])
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = workers
sv.parameters.max_time_in_seconds = secs
t0 = time.time()
st = sv.Solve(m)
print("case I, s = %d, witness line type: %s in %.1f s (workers %d)" % (s, sv.StatusName(st), time.time() - t0, workers),
      flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print("positives:", [sorted(D[k]) for k in range(60) if sv.Value(pos[k])])
    print("negatives:", [sorted(D[k]) for k in range(60) if sv.Value(neg[k])])
