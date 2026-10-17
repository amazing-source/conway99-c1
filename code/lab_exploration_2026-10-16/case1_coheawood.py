"""Case I of c = 1 (and of any root): sigma-sigma 2-cut with four distinct letters, as a CO-HEAWOOD model
(exploration, LAB 17/10/2026).  Line type FREE (only the cut structure fixed by symmetry).
Root l = {v,0,1}; S = letters of root lines {2,3},...,{2s,2s+1}; cut edges {0,a}-{1,d} (d = sigma a, a in S, d not) and
{0,b}-{1,c} (c = sigma b, c in S, b not), a != c, b != d.  h = T 1_{Q_0S} has norm 14 (Codex), so (Codex's lemma, proved
in EXPLORATION.md): h in {0,+1,-1}, P = {+} and N = {-} have 7 elements, cocliques, P-N bipartite 4-regular, two
same-sign vertices have EXACTLY their 2 common neighbours in the opposite sign set; hence every vertex off the support
has either no support neighbour or exactly one + and one - ("linked").
Inside N[l]: h = +1 on {0,a}, {1,c}, -1 on {0,b}, {1,d}, 0 on letters and on the other labels of L_0 u L_1.
Far labels z = {x,y} (x,y letters 2..13): h(z) = s - |z n S| - |L_0-pair(z) n S| - |L_1-pair(z) n S|.
Model (all constraints NECESSARY):
  line type mu_0, mu_1, sigma with the local caps of G_l and the cut;
  5 far + labels whose names partition X \\ {a,c}, 5 far - labels partitioning X \\ {b,d};
  each far support label has 2 + 2 attachments (non-mu pairs), pairs pairwise distinct (bijection), value formula;
  co-Heawood: 4 opposite-sign support neighbours, no same-sign neighbour, same-sign pairs share no off-support
  neighbour (letters, labels of L_0 u L_1) and exactly 2 support neighbours;
  linked condition for the 24 labels of L_0 u L_1 with h = 0 and for the points 0, 1.
UNSAT => no Conway graph has a sigma-sigma 2-cut with distinct letters at any root (for this s).
usage: python case1_coheawood.py <s> <seconds> [workers]"""
import itertools
import sys
import time

from ortools.sat.python import cp_model

s, secs = int(sys.argv[1]), float(sys.argv[2])
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 2
X = list(range(2, 14))
MATE = lambda x: x ^ 1
Sl = set(range(2, 2 + 2 * s))
m = cp_model.CpModel()
# ---------- line type
mu = {}
for r in (0, 1):
    for x, y in itertools.combinations(X, 2):
        mu[(r, x, y)] = mu[(r, y, x)] = m.NewBoolVar("")
    for x in X:
        m.AddExactlyOne([mu[(r, x, y)] for y in X if y != x])
        for y in X:
            if y != x and (x in Sl) != (y in Sl):
                m.Add(mu[(r, x, y)] == 0)          # no mu crossing
sg = {(x, y): m.NewBoolVar("") for x in X for y in X}
for x in X:
    m.AddExactlyOne([sg[(x, y)] for y in X])
    m.AddExactlyOne([sg[(y, x)] for y in X])
m.Add(sum(sg[(x, y)] for x in Sl for y in X if y not in Sl) == 1)
m.Add(sum(sg[(x, y)] for x in X if x not in Sl for y in Sl) == 1)
oneh = lambda name, dom: {v: m.NewBoolVar(name + str(v)) for v in dom}
A_ = oneh("a", sorted(Sl)); D_ = oneh("d", [x for x in X if x not in Sl])
B_ = oneh("b", [x for x in X if x not in Sl]); C_ = oneh("c", sorted(Sl))
for H in (A_, D_, B_, C_):
    m.AddExactlyOne(list(H.values()))
for x in Sl:
    for y in X:
        if y not in Sl:
            m.AddImplication(sg[(x, y)], A_[x]); m.AddImplication(sg[(x, y)], D_[y])
for x in X:
    if x not in Sl:
        for y in Sl:
            m.AddImplication(sg[(x, y)], B_[x]); m.AddImplication(sg[(x, y)], C_[y])
