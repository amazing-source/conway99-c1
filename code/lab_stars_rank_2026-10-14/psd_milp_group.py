"""Does a symmetry family contain ANY four-star structure with T, U >= 0?  MILP with positivity cutting planes
(LAB 15/10/2026, task T3, decisive test of (H-MATCH) in G1'' = <(0 1)M, (2 3)M''>).

Variables: one 0/1 variable per orbit of label pairs under the group.  Linear constraints: (C1) exact star counts,
(C1') caps.  Lazy constraints, added when violated by the current MILP solution: (C2) common-neighbour caps (as in
kernel_milp.py), and the positivity cuts  sum_{i<j} 2 c_i c_j Gamma_ij <= c^T (3I - K) c  for every eigenvector c of T
(on the complement of the star vectors) with a negative eigenvalue, and  sum 2 c_i c_j Gamma_ij >= c^T (3I - K - 7 Pi) c
for U; every cut is valid for every structure with T >= 0 (resp. U >= 0) and is symmetrised over the group.  Optional
extra cuts valid for PSD structures (G1PPCUTS=1, Codex 808-809, see enum_cubes.py).  Objective: maximise the number of
broken star-matching orbit pairs (MODE=broken, default) or nothing (MODE=feas).  Stops when the MILP is infeasible
(no PSD structure in the family, modulo floating-point cut tolerances), or at a PSD structure (printed and saved, with
its numerical nullity and h-relation), or at the time limit.  NOGOOD=1 keeps going after each PSD structure (no-good
cut) to collect them.
usage: python psd_milp_group.py <generators> <out prefix> [time limit s]"""
import itertools
import json
import os
import random
import sys
import time

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

from stars_rank import kval, count_needed, LABELS, build


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14))
    return h


gens_s, out = sys.argv[1], sys.argv[2]
tlim = float(sys.argv[3]) if len(sys.argv) > 3 else 1800
mode = os.environ.get("MODE", "broken")
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
orb_of = {}
orbits = []
for p in pairs:
    if p in orb_of:
        continue
    o = len(orbits)
    members = {(min(g[p[0]], g[p[1]]), max(g[p[0]], g[p[1]])) for g in group}
    for q in members:
        orb_of[q] = o
    orbits.append(sorted(members))
NO = len(orbits)
print("group of order %d, %d pair orbits" % (len(group), NO), flush=True)
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
sl = [(i, j) for (i, j) in pairs if S[i] & S[j] & {0, 1, 2, 3}]
# broken indicator orbits: star pairs p with h(p) in a different orbit
bro = []
seenb = set()
for (i, j) in sl:
    q = (min(hp[i], hp[j]), max(hp[i], hp[j]))
    a, b = orb_of[(i, j)], orb_of[q]
    if a != b and (a, b) not in seenb and (b, a) not in seenb:
        seenb.add((a, b))
        bro.append((a, b))
nv = NO + len(bro)
rows, lo, hi = [], [], []


def add(coeffs, l, u):
    rows.append(coeffs)
    lo.append(l)
    hi.append(u)


def ev(i, j):
    return orb_of[(min(i, j), max(i, j))]


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
            add(co, c, c)
        else:
            add(co, 0, c)
for t, (a, b) in enumerate(bro):
    add({NO + t: 1, a: -1, b: -1}, -np.inf, 0)
    add({NO + t: 1, a: 1, b: 1}, -np.inf, 2)
if os.environ.get("G1PPCUTS"):
    L_ = lambda a, b: idx[frozenset((a, b))]
    Fl = [(0, 4), (0, 5), (1, 4), (1, 5)]
    for b in (2, 3):
        for y in (4, 5):
            for f in Fl:
                add({ev(L_(b, y), L_(*f)): 1}, 0, 0)
    canon = {}
    for y in (6, 8):
        canon[(2, y)] = (0, 4); canon[(2, y ^ 1)] = (1, 5); canon[(3, y)] = (1, 5); canon[(3, y ^ 1)] = (0, 4)
    for y in (10, 12):
        canon[(2, y)] = (0, 5); canon[(2, y ^ 1)] = (1, 4); canon[(3, y)] = (1, 4); canon[(3, y ^ 1)] = (0, 5)
    for lab, f in canon.items():
        for f2 in Fl:
            v = ev(L_(*lab), L_(*f2))
            add({v: 1}, 1 if f2 == f else 0, 1 if f2 == f else 0)
    for y in (6, 8, 10, 12):
        co = {}
        for q in ((2, y ^ 1), (3, y), (3, y ^ 1)):
            v = ev(L_(2, y), L_(*q))
            co[v] = co.get(v, 0) + 1
        add(co, -np.inf, 1)
    print("G1PPCUTS added", flush=True)
NB = nv                                      # binary variables: orbit edges + broken indicators
if os.environ.get("EXACTC2"):
    # (C2) exactly: for every pair {i, j} (one per orbit) with s = |S_i n S_j| shared letters,
    #   sum_t y_ijt <= 2 - s - x_ij,  y_ijt >= x_it + x_jt - 1,  y_ijt in [0, 1] continuous
    # (the number of common neighbours inside S is at most 1 - s if adjacent and 2 - s if not)
    rep_pairs = [orbits[o][0] for o in range(NO)]
    for (i, j) in rep_pairs:
        s_ = len(S[i] & S[j])
        co = {ev(i, j): 1}
        for t in range(n):
            if t in (i, j):
                continue
            y = nv
            nv += 1
            co[y] = 1
            add({y: 1, ev(i, t): -1, ev(j, t): -1}, -1, np.inf)
        add(co, -np.inf, 2 - s_)
    print("EXACTC2: %d continuous product variables" % (nv - NB), flush=True)
