"""Refined cube-and-conquer enumeration of the PSD four-star structures invariant under a group (LAB 15/10/2026,
task T3: decisive test of (H-MATCH) in the family G1'' = <(0 1)M, (2 3)M''>, which has the true symmetry h (4 5) and
not h).

Level 1 ('rcubes'): distinct projections of the invariant admissible structures onto the pairs inside X_l (labels
meeting {0,1}) and inside X_m (labels meeting {2,3}): the whole side structures (M_0, M_1, sigma_l, M_2, M_3, sigma_m).
Level 2 ('solve i0 i1'): for each refined cube, the components C of H_l and of H_m are known; by the side-relation
lemma (CONWAY_CONSTRAINTS G21) every PSD structure satisfies T kappa_C = 0, i.e. for every label i outside the side
of C: sum_{j in C} Gamma_ij = ((3I - K) kappa_C)_i (an exact cardinality equation).  These equations are added under
an activation literal of the cube (so they do not constrain other cubes), all structures of the cube satisfying them
are enumerated (complete when UNSAT), and T, U >= 0 is tested numerically; PSD structures of nullity >= 13 are saved,
nullity >= 14 with matchings not h-related is a TARGET.  Structures excluded by the equations are not PSD, so the
enumeration of PSD structures is complete when every cube is complete.
usage: python enum_rcubes.py <generators> <prefix> rcubes [max seconds]
       python enum_rcubes.py <generators> <prefix> solve <i0> <i1> [max seconds per cube]"""
import itertools
import json
import random
import sys
import time
from fractions import Fraction as Fr

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS


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
sol = Solver()
for c in F.clauses:
    sol.add_clause(c)
nv = [F.n]
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
for (i, j) in list(e):
    nv[0] = max(nv[0], abs(e[(i, j)]))
Xl = [i for i in range(n) if S[i] & {0, 1}]
Xm = [i for i in range(n) if S[i] & {2, 3}]
inXl, inXm = set(Xl), set(Xm)
proj = [k for k in reps if (k[0] in inXl and k[1] in inXl) or (k[0] in inXm and k[1] in inXm)]

