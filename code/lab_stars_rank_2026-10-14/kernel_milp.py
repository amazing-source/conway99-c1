"""Kernel-imposed MILP (LAB 15/10/2026, (H-MATCH) / (H-INV) rigidity test).

ker T contains a given 14-dimensional space N  <=>  Gamma N = (3I - K) N, which is LINEAR in the 0/1 edge variables.
Given a rank-30 object, take N = its exact kernel and solve, with scipy's MILP (HiGHS):
    maximise  the number of star pairs p (labels sharing a star letter) with Gamma_p != Gamma_{h(p)}
    subject to (C1) exact star counts, (C1') partial caps, Gamma N = (3I - K) N,
and (C2) (common-neighbour caps) added lazily as cuts until the optimum satisfies it.  Every feasible point is an
admissible four-star structure of nullity >= 14; the optimum value 0 means: every admissible structure whose kernel
contains N has h-related star matchings (M_1 = h(M_0), M_3 = h(M_2)).  Also reported: the full h-asymmetry and PSD
of the optimum.  MODE=hfull maximises the full h-asymmetry (all pairs) instead.
usage: python kernel_milp.py <bundle json> <object index> [time limit s]"""
import itertools
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

from stars_rank import kval, count_needed, LABELS
from cls_decomp import nullspace_int

bundle, k = sys.argv[1], int(sys.argv[2])
tlim = float(sys.argv[3]) if len(sys.argv) > 3 else 600
d = json.load(open(bundle))
S = [frozenset(l) for l in d["labels"]]
n = len(S)
idx = {s: i for i, s in enumerate(S)}
st = d["structures"][k] if "structures" in d else d
E0 = {tuple(sorted(e)) for e in st["edges"]}
K8 = [[int(round(8 * kval(a, b))) for b in S] for a in S]
G0 = [[1 if tuple(sorted((a, b))) in E0 else 0 for b in range(n)] for a in range(n)]
M = [[(24 if a == b else 0) - 8 * G0[a][b] - K8[a][b] for b in range(n)] for a in range(n)]
N = nullspace_int(M)
print("object %d of %s: c = %s, kernel dimension %d" % (k, bundle, st.get("c"), len(N)), flush=True)
pairs = list(itertools.combinations(range(n), 2))
pid = {p: t for t, p in enumerate(pairs)}
P = len(pairs)
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
mode = os.environ.get("MODE", "match")
if mode == "hfull":
    sp = [p for p in pairs]
else:
    sp = [p for p in pairs if S[p[0]] & S[p[1]] & {0, 1, 2, 3}]
# keep one representative of each {p, h(p)} orbit with p != h(p)
orb = []
seen = set()
for (i, j) in sp:
    q = tuple(sorted((hp[i], hp[j])))
    if (i, j) in seen or q == (i, j):
        continue
    seen.add((i, j))
    seen.add(q)
    orb.append(((i, j), q))
D = len(orb)
nv = P + D
rows, lo, hi = [], [], []


def add(coeffs, l, u):
    rows.append(coeffs)
    lo.append(l)
    hi.append(u)


def e(i, j):
    return pid[(min(i, j), max(i, j))]


# (C1) exact counts towards the stars, (C1') caps towards the other letters
for i in range(n):
    for y in range(14):
        lits = [e(i, t) for t in range(n) if t != i and y in S[t]]
        if not lits:
            continue
        c = count_needed(S[i], y)
        if y in (0, 1, 2, 3):
            add({v: 1 for v in lits}, c, c)
        else:
            add({v: 1 for v in lits}, 0, c)
# kernel: 8 Gamma n = 8 (3I - K) n  (integer equations)
for vec in N:
    for i in range(n):
        rhs = sum((24 if i == j else 0) * vec[j] - K8[i][j] * vec[j] for j in range(n))
        co = {}
        for j in range(n):
            if j != i and vec[j]:
                co[e(i, j)] = co.get(e(i, j), 0) + 8 * vec[j]
        if not co:
            if rhs != 0:
                print("kernel equation impossible at label", i)
            continue
        add(co, rhs, rhs)
# d_t <= x_p + x_q, d_t <= 2 - x_p - x_q
for t, (p, q) in enumerate(orb):
    add({P + t: 1, pid[p]: -1, pid[q]: -1}, -np.inf, 0)
    add({P + t: 1, pid[p]: 1, pid[q]: 1}, -np.inf, 2)
KC = 3 * np.eye(n) - np.array([[kval(a, b) for b in S] for a in S])
GROUP = [list(range(n))]
if os.environ.get("PSDCUTS") and st.get("gens"):
    gl = []
    for cyc in st["gens"].split("|"):
        mp = {i: i for i in range(14)}
        for cc in cyc.split(";"):
            cc = [int(t) for t in cc.split(",")]
            for q in range(len(cc)):
                mp[cc[q]] = cc[(q + 1) % len(cc)]
        gl.append([idx[frozenset(mp[y] for y in S[i])] for i in range(n)])
    frontier = [list(range(n))]
    seenp = {tuple(range(n))}
    while frontier:
        nxt = []
        for g in frontier:
            for h_ in gl:
                gh = [h_[g[i]] for i in range(n)]
                if tuple(gh) not in seenp:
                    seenp.add(tuple(gh))
                    nxt.append(gh)
        frontier = nxt
    GROUP = [list(g) for g in seenp]
    print("cut symmetrisation group of order %d (gens %s)" % (len(GROUP), st["gens"]), flush=True)