Kf = np.array([[kval(a, b) for b in S] for a in S])
KC = 3 * np.eye(n) - Kf
D84 = np.zeros((14, 84))
for jj, l in enumerate(LABELS):
    for y in l:
        D84[y, jj] = 1
Pi = np.eye(84) - D84.T @ np.linalg.inv(D84 @ D84.T) @ D84
pos = {l: ii for ii, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
t0 = time.time()
c2cuts = psdcuts = 0
found = 0
it = 0
while time.time() - t0 < tlim:
    it += 1
    A = lil_matrix((len(rows), nv))
    for r, co in enumerate(rows):
        for v, c in co.items():
            A[r, v] = c
    cvec = np.zeros(nv)
    if mode == "broken":
        cvec[NO:] = -1.0
    res = milp(cvec, constraints=LinearConstraint(A.tocsr(), np.array(lo, float), np.array(hi, float)),
               integrality=np.concatenate([np.ones(NB), np.zeros(nv - NB)]), bounds=Bounds(0, 1),
               options={"time_limit": max(10.0, tlim - (time.time() - t0)), "disp": False})
    if res.x is None:
        print("MILP status %d (%s): NO FEASIBLE STRUCTURE left (C2 cuts %d, positivity cuts %d, PSD found %d, %d "
              "iterations, %.0f s)" % (res.status, res.message, c2cuts, psdcuts, found, it, time.time() - t0), flush=True)
        break
    x = np.rint(res.x[:NO]).astype(int)
    G = np.zeros((n, n))
    for (i, j) in pairs:
        if x[orb_of[(i, j)]]:
            G[i, j] = G[j, i] = 1
    viol = 0
    for i, j in pairs:
        s_ = len(S[i] & S[j])
        com = [t for t in range(n) if t != i and t != j and G[i, t] and G[j, t]]
        cap = (1 - s_) if G[i, j] else (2 - s_)
        if len(com) > cap:
            viol += 1
            co = {}
            if G[i, j]:
                Cp = com[:max(0, 1 - s_) + 1]
                co[ev(i, j)] = co.get(ev(i, j), 0) + 1
                for t in Cp:
                    co[ev(i, t)] = co.get(ev(i, t), 0) + 1
                    co[ev(j, t)] = co.get(ev(j, t), 0) + 1
                add(co, -np.inf, 2 * len(Cp))
            else:
                Cp = com[:(2 - s_) + 1]
                for t in Cp:
                    co[ev(i, t)] = co.get(ev(i, t), 0) + 1
                    co[ev(j, t)] = co.get(ev(j, t), 0) + 1
                co[ev(i, j)] = co.get(ev(i, j), 0) - 1
                add(co, -np.inf, 2 * len(Cp) - 1)
            c2cuts += 1
    if viol:
        continue
    T = 3 * np.eye(n) - G - Kf
    MT = Pp @ T @ Pp + 50 * (np.eye(n) - Pp)
    MU = Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp)
    wt, Vt = np.linalg.eigh(MT)
    wu, Vu = np.linalg.eigh(MU)
    if wt[0] > -1e-9 and wu[0] > -1e-9:
        found += 1
        nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
        broken = any(G[i, j] != G[hp[i], hp[j]] for (i, j) in sl)
        fn = "%s_PSD_%d.json" % (out, found)
        json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "nullity_numeric": nul, "matchings_broken": broken,
                   "lambda_T": float(wt[0]), "lambda_U": float(wu[0]),
                   "edges": [[i, j] for (i, j) in pairs if G[i, j]]}, open(fn, "w"))
        print("iteration %d: PSD STRUCTURE (nullity %d, matchings %s), saved %s, %.0f s"
              % (it, nul, "BROKEN" if broken else "h-related", fn, time.time() - t0), flush=True)
        if not os.environ.get("NOGOOD"):
            break
        co = {}
        ones = 0
        for o in range(NO):
            if x[o]:
                co[o] = co.get(o, 0) - 1
                ones += 1
            else:
                co[o] = co.get(o, 0) + 1
        add(co, 1 - ones, np.inf)
        continue
    new = 0
    for (w, V, sign) in ((wt, Vt, 1), (wu, Vu, -1)):
        for q in range(n):
            if w[q] > -1e-9:
                break
            for g in group[:1]:              # images under the group give the SAME cut on invariant structures
                c = np.zeros(n)
                c[g] = V[:, q]
                co = {}
                for (i, j) in pairs:
                    a = 2 * c[i] * c[j]
                    if abs(a) > 1e-12:
                        o = orb_of[(i, j)]
                        co[o] = co.get(o, 0) + a
                base = float(c @ KC @ c)
                if sign == 1:
                    add(co, -np.inf, base + 1e-7)
                else:
                    add(co, base - 7 * float(c @ PiS @ c) - 1e-7, np.inf)
                new += 1
    psdcuts += new
    if it % 10 == 0:
        print("iteration %d: lambda_T %.4f, lambda_U %.4f, C2 cuts %d, positivity cuts %d, %.0f s"
              % (it, wt[0], wu[0], c2cuts, psdcuts, time.time() - t0), flush=True)
print("end: %d iterations, C2 cuts %d, positivity cuts %d, PSD structures found %d, %.0f s"
      % (it, c2cuts, psdcuts, found, time.time() - t0), flush=True)
