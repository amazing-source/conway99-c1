"""SDP relaxation of the PSD four-star structures of a symmetry family (LAB 15/10/2026, task T3).

Variables: x_o in [0, 1] for each orbit o of label pairs under the group (the edge indicator of every pair of o),
plus continuous y for (C2).  Constraints: (C1) exact star counts, (C1') caps, (C2) exactly as in psd_milp_group.py
(y_ijt >= x_it + x_jt - 1, sum_t y_ijt <= 2 - s - x_ij), optional G1PPCUTS (Codex's cuts for G1''), optional cube
fixings (CUBES json + index: M_0, M_2 fixed), and the two semidefinite constraints Q^T T(x) Q >= 0, Q^T U(x) Q >= 0
(Q = orthonormal basis of the complement of the star vectors, T(x) = 3I - K - Gamma(x), U = 7 Pi - T).  Every PSD
admissible structure of the family (and of the cube) is a feasible point; so PRIMAL INFEASIBLE (Clarabel certificate)
proves numerically that there is none.  Solver: Clarabel (interior point).
usage: python sdp_relax.py <generators> [cubes json] [cube index or i0:i1]"""
import itertools
import json
import os
import random
import sys
import time

import numpy as np
import scipy.sparse as sp
import clarabel

from stars_rank import kval, count_needed, LABELS, build


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14))
    return h


gens_s = sys.argv[1]
S, idx, _e, _F = build([0, 1, 2, 3], random.Random(1))
n = len(S)
gens = [parse(c) for c in gens_s.split("|")]
gl = [[idx[frozenset(h[y] for y in S[i])] for i in range(n)] for h in gens]
group = {tuple(range(n))}
frontier = [tuple(range(n))]
while frontier:
    nxt = []
    for g in frontier:
        for m in gl:
            gm = tuple(m[g[i]] for i in range(n))
            if gm not in group:
                group.add(gm)
                nxt.append(gm)
    frontier = nxt
group = [list(g) for g in group]
pairs = list(itertools.combinations(range(n), 2))
orb_of, orbits = {}, []
for p in pairs:
    if p in orb_of:
        continue
    members = sorted({(min(g[p[0]], g[p[1]]), max(g[p[0]], g[p[1]])) for g in group})
    for q in members:
        orb_of[q] = len(orbits)
    orbits.append(members)
NO = len(orbits)
ev = lambda i, j: orb_of[(min(i, j), max(i, j))]
eq_rows, eq_b, le_rows, le_b = [], [], [], []      # rows: dict var -> coef ; eq: row.x = b ; le: row.x <= b
nv = NO
for i in range(n):
    for y in range(14):
        lits = [ev(i, t) for t in range(n) if t != i and y in S[t]]
        if not lits:
            continue
        co = {}
        for v in lits:
            co[v] = co.get(v, 0) + 1
        c = count_needed(S[i], y)
        if y in (0, 1, 2, 3):
            eq_rows.append(co); eq_b.append(c)
        else:
            le_rows.append(co); le_b.append(c)
for o in range(NO):
    le_rows.append({o: 1}); le_b.append(1)
    le_rows.append({o: -1}); le_b.append(0)
for o in range(NO):
    (i, j) = orbits[o][0]
    s_ = len(S[i] & S[j])
    co = {o: 1}
    for t in range(n):
        if t in (i, j):
            continue
        y = nv
        nv += 1
        co[y] = 1
        le_rows.append({y: -1, ev(i, t): 1, ev(j, t): 1}); le_b.append(1)     # y >= x_it + x_jt - 1
        le_rows.append({y: -1}); le_b.append(0)                                # y >= 0
    le_rows.append(co); le_b.append(2 - s_)
if os.environ.get("G1PPCUTS"):
    L_ = lambda a, b: idx[frozenset((a, b))]
    Fl = [(0, 4), (0, 5), (1, 4), (1, 5)]
    for b in (2, 3):
        for y in (4, 5):
            for f in Fl:
                eq_rows.append({ev(L_(b, y), L_(*f)): 1}); eq_b.append(0)
    canon = {}
    for y in (6, 8):
        canon[(2, y)] = (0, 4); canon[(2, y ^ 1)] = (1, 5); canon[(3, y)] = (1, 5); canon[(3, y ^ 1)] = (0, 4)
    for y in (10, 12):
        canon[(2, y)] = (0, 5); canon[(2, y ^ 1)] = (1, 4); canon[(3, y)] = (1, 4); canon[(3, y ^ 1)] = (0, 5)
    for lab, f in canon.items():
        for f2 in Fl:
            eq_rows.append({ev(L_(*lab), L_(*f2)): 1}); eq_b.append(1 if f2 == f else 0)
    for y in (6, 8, 10, 12):
        co = {}
        for q in ((2, y ^ 1), (3, y), (3, y ^ 1)):
            v = ev(L_(2, y), L_(*q))
            co[v] = co.get(v, 0) + 1
        le_rows.append(co); le_b.append(1)