cuts = 0
t0 = time.time()
while True:
    A = lil_matrix((len(rows), nv))
    for r, co in enumerate(rows):
        for v, c in co.items():
            A[r, v] = c
    cvec = np.zeros(nv)
    cvec[P:] = -1.0
    res = milp(cvec, constraints=LinearConstraint(A.tocsr(), np.array(lo, dtype=float), np.array(hi, dtype=float)),
               integrality=np.ones(nv), bounds=Bounds(0, 1),
               options={"time_limit": max(10.0, tlim - (time.time() - t0)), "disp": False})
    if res.x is None:
        print("MILP status %d (%s): no feasible structure (cuts %d, %.0f s)" % (res.status, res.message, cuts,
                                                                              time.time() - t0), flush=True)
        break
    x = np.rint(res.x[:P]).astype(int)
    G = np.zeros((n, n), dtype=int)
    for (i, j), t in pid.items():
        if x[t]:
            G[i, j] = G[j, i] = 1
    # (C2) check, add cuts for violations
    viol = 0
    for i, j in pairs:
        s_ = len(S[i] & S[j])
        com = [t for t in range(n) if t != i and t != j and G[i, t] and G[j, t]]
        cap = (1 - s_) if G[i, j] else (2 - s_)
        if len(com) > cap:
            viol += 1
            if G[i, j]:
                Cp = com[:max(0, 1 - s_) + 1] if 1 - s_ >= 0 else []
                # forbid: adjacent and all of Cp common
                co = {e(i, j): 1}
                for t in Cp:
                    co[e(i, t)] = co.get(e(i, t), 0) + 1
                    co[e(j, t)] = co.get(e(j, t), 0) + 1
                add(co, -np.inf, 2 * len(Cp))
            else:
                Cp = com[:(2 - s_) + 1]
                co = {}
                for t in Cp:
                    co[e(i, t)] = co.get(e(i, t), 0) + 1
                    co[e(j, t)] = co.get(e(j, t), 0) + 1
                co[e(i, j)] = co.get(e(i, j), 0) - 1      # only when non-adjacent
                add(co, -np.inf, 2 * len(Cp) - 1)
            cuts += 1
    obj = int(round(-res.fun))
    if viol == 0:
        hasym = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
        T = 3 * np.eye(n) - G - np.array([[kval(a, b) for b in S] for a in S])
        nul = int(np.sum(np.abs(np.linalg.eigvalsh(T)) < 1e-8))
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
        lt = float(np.linalg.eigvalsh(Pp @ T @ Pp + 50 * (np.eye(n) - Pp))[0])
        lu = float(np.linalg.eigvalsh(Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp))[0])
        same = all(G[i, j] == G0[i][j] for i, j in pairs)
        if os.environ.get("PSDCUTS") and obj > 0 and min(lt, lu) <= -1e-9:
            # PSD cutting planes (as psd_cuts.py): c^T T c >= 0 and c^T U c >= 0 are linear in the edge variables
            npc = 0
            for Mat, sign in ((Pp @ T @ Pp + 50 * (np.eye(n) - Pp), 1), (Pp @ (7 * PiS - T) @ Pp + 50 * (np.eye(n) - Pp), -1)):
                w, V = np.linalg.eigh(Mat)
                for q in range(n):
                    if w[q] > -1e-9:
                        break
                    for gperm in GROUP:
                      c = V[gperm, q]          # symmetrised cut: the problem is invariant under the object's group
                      co = {}
                      for (i, j), t in pid.items():
                          if abs(c[i] * c[j]) > 1e-12:
                              co[t] = 2 * c[i] * c[j]
                      base = float(c @ KC @ c)
                      if sign == 1:      # sum 2 c_i c_j x_ij <= c^T (3I - K) c
                          add(co, -np.inf, base + 1e-7)
                      else:              # sum 2 c_i c_j x_ij >= c^T (3I - K - 7 Pi) c
                          add(co, base - 7 * float(c @ PiS @ c) - 1e-7, np.inf)
                      npc += 1
            psdcuts = getattr(sys.modules[__name__], "psdcuts", 0) + npc
            sys.modules[__name__].psdcuts = psdcuts
            print("  PSD cuts: +%d (total %d), current optimum %d, lambda_T %.4f, lambda_U %.4f, %.0f s"
                  % (npc, psdcuts, obj, lt, lu, time.time() - t0), flush=True)
            if time.time() - t0 > tlim:
                print("time limit during PSD cuts", flush=True)
                break
            continue
        print("OPTIMUM (status %d): %s asymmetry %d (orbit pairs), full h-asymmetry %d, numerical nullity %d, "
              "lambda_T %.4f, lambda_U %.4f, identical to the start: %s, cuts %d, %.0f s"
              % (res.status, mode, obj, hasym, nul, lt, lu, same, cuts, time.time() - t0), flush=True)
        if obj > 0:
            out = "kmilp_obj%d_%s.json" % (k, mode)
            json.dump({"labels": d["labels"], "edges": [[i, j] for i, j in pairs if G[i, j]], "masym_orbits": obj,
                       "hasym": hasym, "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul}, open(out, "w"))
            print("saved", out, flush=True)
        break
    if time.time() - t0 > tlim:
        print("time limit with (C2) violations remaining (%d cuts)" % cuts, flush=True)
        break