for x in Sl:
    m.AddBoolOr([A_[x].Not(), C_[x].Not()])       # a != c
for x in X:
    if x not in Sl:
        m.AddBoolOr([B_[x].Not(), D_[x].Not()])   # b != d
# G_l vertices and adjacency (literal or constant)
G = [("L", x) for x in X] + [(0, x) for x in X] + [(1, x) for x in X]
def gadj(u, w):
    if u == w:
        return 0
    if u[0] == "L" and w[0] == "L":
        return 1 if MATE(u[1]) == w[1] else 0
    if u[0] == "L" or w[0] == "L":
        return 1 if u[1] == w[1] else 0
    if u[0] == w[0]:
        return mu[(u[0], u[1], w[1])]
    return sg[(u[1], w[1])] if u[0] == 0 else sg[(w[1], u[1])]
def AND(p, q):
    if isinstance(p, int) or isinstance(q, int):
        if isinstance(p, int) and isinstance(q, int):
            return p * q
        return (q if p else 0) if isinstance(p, int) else (p if q else 0)
    z = m.NewBoolVar("")
    m.AddBoolOr([p.Not(), q.Not(), z]); m.AddImplication(z, p); m.AddImplication(z, q)
    return z
def ADD(ct_lhs, op, rhs, enforce=None):
    """add lhs op rhs unless it is constant (then check it)."""
    lhs = ct_lhs
    const = isinstance(lhs, int) and (isinstance(rhs, int))
    if const:
        ok = {"<=": lhs <= rhs, "==": lhs == rhs}[op]
        assert ok or enforce is not None, ("constant constraint violated", lhs, op, rhs)
        if not ok and enforce is not None:
            m.AddBoolOr([enforce.Not()])
        return
    ct = (lhs <= rhs) if op == "<=" else (lhs == rhs)
    c = m.Add(ct)
    if enforce is not None:
        c.OnlyEnforceIf(enforce)
for u, w in itertools.combinations(G, 2):          # local caps inside G_l
    terms = [AND(gadj(u, t), gadj(w, t)) for t in G if t not in (u, w)]
    e = gadj(u, w)
    same = 1 if u[0] == w[0] else 0
    ADD(sum(terms), "<=", (2 - same) - e if not isinstance(e, int) else (1 - same if e else 2 - same))
# ---------- h on G_l
hp = {u: 0 for u in G}
hn = {u: 0 for u in G}
for x in Sl:
    hp[(0, x)] = A_[x]; hp[(1, x)] = C_[x]
for x in X:
    if x not in Sl:
        hn[(0, x)] = B_[x]; hn[(1, x)] = D_[x]
# ---------- far labels
Dl = [frozenset((x, y)) for x, y in itertools.combinations(X, 2) if y != MATE(x)]
pos = [m.NewBoolVar("") for _ in Dl]
neg = [m.NewBoolVar("") for _ in Dl]
for k in range(60):
    m.AddBoolOr([pos[k].Not(), neg[k].Not()])
for x in X:
    inA = A_[x] if x in Sl else 0
    inC = C_[x] if x in Sl else 0
    inB = B_[x] if x not in Sl else 0
    inD = D_[x] if x not in Sl else 0
    m.Add(sum(pos[k] for k, z in enumerate(Dl) if x in z) + inA + inC == 1)
    m.Add(sum(neg[k] for k, z in enumerate(Dl) if x in z) + inB + inD == 1)
