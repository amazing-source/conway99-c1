"""Readable form of the 7-adic drop of a four-star block (exploration, LAB 16/10/2026).
ker_7 = {g : 8T_S g = 0 mod 7}; N_7 = reduction mod 7 of the saturated integral kernel of T_S (the liftable part).
For the quotient ker_7 / N_7 (dimension = rank_Q - rank_F7) we look for vectors of MINIMAL SUPPORT in ker_7 \ N_7
(CP-SAT, exact: g = sum a_i b_i - 7 q, balanced entries in [-3, 3], at least one non-liftable coordinate a_i != 0).
Then we peel: fix the minimal vector, add it to N_7, repeat, to get a readable basis of the whole drop.
Prints each vector in label notation, with the block's structural data (corner square, the line components).
usage: python f7_minsupport.py <block json> [seconds per solve]"""
import itertools
import json
import sys

import numpy as np
import sympy as sp
from ortools.sat.python import cp_model

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from f7_kernel_look import t8, rref_mod, null_mod, load  # noqa: E402

path = sys.argv[1]
secs = float(sys.argv[2]) if len(sys.argv) > 2 else 60.0
S, E = load(path)
names = ["".join(str(t) for t in sorted(l)) for l in S]
M = t8(S, E)
k7 = null_mod(M.tolist(), 7)
ker = sp.Matrix(M.tolist()).nullspace()
Kint = []
for v in ker:
    den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
    w = [int(x * den) for x in v]
    g = 0
    for x in w:
        g = sp.igcd(g, x)
    Kint.append([x // g for x in w])
# saturate the integral kernel at 7
while Kint and len(rref_mod(Kint, 7)[0]) < len(Kint):
    Mt = [[Kint[i][j] for i in range(len(Kint))] for j in range(44)]
    c = null_mod(Mt, 7)[0]
    vec = [sum((c[i] if c[i] <= 3 else c[i] - 7) * Kint[i][j] for i in range(len(Kint))) for j in range(44)]
    i0 = next(i for i in range(len(c)) if c[i])
    Kint[i0] = [x // 7 for x in vec]
N7 = rref_mod(Kint, 7)[0]
drop = len(k7) - len(N7)
print("block %s: rank_Q %d, rank_F7 %d, drop %d" % (path.replace("\\", "/").split("/")[-1], 44 - len(ker),
                                                   44 - len(k7), drop))


def minimal_nonliftable(base, extra):
    """minimise the support of g in span(base + extra) mod 7 with some extra-coefficient non-zero"""
    B = base + extra
    nb, ne = len(base), len(extra)
    m = cp_model.CpModel()
    a = [m.NewIntVar(0, 6, "a%d" % i) for i in range(nb + ne)]
    nz = []
    for i in range(nb, nb + ne):
        b = m.NewBoolVar("")
        m.Add(a[i] >= 1).OnlyEnforceIf(b)
        m.Add(a[i] == 0).OnlyEnforceIf(b.Not())
        nz.append(b)
    m.AddBoolOr(nz)
    gs, sup = [], []
    for j in range(44):
        gj = m.NewIntVar(-3, 3, "g%d" % j)
        qj = m.NewIntVar(-200, 200, "q%d" % j)
        m.Add(sum(int(B[i][j]) * a[i] for i in range(nb + ne)) - 7 * qj == gj)
        s = m.NewBoolVar("")
        m.Add(gj == 0).OnlyEnforceIf(s.Not())
        gs.append(gj)
        sup.append(s)
    m.Minimize(sum(sup))
    sv = cp_model.CpSolver()
    sv.parameters.num_search_workers = 8
    sv.parameters.max_time_in_seconds = secs
    st = sv.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, sv.StatusName(st)
    return [sv.Value(x) for x in gs], sv.StatusName(st)


# complement basis
comp = []
for g in k7:
    if len(rref_mod(N7 + comp + [g], 7)[0]) > len(N7) + len(comp):
        comp.append(g)
base = [list(r) for r in N7]
found = []
for step in range(drop):
    # remaining complement: those not yet in span(base)
    rem = [g for g in comp if len(rref_mod(base + [g], 7)[0]) > len(base)]
    g, st = minimal_nonliftable(base, rem)
    if g is None:
        print("solver:", st)
        break
    supp = [(names[j], g[j]) for j in range(44) if g[j]]
    print("drop vector %d (%s, support %d): %s" % (step + 1, st, len(supp), supp))
    found.append(g)
    base = base + [[x % 7 for x in g]]
corners = [frozenset(p) for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
print("corner edges:", [("".join(map(str, sorted(a))), "".join(map(str, sorted(b))))
                        for a, b in itertools.combinations(corners, 2) if frozenset((a, b)) in E])
for r in range(4):
    Lr = [l for l in S if r in l]
    pairs = [("".join(map(str, sorted(a))), "".join(map(str, sorted(b)))) for a, b in itertools.combinations(Lr, 2)
             if frozenset((a, b)) in E]
    print("M_%d:" % r, pairs)