if mode == "rcubes":
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
        if len(cubes) % 1000 == 0:
            print("progress: %d refined cubes, %.0f s" % (len(cubes), time.time() - t0), flush=True)
    json.dump({"gens": gens_s, "proj_pairs": proj, "complete": complete, "cubes": cubes}, open(prefix + "_rcubes.json", "w"))
    print("%s: %d pair orbits, %d side-pair orbits, %d refined cubes (%s), %.0f s"
          % (gens_s, len(reps), len(proj), len(cubes), "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
    sys.exit(0)

i0, i1 = int(sys.argv[4]), int(sys.argv[5])
maxsec = float(sys.argv[6]) if len(sys.argv) > 6 else 1e9
cubes = json.load(open(prefix + "_rcubes.json"))["cubes"]
Kfr = [[Fr(kval(S[a], S[b])).limit_denominator(8) for b in range(n)] for a in range(n)]
Kf = np.array([[float(x) for x in row] for row in Kfr])
HP = [idx[frozenset({0: 1, 1: 0, 2: 3, 3: 2}.get(y, y) for y in s_)] for s_ in S]
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
sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
lit_of = {}
for k in proj:
    lit_of[e[k]] = k


def components(side_pairs_true, centre):
    """components of H_{line centre} from the true side pairs: letters W (unions of lines)."""
    others = [y for y in range(14) if y not in centre]
    par = {y: y for y in others}

    def find(y):
        while par[y] != y:
            par[y] = par[par[y]]
            y = par[y]
        return y
    for y in others:
        par[find(y)] = find(y ^ 1)
    for (i, j) in side_pairs_true:
        yi = [y for y in S[i] if y not in centre][0]
        yj = [y for y in S[j] if y not in centre][0]
        par[find(yi)] = find(yj)
    comps = {}
    for y in others:
        comps.setdefault(find(y), set()).add(y)
    return list(comps.values())


def add_card(rows_cols_targets, act):
    """for each (i, cols, r): sum_{j in cols} x_ij = r, guarded by the activation literal act (sequential DP)."""
    for i, cols, r in rows_cols_targets:
        lits = [e[(min(i, j), max(i, j))] for j in cols]
        if r < 0 or r > len(lits):
            sol.add_clause([-act])
            return False
        layer = {0: None}
        for t, x in enumerate(lits):
            rem = len(lits) - t - 1
            nxt = {}
            for v, yv in layer.items():
                for val, lit in ((v, -x), (v + 1, x)):
                    if not (val <= r <= val + rem):
                        sol.add_clause([-act, -lit] if yv is None else [-act, -yv, -lit])
                        continue
                    if val not in nxt:
                        nv[0] += 1
                        nxt[val] = nv[0]
                    sol.add_clause([-act, -lit, nxt[val]] if yv is None else [-act, -yv, -lit, nxt[val]])
            layer = nxt
        for v, yv in layer.items():
            if v != r:
                sol.add_clause([-act, -yv])
    return True


tot = {"structures": 0, "psd": 0, "targets": 0, "max_psd_nullity": 0, "cubes_complete": 0, "cubes": 0}
for ci in range(i0, min(i1, len(cubes))):
    cube = cubes[ci]
    t0 = time.time()
    true_pairs = []
    for x in cube:
        if x > 0:
            k = lit_of[x]
            # expand the orbit representative to the whole orbit: all pairs with the same literal value
            true_pairs.append(k)
    # all true side pairs (orbit images included): read them from a model of the cube
    ok, m = sol.solve(cube)
    if not ok:
        print("cube %d: unsatisfiable" % ci, flush=True)
        continue
    sideL = [(i, j) for i in Xl for j in Xl if i < j and m[e[(i, j)]]]
    sideM = [(i, j) for i in Xm for j in Xm if i < j and m[e[(i, j)]]]
    eqs = []
    for centre, side_pairs, side_set in (((0, 1), sideL, inXl), ((2, 3), sideM, inXm)):
        for W in components(side_pairs, centre):
            C = [i for i in range(n) if (S[i] & set(centre)) and ([y for y in S[i] if y not in centre][0] in W)]
            for i in range(n):
                if i in side_set:
                    continue
                r = -sum(Kfr[i][j] for j in C)
                assert r.denominator == 1
                eqs.append((i, [j for j in C], int(r)))
    nv[0] += 1
    act = nv[0]
    feasible = add_card(eqs, act)
    assum = cube + [act]
    cnt = npsd = targets = mx = 0
    complete = False
    while feasible and time.time() - t0 < maxsec:
        ok, m = sol.solve(assum)
        if not ok:
            complete = True
            break
        cnt += 1
        sol.add_clause([-e[k] if m[e[k]] else e[k] for k in reps])
        G = np.zeros((n, n))
        for (i, j), v in e.items():
            if i < j and m[v]:
                G[i, j] = G[j, i] = 1
        T = 3 * np.eye(n) - G - Kf
        lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
        lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
        if min(lt, lu) <= -1e-9:
            continue
        npsd += 1
        nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
        mx = max(mx, nul)
        if nul >= 13:
            broken = any(G[i, j] != G[HP[i], HP[j]] for (i, j) in sl)
            fn = "%s_rc%d_P%d_%d.json" % (prefix, ci, nul, npsd)
            json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "lambda_T": lt, "lambda_U": lu,
                       "nullity_numeric": nul, "matchings_broken": bool(broken),
                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]}, open(fn, "w"))
            if nul >= 14 and broken:
                targets += 1
                print("cube %d: TARGET: PSD nullity %d with BROKEN matchings, saved %s" % (ci, nul, fn), flush=True)
    if not feasible:
        complete = True
    tot["structures"] += cnt
    tot["psd"] += npsd
    tot["targets"] += targets
    tot["max_psd_nullity"] = max(tot["max_psd_nullity"], mx)
    tot["cubes_complete"] += complete
    tot["cubes"] += 1
    print("cube %d: %d component equations, %d structures, %d PSD, max PSD nullity %d, targets %d, %s, %.1f s"
          % (ci, len(eqs), cnt, npsd, mx, targets, "COMPLETE" if complete else "stopped", time.time() - t0), flush=True)
print("refined cubes [%d, %d): %s" % (i0, min(i1, len(cubes)), tot), flush=True)
