"""Two-level (cube-and-conquer) exhaustive enumeration of the four-star structures invariant under a group
(LAB 15/10/2026, task T3: decisive test of (H-MATCH) in families with a TRUE symmetry that does not contain h).

Same SAT model and orbit tying as enum_group.py.  Level 1 ('cubes'): enumerate the distinct projections of the
invariant admissible structures onto the pairs inside the stars L_0 and L_2 (the star matchings M_0, M_2; the others
follow by symmetry in the groups of interest), blocking on those pairs only; write the cubes to <prefix>_cubes.json.
Level 2 ('solve i0 i1'): for each cube in [i0, i1), enumerate ALL invariant admissible structures under the cube
assumptions (complete when UNSAT), test T, U >= 0 numerically, and for the PSD ones compute the numerical nullity,
c(l), c(m) and whether the star matchings are h-related (h = (0 1)(2 3), M_1 = s_m M_0 and M_3 = s_l M_2).  Every
PSD structure of nullity >= 13 is saved; a PSD structure of nullity >= 14 with broken matchings is reported as a
TARGET (it would refute (H-MATCH) after an exact check).  Cubes are disjoint, so level 2 can be split into
independent jobs; a per-cube summary line is printed (cube index, structures, PSD, max PSD nullity, targets, COMPLETE).
usage: python enum_cubes.py <generators> <prefix> cubes [max seconds]
       python enum_cubes.py <generators> <prefix> solve <i0> <i1> [max seconds per cube]"""
import itertools
import json
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14))
    return h


gens_s, prefix, mode = sys.argv[1], sys.argv[2], sys.argv[3]
gens = [parse(c) for c in gens_s.split("|")]
S, idx, e, F = build([0, 1, 2, 3], random.Random(1))
n = len(S)


def model_with_orbits():
    sol = Solver()
    for c in F.clauses:
        sol.add_clause(c)
    gl = [{i: idx[frozenset(h[y] for y in S[i])] for i in range(n)} for h in gens]
    reps, seen = [], set()
    for i, j in itertools.combinations(range(n), 2):
        orb, stack = {(i, j)}, [(i, j)]
        while stack:
            a, b = stack.pop()
            for m in gl:
                p = (min(m[a], m[b]), max(m[a], m[b]))
                if p not in orb:
                    orb.add(p)
                    stack.append(p)
        key = min(orb)
        if key in seen:
            continue
        seen.add(key)
        reps.append(key)
        for p in orb:
            if p != key:
                sol.add_clause([-e[key], e[p]])
                sol.add_clause([e[key], -e[p]])
    return sol, reps


sol, reps = model_with_orbits()
import os
for _env, (_a0, _a1) in (("FORCE_TL", (0, 1)), ("FORCE_TM", (2, 3))):
    # FORCE_TL / FORCE_TM (15/10): impose the transversals {a0,x} ~ {a1,x} at the listed letters x
    if os.environ.get(_env):
        for _x in [int(t) for t in os.environ[_env].split(",")]:
            _i, _j = idx[frozenset((_a0, _x))], idx[frozenset((_a1, _x))]
            sol.add_clause([e[(min(_i, _j), max(_i, _j))]])
        print("%s imposed at %s" % (_env, os.environ[_env]), flush=True)
if os.environ.get("G1PPCUTS"):
    # 15/10, 11:25 UTC: cuts valid for every PSD structure of G1'' = <(0 1)M, (2 3)M''> (Codex messages 808-809,
    # re-derived): (a) the square F = {04, 05, 14, 15} is the component {4,5} of H_l, so T kappa_F = 0: every m-only
    # label {b, y} has 0 neighbours in F if y in {4,5} and exactly 1 if y in 6..13; (b) normalisation of the F-interface
    # under the wreath group C2 wr S4 of the pairs 6/7, 8/9, 10/11, 12/13 (it normalises G1'' and is transitive on the
    # 96 interfaces allowed by (a) and C1): {2,y} ~ 04, {2,y^1} ~ 15, {3,y} ~ 15, {3,y^1} ~ 04 for y = 6, 8, and the
    # same with 05, 14 for y = 10, 12; (c) d_P <= 1 for P = {y, y^1}, y = 6, 8, 10, 12 (2 x 2 minor with the F-mode
    # q_F): Gamma[2y, 2y^1] + Gamma[2y, 3y] + Gamma[2y, 3y^1] <= 1.  (b) keeps one representative of every orbit of PSD
    # structures, so with (b) the enumeration is complete for PSD structures up to that symmetry.
    L_ = lambda a, b: idx[frozenset((a, b))]
    E_ = lambda p, q: e[(min(L_(*p), L_(*q)), max(L_(*p), L_(*q)))]
    Fl = [(0, 4), (0, 5), (1, 4), (1, 5)]
    for b in (2, 3):
        for y in range(4, 14):
            lits = [E_((b, y), f) for f in Fl]
            if y in (4, 5):
                for x in lits:
                    sol.add_clause([-x])
    canon = {}
    for y in (6, 8):
        canon[(2, y)] = (0, 4); canon[(2, y ^ 1)] = (1, 5); canon[(3, y)] = (1, 5); canon[(3, y ^ 1)] = (0, 4)
    for y in (10, 12):
        canon[(2, y)] = (0, 5); canon[(2, y ^ 1)] = (1, 4); canon[(3, y)] = (1, 4); canon[(3, y ^ 1)] = (0, 5)
    for lab, f in canon.items():
        for f2 in Fl:
            sol.add_clause([E_(lab, f2)] if f2 == f else [-E_(lab, f2)])
    for y in (6, 8, 10, 12):
        trio = [E_((2, y), (2, y ^ 1)), E_((2, y), (3, y)), E_((2, y), (3, y ^ 1))]
        for a_, b_ in itertools.combinations(trio, 2):
            sol.add_clause([-a_, -b_])
    print("G1PPCUTS: F-square counts, canonical F-interface and d_P <= 1 cuts added", flush=True)