Kf = np.array([[kval(a, b) for b in S] for a in S])
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
U_, s_, _ = np.linalg.svd(Z, full_matrices=True)
Q = U_[:, 4:]                                     # 44 x 40, orthonormal complement of the star vectors
m = Q.shape[1]
iu = [(r, c) for c in range(m) for r in range(c + 1)]   # upper triangle, column-major (Clarabel's svec order)
sc = np.array([1.0 if r == c else np.sqrt(2.0) for (r, c) in iu])


def svec(Mt):
    return np.array([Mt[r, c] for (r, c) in iu]) * sc


T0 = Q.T @ (3 * np.eye(n) - Kf) @ Q              # T(x) = T0 - sum_o x_o Q^T E_o Q
U0 = Q.T @ (7 * PiS - (3 * np.eye(n) - Kf)) @ Q   # U(x) = U0 + sum_o x_o Q^T E_o Q
Ecols = []
for o in range(NO):
    E = np.zeros((n, n))
    for (i, j) in orbits[o]:
        E[i, j] += 1
        E[j, i] += 1
    Ecols.append(svec(Q.T @ E @ Q))
Ecols = np.array(Ecols).T                         # (m(m+1)/2) x NO


def build_and_solve(fix):
    rows_A, b = [], []
    # equalities (ZeroCone): A x + s = b with s = 0 -> A = row, b
    nz = len(eq_rows) + len(fix)
    data, ri, ci = [], [], []
    r = 0
    for co, bb in zip(eq_rows, eq_b):
        for v, c in co.items():
            data.append(c); ri.append(r); ci.append(v)
        b.append(bb); r += 1
    for v, val in fix:
        data.append(1.0); ri.append(r); ci.append(v)
        b.append(val); r += 1
    nzero = r
    for co, bb in zip(le_rows, le_b):            # A x + s = b, s >= 0  <=>  row.x <= b
        for v, c in co.items():
            data.append(c); ri.append(r); ci.append(v)
        b.append(bb); r += 1
    nnon = r - nzero
    # PSD cones: s = b - A x = svec(T(x)) = svec(T0) - sum x_o Ecol_o  -> A = +Ecol, b = svec(T0)
    t0v = svec(T0)
    for k in range(len(t0v)):
        for o in np.nonzero(np.abs(Ecols[k]) > 1e-14)[0]:
            data.append(Ecols[k, o]); ri.append(r); ci.append(o)
        b.append(t0v[k]); r += 1
    u0v = svec(U0)
    for k in range(len(u0v)):                    # s = svec(U(x)) = svec(U0) + sum x_o Ecol_o -> A = -Ecol
        for o in np.nonzero(np.abs(Ecols[k]) > 1e-14)[0]:
            data.append(-Ecols[k, o]); ri.append(r); ci.append(o)
        b.append(u0v[k]); r += 1
    A = sp.csc_matrix((data, (ri, ci)), shape=(r, nv))
    P = sp.csc_matrix((nv, nv))
    q = np.zeros(nv)
    cones = [clarabel.ZeroConeT(nzero), clarabel.NonnegativeConeT(nnon), clarabel.PSDTriangleConeT(m),
             clarabel.PSDTriangleConeT(m)]
    settings = clarabel.DefaultSettings()
    settings.verbose = False
    settings.max_iter = 500
    solver = clarabel.DefaultSolver(P, q, A, np.array(b, float), cones, settings)
    t = time.time()
    sol = solver.solve()
    return str(sol.status), np.array(sol.x), time.time() - t


print("group of order %d, %d orbits, %d variables, PSD cones of size %d" % (len(group), NO, nv, m), flush=True)
if len(sys.argv) <= 2:
    st, x, dt = build_and_solve([])
    xs = x[:NO]
    print("whole family: status %s (%.1f s); fractional orbits %d" % (st, dt, int(np.sum((xs > 1e-4) & (xs < 1 - 1e-4)))),
          flush=True)
    sys.exit(0)
cd = json.load(open(sys.argv[2]))
cubes, proj = cd["cubes"], [tuple(p) for p in cd["proj_pairs"]]
rng_s = sys.argv[3]
i0, i1 = (int(rng_s.split(":")[0]), int(rng_s.split(":")[1])) if ":" in rng_s else (int(rng_s), int(rng_s) + 1)
summ = {}
for ci in range(i0, min(i1, len(cubes))):
    fix = [(ev(*k), 1.0 if lit > 0 else 0.0) for k, lit in zip(proj, cubes[ci])]
    st, x, dt = build_and_solve(fix)
    summ[st] = summ.get(st, 0) + 1
    print("cube %d: %s (%.1f s)" % (ci, st, dt), flush=True)
print("cubes [%d, %d): %s" % (i0, min(i1, len(cubes)), summ), flush=True)