att = {}
for k in range(60):
    for r in (0, 1):
        for x in X:
            att[(k, r, x)] = m.NewBoolVar("")
    sup = m.NewBoolVar("")
    m.AddBoolOr([pos[k], neg[k], sup.Not()]); m.AddImplication(pos[k], sup); m.AddImplication(neg[k], sup)
    for r in (0, 1):
        if "--full" in sys.argv:
            m.Add(sum(att[(k, r, x)] for x in X) == 2)
        else:
            m.Add(sum(att[(k, r, x)] for x in X) == 2).OnlyEnforceIf(sup)
            m.Add(sum(att[(k, r, x)] for x in X) == 0).OnlyEnforceIf(sup.Not())
        for x, y in itertools.combinations(X, 2):          # attachment pair is not a mu pair
            m.AddBoolOr([att[(k, r, x)].Not(), att[(k, r, y)].Not(), mu[(r, x, y)].Not()])
    kv = len(Dl[k] & Sl)
    val = s - kv - sum(att[(k, r, x)] for r in (0, 1) for x in Sl)
    m.Add(val == 1).OnlyEnforceIf(pos[k])
    m.Add(val == -1).OnlyEnforceIf(neg[k])
    if "--full" in sys.argv:
        m.Add(val == 0).OnlyEnforceIf(sup.Not())
# distinct attachment pairs (bijection): two support labels never share both attachments in a star
for k, k2 in itertools.combinations(range(60), 2):
    for r in (0, 1):
        for x, y in itertools.combinations(X, 2):
            m.AddBoolOr([att[(k, r, x)].Not(), att[(k, r, y)].Not(), att[(k2, r, x)].Not(), att[(k2, r, y)].Not()])
# far-far support adjacency
F = {}
for k, k2 in itertools.combinations(range(60), 2):
    F[(k, k2)] = F[(k2, k)] = m.NewBoolVar("")
# signs as literals for all support candidates: far labels and the four L01 labels
def adjL(u, k):          # adjacency G_l vertex u - far label k
    if u[0] == "L":
        return 1 if u[1] in Dl[k] else 0
    return att[(k, u[0], u[1])]
# (i) co-Heawood counts at far support labels
for k in range(60):
    opp_p, opp_n, same_p, same_n = [], [], [], []
    for k2 in range(60):
        if k2 == k:
            continue
        opp_p.append(AND(F[(k, k2)], neg[k2])); same_p.append(AND(F[(k, k2)], pos[k2]))
    for u in G:
        if u[0] == "L":
            continue
        e = adjL(u, k)
        if not isinstance(hp[u], int):
            same_p.append(AND(e, hp[u]))
        if not isinstance(hn[u], int):
            opp_p.append(AND(e, hn[u]))
    m.Add(sum(opp_p) == 4).OnlyEnforceIf(pos[k])
    m.Add(sum(same_p) == 0).OnlyEnforceIf(pos[k])
    opp_n, same_n = [], []
    for k2 in range(60):
        if k2 == k:
            continue
        opp_n.append(AND(F[(k, k2)], pos[k2])); same_n.append(AND(F[(k, k2)], neg[k2]))
    for u in G:
        if u[0] == "L":
            continue
        e = adjL(u, k)
        if not isinstance(hn[u], int):
            same_n.append(AND(e, hn[u]))
        if not isinstance(hp[u], int):
            opp_n.append(AND(e, hp[u]))
    m.Add(sum(opp_n) == 4).OnlyEnforceIf(neg[k])
    m.Add(sum(same_n) == 0).OnlyEnforceIf(neg[k])
# (ii) co-Heawood counts at the four L01 support labels, and linked condition at the other labels of L_0 u L_1
for u in G:
    if u[0] == "L":
        continue
    plus = [AND(adjL(u, k), pos[k]) for k in range(60)] + [AND(gadj(u, t), hp[t]) for t in G if t != u and t[0] != "L" and not isinstance(hp[t], int)]
    minus = [AND(adjL(u, k), neg[k]) for k in range(60)] + [AND(gadj(u, t), hn[t]) for t in G if t != u and t[0] != "L" and not isinstance(hn[t], int)]
    isp = hp[u] if not isinstance(hp[u], int) else None
    isn = hn[u] if not isinstance(hn[u], int) else None
    lits = [x for x in (isp, isn) if x is not None]
    zero = m.NewBoolVar("")
    m.AddBoolOr(lits + [zero])
    for x in lits:
        m.AddBoolOr([x.Not(), zero.Not()])
    if isp is not None:
        m.Add(sum(minus) == 4).OnlyEnforceIf(isp); m.Add(sum(plus) == 0).OnlyEnforceIf(isp)
    if isn is not None:
        m.Add(sum(plus) == 4).OnlyEnforceIf(isn); m.Add(sum(minus) == 0).OnlyEnforceIf(isn)
    m.Add(sum(plus) == sum(minus)).OnlyEnforceIf(zero)
    m.Add(sum(plus) <= 1).OnlyEnforceIf(zero)