proj = [k for k in reps if all(a in S[k[0]] and a in S[k[1]] for a in (0,)) or all(a in S[k[0]] and a in S[k[1]] for a in (2,))]
if mode == "cubes":
    maxsec = float(sys.argv[4]) if len(sys.argv) > 4 else 3600
    t0 = time.time()
    cubes = []
    complete = False
    while time.time() - t0 < maxsec:
        ok, m = sol.solve()
        if not ok:
            complete = True
            break
        cube = [e[k] if m[e[k]] else -e[k] for k in proj]
        cubes.append(cube)
        sol.add_clause([-x for x in cube])
    json.dump({"gens": gens_s, "proj_pairs": proj, "complete": complete, "cubes": cubes}, open(prefix + "_cubes.json", "w"))
    print("%s: %d pair orbits, %d projection orbits (pairs inside L_0 or L_2), %d cubes (%s), %.0f s"
          % (gens_s, len(reps), len(proj), len(cubes), "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
    sys.exit(0)

i0, i1 = int(sys.argv[4]), int(sys.argv[5])
maxsec = float(sys.argv[6]) if len(sys.argv) > 6 else 1e9
cubes = json.load(open(prefix + "_cubes.json"))["cubes"]
HP = [idx[frozenset({0: 1, 1: 0, 2: 3, 3: 2}.get(y, y) for y in s_)] for s_ in S]
K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
D = np.zeros((14, 84))
for j, l in enumerate(LABELS):
    for y in l:
        D[y, j] = 1
Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
pos = {l: i for i, l in enumerate(LABELS)}
PiS = Pi[np.ix_([pos[l] for l in S], [pos[l] for l in S])]
Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in (0, 1, 2, 3)]).T
Qz, _ = np.linalg.qr(Z)
Pp = np.eye(n) - Qz @ Qz.T
Xl = [i for i in range(n) if S[i] & {0, 1}]
Xm = [i for i in range(n) if S[i] & {2, 3}]
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
tot = {"structures": 0, "psd": 0, "targets": 0, "max_psd_nullity": 0, "cubes_complete": 0}
for ci in range(i0, min(i1, len(cubes))):
    cube = cubes[ci]
    t0 = time.time()
    cnt = npsd = targets = 0
    mx = 0
    complete = False
    while time.time() - t0 < maxsec:
        ok, m = sol.solve(cube)
        if not ok:
            complete = True
            break
        cnt += 1
        sol.add_clause([-e[k] if m[e[k]] else e[k] for k in reps])
        G = np.zeros((n, n), dtype=np.int64)
        for (i, j), v in e.items():
            if i < j and m[v]:
                G[i, j] = G[j, i] = 1
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        T = M8 / 8.0
        lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
        lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
        if min(lt, lu) <= -1e-9:
            continue
        npsd += 1
        nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
        mx = max(mx, nul)
        if nul >= int(os.environ.get("SAVEMIN", "13")):
            broken = any(G[i, j] != G[HP[i], HP[j]] for (i, j) in sl)
            cl = 23 - exact_rank([[int(M8[a][b]) for b in Xl] for a in Xl])
            cm = 23 - exact_rank([[int(M8[a][b]) for b in Xm] for a in Xm])
            fn = "%s_c%d_P%d_%d.json" % (prefix, ci, nul, npsd)
            json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt, "lambda_U": lu,
                       "nullity_numeric": nul, "matchings_broken": bool(broken),
                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]}, open(fn, "w"))
            if nul >= 14 and broken:
                targets += 1
                print("cube %d: TARGET: PSD nullity %d with BROKEN matchings, c = (%d,%d), saved %s" % (ci, nul, cl, cm, fn),
                      flush=True)
    tot["structures"] += cnt
    tot["psd"] += npsd
    tot["targets"] += targets
    tot["max_psd_nullity"] = max(tot["max_psd_nullity"], mx)
    tot["cubes_complete"] += complete
    print("cube %d: %d structures, %d PSD, max PSD nullity %d, targets %d, %s, %.0f s"
          % (ci, cnt, npsd, mx, targets, "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
print("cubes [%d, %d): %s" % (i0, min(i1, len(cubes)), tot), flush=True)