# (iii) same-sign far pairs share no off-support neighbour in L_0 u L_1 (letters: names disjoint already)
for k, k2 in itertools.combinations(range(60), 2):
    for r in (0, 1):
        for x in X:
            u = (r, x)
            supp_u = [hp[u], hn[u]]
            zero_u = [v for v in supp_u if not isinstance(v, int)]
            # if both k, k2 positive (or both negative) and attached to u, then u must be in the support
            for P_ in (pos, neg):
                m.AddBoolOr([P_[k].Not(), P_[k2].Not(), att[(k, r, x)].Not(), att[(k2, r, x)].Not()] + zero_u)

if "--full" in sys.argv:
    # (A') bijection: every non-mu pair of a star is the attachment pair of exactly one far label
    for r in (0, 1):
        for x, y in itertools.combinations(X, 2):
            prs = [AND(att[(k, r, x)], att[(k, r, y)]) for k in range(60)]
            m.Add(sum(prs) + mu[(r, x, y)] == 1)
    # (B) letter / label counts and (C) L_0 / L_1 cross counts (exact srg counts)
    def common_in_G(u, w):
        return sum(AND(gadj(u, t), gadj(w, t)) for t in G if t not in (u, w))
    for xl in X:
        for r in (0, 1):
            for x in X:
                u, w = ("L", xl), (r, x)
                tgt_adj = 1 if xl == x else 0
                lhs = sum(att[(k, r, x)] for k, z in enumerate(Dl) if xl in z)
                m.Add(lhs + common_in_G(u, w) == (1 if tgt_adj else 2))
    for x in X:
        for y in X:
            u, w = (0, x), (1, y)
            lhs = sum(AND(att[(k, 0, x)], att[(k, 1, y)]) for k in range(60))
            m.Add(lhs + common_in_G(u, w) + sg[(x, y)] == 2)
    # (D) linked condition at far labels off the support, (E) far degree 8
    for k in range(60):
        sup_k = m.NewBoolVar("")
        m.AddBoolOr([pos[k], neg[k], sup_k.Not()]); m.AddImplication(pos[k], sup_k); m.AddImplication(neg[k], sup_k)
        pl = [AND(F[(k, k2)], pos[k2]) for k2 in range(60) if k2 != k]
        mi = [AND(F[(k, k2)], neg[k2]) for k2 in range(60) if k2 != k]
        for u in G:
            if u[0] == "L":
                continue
            if not isinstance(hp[u], int):
                pl.append(AND(att[(k, u[0], u[1])], hp[u]))
            if not isinstance(hn[u], int):
                mi.append(AND(att[(k, u[0], u[1])], hn[u]))
        m.Add(sum(pl) == sum(mi)).OnlyEnforceIf(sup_k.Not())
        m.Add(sum(pl) <= 1).OnlyEnforceIf(sup_k.Not())
        m.Add(sum(F[(k, k2)] for k2 in range(60) if k2 != k) == 8)
sv = cp_model.CpSolver()
sv.parameters.num_search_workers = workers
sv.parameters.max_time_in_seconds = secs
t0 = time.time()
st = sv.Solve(m)
print("case I co-Heawood model, s = %d: %s in %.1f s (workers %d)" % (s, sv.StatusName(st), time.time() - t0, workers),
      flush=True)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    val = lambda H: [x for x, v in H.items() if sv.Value(v)]
    print("a, d, b, c =", val(A_), val(D_), val(B_), val(C_))
    print("+ far:", [sorted(Dl[k]) for k in range(60) if sv.Value(pos[k])])
    print("- far:", [sorted(Dl[k]) for k in range(60) if sv.Value(neg[k])])
