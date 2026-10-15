"""Four-star structures under a symmetry GROUP (several commuting involutions), towards H4' (14/10/2026).

H4' (open): no admissible four-star structure (lines l = {v,0,1}, m = {v,2,3}) with c(l) = c(m) = 1 is PSD (T and U)
with rank T <= 30 (nullity >= 14: four stars plus ten mixed relations).  Allowed symmetries (P5): no group element may
fix 0, 1, 2 (or 0, 1, 3, or 2, 3, 0, or 2, 3, 1) pointwise while moving a letter.  Generators are given as cycle strings
separated by '|', e.g. "0,1;4,5;6,7;8,9;10,11;12,13|2,3;4,6;5,7;8,10;9,11;12,13".
Modes: mix3 (15/10: target three mixed relations under T, U >= 0, saves _MIX3_k.json), lowrank (maximise -(sum of the 14 smallest |eigenvalues| of T), positivity ignored: can ten mixed relations
occur at all?), zero (maximise min(-(14th smallest |eigenvalue|), lambda_min T, lambda_min U)), psd.
Every structure with c(l) = c(m) = 1 has its numerical nullity recorded; record-breaking ones are re-checked exactly.
usage: python sym4g.py <generators> <moves> <seed> <out prefix> [lowrank|zero|psd]
"""
import itertools
import os
import json
import math
import random
import sys
import time

import numpy as np
from pycryptosat import Solver

from stars_rank import build, kval, LABELS
from z5_enum import exact_rank
from disc_scan import sym_pivot_det, small_odd_primes


def parse(cyc):
    h = {i: i for i in range(14)}
    for c in cyc.split(";"):
        c = [int(t) for t in c.split(",")]
        for k in range(len(c)):
            h[c[k]] = c[(k + 1) % len(c)]
    assert all(h[i ^ 1] == h[i] ^ 1 for i in range(14)), "must preserve mates"
    assert set(h[i] for i in range(4)) == {0, 1, 2, 3}
    return h


def main():
    gens_s, moves, seed, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    mode = sys.argv[5] if len(sys.argv) > 5 else "lowrank"
    anyc = len(sys.argv) > 6 and sys.argv[6] in ("anyc", "cl1", "cl2")   # H4 test: P5 not enforced
    cl1 = len(sys.argv) > 6 and sys.argv[6] == "cl1"               # (A4) test: require c(l) = 1 only
    cl2 = len(sys.argv) > 6 and sys.argv[6] == "cl2"               # require c(l) <= 2 only
    gens = [parse(c) for c in gens_s.split("|")]
    # close the group and check the P5 condition
    group = [tuple(range(14))]
    frontier = list(group)
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                gh = tuple(h[g[i]] for i in range(14))
                if gh not in group:
                    group.append(gh)
                    new.append(gh)
        frontier = new
    for g in group:
        moves_letter = any(g[i] != i for i in range(14))
        for fixed in ((0, 1, 2), (0, 1, 3), (2, 3, 0), (2, 3, 1)):
            assert anyc or not (moves_letter and all(g[i] == i for i in fixed)), "group element violates P5: %s" % (g,)
    print("group of order %d" % len(group), flush=True)
    rng = random.Random(seed)
    stars = [0, 1, 2, 3]
    S, idx, e, F = build(stars, rng)
    n = len(S)
    sol = Solver(options={"polar": "rnd", "seed": str(seed)})
    for c in F.clauses:
        sol.add_clause(c)
    gl = [{i: idx[frozenset(h[y] for y in S[i])] for i in range(n)} for h in gens]
    reps, seen = [], set()
    for i, j in itertools.combinations(range(n), 2):
        orb = {(i, j)}
        stack = [(i, j)]
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
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    Xl = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    Xm = [i for i in range(n) if 2 in S[i] or 3 in S[i]]
    oddv_m = [(idx[frozenset((2, y))], idx[frozenset((3, y))]) for y in range(4, 14)]   # f_y, mode odd9
    oddv_l = [(idx[frozenset((0, y))], idx[frozenset((1, y))]) for y in range(4, 14)]   # e_y
    Q9 = np.linalg.qr(np.eye(10) - np.ones((10, 10)) / 10.0)[0][:, :9]   # orthonormal basis of 1^perp in R^10
    D = np.zeros((14, 84))
    for j, l in enumerate(LABELS):
        for y in l:
            D[y, j] = 1
    Pi = np.eye(84) - D.T @ np.linalg.inv(D @ D.T) @ D
    pos = {l: i for i, l in enumerate(LABELS)}
    ix = [pos[l] for l in S]
    PiS = Pi[np.ix_(ix, ix)]
    Z = np.array([[1.0 if y in l else 0.0 for l in S] for y in stars]).T
    Qz, _ = np.linalg.qr(Z)
    Pp = np.eye(n) - Qz @ Qz.T

    def perp_min(M):
        ev, V = np.linalg.eigh(Pp @ M @ Pp)
        keep = [k for k in range(n) if np.linalg.norm(Qz.T @ V[:, k]) < 1e-6]
        return float(ev[keep].min()) if keep else 0.0

    # character sectors (gens = one or two commuting involutions): basis vectors sum_g chi(g) e_{g(alpha)}
    sectors = []
    if len(gl) in (1, 2) and all(all(m[m[i]] == i for i in range(n)) for m in gl):
        signs = [(1,), (-1,)] if len(gl) == 1 else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        elems = [((), lambda i: i)]
        if len(gl) == 1:
            elems = [((0,), lambda i: i), ((1,), lambda i, m=gl[0]: m[i])]
        else:
            elems = [((0, 0), lambda i: i), ((1, 0), lambda i, m=gl[0]: m[i]),
                     ((0, 1), lambda i, m=gl[1]: m[i]), ((1, 1), lambda i, a=gl[0], b=gl[1]: a[b[i]])]
        for sg in signs:
            vecs, seen_o = [], set()
            for i in range(n):
                orb = frozenset(f(i) for _, f in elems)
                if orb in seen_o:
                    continue
                seen_o.add(orb)
                v = np.zeros(n)
                for ex, f in elems:
                    v[f(i)] += np.prod([sg[k] ** ex[k] for k in range(len(sg))])
                if np.linalg.norm(v) > 1e-9:
                    vecs.append(v / np.linalg.norm(v))
            B = np.array(vecs).T if vecs else np.zeros((n, 0))
            sectors.append((sg, B))

    def sector_defect(T, cap_triv):
        """greedy minimal sum of 14 smallest |eigenvalues| with at most cap_triv taken in the trivial sector"""
        pool = []
        for k, (sg, B) in enumerate(sectors):
            if B.shape[1] == 0:
                continue
            ev = np.sort(np.abs(np.linalg.eigvalsh(B.T @ T @ B)))
            pool += [(x, k) for x in ev]
        pool.sort()
        taken, tot, cnt = {}, 0.0, 0
        for x, k in pool:
            cap = cap_triv if k == 0 else 99
            if taken.get(k, 0) >= cap:
                continue
            taken[k] = taken.get(k, 0) + 1
            tot += x
            cnt += 1
            if cnt == 14:
                break
        return tot

    def sector_nullities(M8):
        out = []
        for sg, B in sectors:
            if B.shape[1] == 0:
                out.append(0)
                continue
            Bi = np.rint(B * np.sqrt(np.sum(np.abs(B) > 1e-9, axis=0))).astype(np.int64)   # integer basis
            blk = (Bi.T @ M8 @ Bi).tolist()
            out.append(len(blk) - exact_rank(blk))
        return out

    tmax = int(os.environ["TMAX"]) if os.environ.get("TMAX") else None
    # FORCE_SPLIT_L / FORCE_SPLIT_M: groups of letters separated by '/', e.g. "4,5,6,7/8,9,10,11/12,13,2,3": the base graph
    # of l (resp. m) has no edge between labels whose outer letters lie in different groups (closed configurations)
    for env_name, centre in (("FORCE_SPLIT_L", (0, 1)), ("FORCE_SPLIT_M", (2, 3))):
        if os.environ.get(env_name):
            groups = [set(int(t) for t in g.split(",")) for g in os.environ[env_name].split("/")]
            gof = {x: k for k, g in enumerate(groups) for x in g}
            cs = set(centre)
            for i in range(n):
                for j in range(i + 1, n):
                    if not (S[i] & cs) or not (S[j] & cs):
                        continue
                    xi = [y for y in S[i] if y not in cs]
                    xj = [y for y in S[j] if y not in cs]
                    if len(xi) == 1 and len(xj) == 1 and gof.get(xi[0]) != gof.get(xj[0]):
                        sol.add_clause([-e[(i, j)]])
    # FORCE_GRID_L / FORCE_GRID_M: even letters x (pair {x, x+1}) such that l (resp. m) spans a 3x3 grid with the line
    # {v, x, x+1}: the closed square z_ax ~ z_ax', z_a'x ~ z_a'x', z_ax ~ z_a'x, z_ax' ~ z_a'x' is imposed (straight grid)
    for env_name, (a0, a1) in (("FORCE_GRID_L", (0, 1)), ("FORCE_GRID_M", (2, 3))):
        if os.environ.get(env_name):
            for x in [int(t) for t in os.environ[env_name].split(",")]:
                y = x ^ 1
                for (p, q) in (((a0, x), (a0, y)), ((a1, x), (a1, y)), ((a0, x), (a1, x)), ((a0, y), (a1, y))):
                    sol.add_clause([e[(idx[frozenset(p)], idx[frozenset(q)])]])
    # FORCE_TL / FORCE_TM: letters x at which the transversal of l (z_0x ~ z_1x) / of m (z_2x ~ z_3x) is imposed
    for env_name, (a0, a1) in (("FORCE_TL", (0, 1)), ("FORCE_TM", (2, 3))):
        if os.environ.get(env_name):
            for x in [int(t) for t in os.environ[env_name].split(",")]:
                sol.add_clause([e[(idx[frozenset((a0, x))], idx[frozenset((a1, x))])]])
    trans_l = [(idx[frozenset((0, x))], idx[frozenset((1, x))]) for x in range(2, 14)]
    trans_m = [(idx[frozenset((2, x))], idx[frozenset((3, x))]) for x in list(range(0, 2)) + list(range(4, 14))]
    # FIXSUB=<json> [FIXIDX=k] (15/10, (B') completion test): fix the induced graph on the labels of a smaller
    # structure (e.g. a three-star (A) counterexample, labels X_l u L_2) and let the walk choose the remaining edges
    if os.environ.get("FIXSUB"):
        dsub = json.load(open(os.environ["FIXSUB"]))
        if "structures" in dsub:
            esub = dsub["structures"][int(os.environ.get("FIXIDX", "0"))]["edges"]
        else:
            esub = dsub["edges"]
        lsub = [frozenset(l) for l in dsub["labels"]]
        eset = {frozenset((lsub[i], lsub[j])) for i, j in esub}
        inside = [i for i in range(n) if S[i] in set(lsub)]
        nfix = 0
        for i, j in itertools.combinations(inside, 2):
            lit = e[(i, j)]
            sol.add_clause([lit] if frozenset((S[i], S[j])) in eset else [-lit])
            nfix += 1
        print("FIXSUB %s: %d labels fixed, %d pairs fixed, %d edges" % (os.environ["FIXSUB"], len(inside), nfix, len(eset)),
              flush=True)
    init = os.environ.get("INIT")            # warm start from a saved structure (same labels and group)
    if init:
        di = json.load(open(init))
        assert [sorted(l) for l in S] == di["labels"], "label order differs"
        eset = {tuple(x) for x in di["edges"]}
        assum0 = [e[(i, j)] if (i, j) in eset else -e[(i, j)] for i, j in itertools.combinations(range(n), 2)]
        if os.environ.get("NOSQUARE"):
            # 15/10 audit: forbid the closed square on (l, m) (no grid on the two lines); warm start near INIT by
            # freeing every pair that touches the four cross labels {0,2}, {0,3}, {1,2}, {1,3}
            cross = {idx[frozenset(p)] for p in ((0, 2), (0, 3), (1, 2), (1, 3))}
            sqp = [(idx[frozenset((0, 2))], idx[frozenset((0, 3))]), (idx[frozenset((0, 2))], idx[frozenset((1, 2))]),
                   (idx[frozenset((0, 3))], idx[frozenset((1, 3))]), (idx[frozenset((1, 2))], idx[frozenset((1, 3))])]
            sol.add_clause([-e[p] for p in sqp])
            assum0 = [e[(i, j)] if (i, j) in eset else -e[(i, j)] for i, j in itertools.combinations(range(n), 2)
                      if i not in cross and j not in cross]
        ok, model = sol.solve(assum0)
        if not ok and os.environ.get("NOSQUARE"):
            # keep a shrinking random part of the fixed pairs until the no-square structure exists
            for frac in (0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0):
                part = [x for x in assum0 if rng.random() < frac]
                ok, model = sol.solve(part)
                if ok:
                    print("warm start (no square): kept %.0f%% of the fixed pairs" % (100 * frac), flush=True)
                    break
        print("warm start from %s: %s" % (init, ok), flush=True)
    else:
        ok, model = sol.solve()
    if not ok:
        print("no invariant admissible structure", flush=True)
        return
    t0 = time.time()
    hist, npsd = {}, 0
    best_psd = None
    best_near = None
    best_null = -1
    cur, temp = None, float(os.environ.get("TEMP0", "0.3"))
    maxsec = float(os.environ.get("MAXSEC", "1e12"))   # self-termination (Git Bash timeout does not kill python.exe)
    for mv in range(moves):
        if time.time() - t0 > maxsec:
            print("time limit reached (%.0f s)" % (time.time() - t0), flush=True)
            break
        Rl = set(rng.sample(range(n), int(os.environ.get("NFREE", "4"))))   # NFREE (15/10): labels freed per move
        bad = set(Rl)
        for m in gl:
            bad |= {m[i] for i in Rl}
        assum = []
        for key in reps:
            i, j = key
            if i in bad or j in bad:
                continue
            v = e[key]
            assum.append(v if model[v] else -v)
        if mv == 0 and init:
            ok2, m2 = True, model                 # evaluate the warm-start structure itself first
        else:
            ok2, m2 = sol.solve(assum)
        if not ok2:
            continue
        G = np.zeros((n, n), dtype=np.int64)
        for (i, j), v in e.items():
            if i < j and m2[v]:
                G[i, j] = G[j, i] = 1
        M8 = 24 * np.eye(n, dtype=np.int64) - 8 * G - K8
        T = M8 / 8.0
        ev = np.linalg.eigvalsh(T)
        absev = np.sort(np.abs(ev))
        nul_num = int(np.sum(absev < 1e-8))
        cl = 23 - exact_rank([[int(M8[i][j]) for j in Xl] for i in Xl])
        cm = 23 - exact_rank([[int(M8[i][j]) for j in Xm] for i in Xm])
        both = (cl == 1) if cl1 else ((cl <= 2) if cl2 else ((cl == 1 and cm == 1) or anyc))
        tl = sum(1 for (i0, i1) in trans_l if G[i0, i1])
        tm = sum(1 for (i0, i1) in trans_m if G[i0, i1])
        if tmax is not None and max(tl, tm) > tmax:
            both = False
        lt = perp_min(T)
        lu = perp_min(7 * PiS - T)
        # SAVE30=N (15/10): harvest the first N distinct PSD structures of numerical nullity >= 14 (rank <= 30), any mode
        if (os.environ.get("SAVE30") and min(lt, lu) > -1e-9 and nul_num >= 14) or (os.environ.get("SAVE30ANY") and nul_num >= 14):
            h30 = getattr(main, "h30", None)
            if h30 is None:
                h30 = main.h30 = set()
            key30 = hash(G[np.triu_indices(n, 1)].tobytes())
            if key30 not in h30 and len(h30) < int(os.environ.get("SAVE30") or os.environ.get("SAVE30ANY")):
                h30.add(key30)
                json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt, "lambda_U": lu,
                           "nullity_numeric": nul_num,
                           "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                          open(out + "_H30_%d.json" % len(h30), "w"))
        if min(lt, lu) > -1e-9:
            npsd += 1
            # 15/10: saving every PSD visit filled the folder with 460 000 files; save only the first SAVEPSD (default 20)
            if npsd <= int(os.environ.get("SAVEPSD", "20")):
                json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt, "lambda_U": lu,
                           "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                          open(out + "_PSD_%d.json" % npsd, "w"))
            print("move %d: T AND U PSD (c(l)=%d, c(m)=%d), lambda_T %.4f, lambda_U %.4f, numerical nullity %d, t = (%d,%d)"
                  % (mv, cl, cm, lt, lu, nul_num, tl, tm), flush=True)
        if both and (best_psd is None or min(lt, lu) > best_psd):
            best_psd = min(lt, lu)
            json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt, "lambda_U": lu,
                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                      open(out + "_bestpsd.json", "w"))
        if both:
            hist[nul_num] = hist.get(nul_num, 0) + 1
            if nul_num > best_null:
                rex = exact_rank(M8.tolist())
                best_null = n - rex
                json.dump({"labels": [sorted(l) for l in S], "gens": gens_s,
                           "best": {"move": mv, "nullity": best_null, "lambda_T": lt, "lambda_U": lu,
                                    "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]}},
                          open(out + "_best.json", "w"))
                print("move %d: c(l)=c(m)=1, new best EXACT nullity %d (lambda_T %.4f, lambda_U %.4f)"
                      % (mv, best_null, lt, lu), flush=True)
                if best_null >= 14 and min(lt, lu) > -1e-9 and mode not in ("mix3", "r7", "schur", "oddgap", "disc", "odd9", "b1", "b1x"):
                    print("H4' REFUTED (if exact positivity confirmed)", flush=True)
                    return
        if mode in ("sector", "urepair"):
            capt = 5 + min(cl, cm)
            if mode == "urepair" and both and nul_num >= 14 and lt > -1e-9:
                s2 = lu                                   # stay on the plateau nullity >= 14, T >= 0; push U up
            else:
                s2 = min(-sector_defect(T, capt), lt, lu) if both else -99.0
                if mode == "urepair":
                    s2 -= 1.0
            if nul_num >= 13 and min(lt, lu) > -0.05:
                print("move %d: near target: numerical nullity %d, sector nullities %s, lambda_T %.4f, lambda_U %.4f, c = (%d,%d), t = (%d,%d)"
                      % (mv, nul_num, sector_nullities(M8), lt, lu, cl, cm, tl, tm), flush=True)
                key = (nul_num, min(lt, lu))
                if best_near is None or key > best_near:
                    best_near = key
                    json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt,
                               "lambda_U": lu, "nullity_numeric": nul_num,
                               "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                              open(out + "_near.json", "w"))
        elif mode == "mix3":
            # MIX test (15/10): mixed = nullity - (2 + c(l) + c(m) - [grid(l,m)]); push the nullity needed for
            # three mixed relations to zero while keeping T, U PSD; save every PSD structure with mixed >= 3
            c4 = [idx[frozenset(p)] for p in ((0, 2), (0, 3), (1, 2), (1, 3))]
            gr = int(G[c4[0], c4[1]] and G[c4[2], c4[3]] and G[c4[0], c4[2]] and G[c4[1], c4[3]])
            target = 2 + int(os.environ.get("MIXT", "3")) + cl + cm - gr   # MIXT = mixed relations aimed at
            if os.environ.get("NULT"):
                target = int(os.environ["NULT"])                          # NULT = absolute nullity aimed at
            if not (both and target <= n):
                s2 = -99.0
            elif min(lt, lu) > -1e-9:
                s2 = -float(absev[target - 1])          # on the PSD set: push the target eigenvalue to 0
            else:
                s2 = -1.0 + 3.0 * min(lt, lu)            # off the PSD set: always worse than any PSD structure
            if min(lt, lu) > -1e-9 and nul_num >= target:
                nmix = getattr(main, "nmix", 0) + 1
                main.nmix = nmix
                if nmix <= int(os.environ.get("SAVEPSD", "20")):
                  json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "grid_lm": gr,
                           "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                           "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                          open(out + "_MIX3_%d.json" % nmix, "w"))
                print("move %d: PSD WITH >= MIXT MIXED RELATIONS (numerical): nullity %d, c = (%d,%d), grid %d"
                      % (mv, nul_num, cl, cm, gr), flush=True)
        elif mode == "oddgap":
            # ODD-h test (15/10): one generator h; on the PSD set push the THIRD smallest eigenvalue of the h-odd sector
            # of T to 0 (two zeros = the star differences); save PSD structures with odd nullity >= 3
            if min(lt, lu) > -1e-9:
                Bo = [B for sg, B in sectors if sg == (-1,)][0]
                evo = np.sort(np.linalg.eigvalsh(Bo.T @ T @ Bo))
                g3 = float(evo[2])
                s2 = -g3
                bestg = getattr(main, "bestg", 99.0)
                if g3 < bestg - 1e-6:
                    main.bestg = g3
                    print("move %d: PSD, third odd eigenvalue %.5f (new minimum), nullity %d, c = (%d,%d)"
                          % (mv, g3, nul_num, cl, cm), flush=True)
                    if g3 < 0.01:
                        # 15/10: keep the near-failures of ODD-h for an exact local search (cap 30)
                        kn = getattr(main, "kn", 0) + 1
                        main.kn = kn
                        if kn <= 30:
                            json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "odd_gap": g3,
                                       "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                      open(out + "_NEAR_%d.json" % kn, "w"))
                if g3 < 1e-7:
                    ko = getattr(main, "ko", 0) + 1
                    main.ko = ko
                    json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "odd_gap": g3,
                               "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                               "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                              open(out + "_ODD_%d.json" % ko, "w"))
            else:
                s2 = -100.0 + 3.0 * min(lt, lu)
        elif mode == "schur":
            # SCHUR12 stress test (15/10): on the PSD set, minimise min(rank T_S4 - rank T_Xl, rank T_S4 - rank T_Xm)
            # (Conway needs 7 + c(l) - delta resp. 7 + c(m) - delta); save every PSD structure with value <= 11
            if min(lt, lu) > -1e-9:
                rk = n - nul_num
                sch = min(rk - (23 - cl), rk - (23 - cm))
                s2 = -float(sch) - 0.1 * float(absev[13])
                if os.environ.get("ASYMW"):
                    # drift away from the h-symmetric region (diversity): reward h-asymmetry of the edge set
                    hp = getattr(main, "hperm", None)
                    if hp is None:
                        hm = {0: 1, 1: 0, 2: 3, 3: 2}
                        hp = [idx[frozenset(hm.get(y, y) for y in S[i])] for i in range(n)]
                        main.hperm = hp
                    asym = float(np.abs(G[np.ix_(hp, hp)] - G).sum()) / 2.0
                    s2 += float(os.environ["ASYMW"]) * min(asym, 60.0)
                bests = getattr(main, "bests", 99)
                if sch < bests:
                    main.bests = sch
                    print("move %d: PSD with Schur rank %d (new minimum), rank %d, c = (%d,%d)" % (mv, sch, rk, cl, cm),
                          flush=True)
                if sch <= 11:
                    ks = getattr(main, "ks", 0) + 1
                    main.ks = ks
                    json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "schur": sch,
                               "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                               "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                              open(out + "_SCH_%d.json" % ks, "w"))
            else:
                s2 = -100.0 + 3.0 * min(lt, lu)
        elif mode == "r7":
            # 7-adic stress test (15/10): on the PSD set, minimise rank_7(8T_S4) (Conway needs <= k <= 28, L4/L22/L23);
            # tie-break by pushing the 14th smallest |eigenvalue| down; save every PSD structure with rank_7 <= 29
            if min(lt, lu) > -1e-9 or os.environ.get("R7NOPSD"):
                A7 = M8 % 7
                r7 = 0
                for c in range(n):
                    piv = np.nonzero(A7[r7:, c])[0]
                    if len(piv) == 0:
                        continue
                    q = r7 + piv[0]
                    A7[[r7, q]] = A7[[q, r7]]
                    A7[r7] = (A7[r7] * pow(int(A7[r7, c]), 5, 7)) % 7
                    colv = A7[:, c].copy()
                    colv[r7] = 0
                    A7 = (A7 - np.outer(colv, A7[r7])) % 7
                    r7 += 1
                    if r7 == n:
                        break
                s2 = -float(r7) - 0.1 * float(absev[13])
                # R7RANKW (15/10, K22 question): penalty per missing relation below nullity 14 (a Conway four-star block
                # has rank <= 30); rank-30 PSD records are tracked separately
                rkw = float(os.environ.get("R7RANKW", "0"))
                if rkw > 0:
                    s2 -= rkw * max(0, 14 - nul_num)
                    if min(lt, lu) > -1e-9 and nul_num >= 14:
                        b30 = getattr(main, "best7r30", 99)
                        if r7 < b30:
                            main.best7r30 = r7
                            k30 = getattr(main, "k30", 0) + 1
                            main.k30 = k30
                            json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "rank7": r7,
                                       "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                      open(out + "_R30_%d.json" % k30, "w"))
                            print("move %d: RANK-30 PSD with rank_7 = %d (new record, saved %s_R30_%d.json), c = (%d,%d)"
                                  % (mv, r7, out, k30, cl, cm), flush=True)
                best7 = getattr(main, "best7", 99)
                if r7 < best7:
                    main.best7 = r7
                    print("move %d: %s with rank_7 = %d (new minimum), numerical nullity %d, c = (%d,%d), lambda %.3f"
                          % (mv, "PSD" if min(lt, lu) > -1e-9 else "non-PSD", r7, nul_num, cl, cm, min(lt, lu)), flush=True)
                if r7 <= 29 and min(lt, lu) > -1e-9:
                    k7 = getattr(main, "k7", 0) + 1
                    main.k7 = k7
                    # 15/10: cap the files (SAVEPSD first ones, every new PSD minimum, at most 200 with rank_7 <= 28)
                    b7p = getattr(main, "best7psd", 99)
                    n28 = getattr(main, "n28", 0) + (1 if r7 <= 28 else 0)
                    main.n28 = n28
                    if k7 <= int(os.environ.get("SAVEPSD", "20")) or r7 < b7p or (r7 <= 28 and n28 <= 200):
                        json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "rank7": r7,
                                   "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                                   "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                  open(out + "_R7_%d.json" % k7, "w"))
                    if r7 < b7p:
                        main.best7psd = r7
                        print("move %d: PSD with rank_7 = %d (new PSD minimum, saved as %s_R7_%d.json), c = (%d,%d)"
                              % (mv, r7, out, k7, cl, cm), flush=True)
            else:
                s2 = -100.0 + 3.0 * min(lt, lu)
        elif mode == "disc":
            # DISC-targeted walk (15/10): on PSD structures of rank 30, Conway needs det(8T_I) = 2 x square
            # (I a basis of the 44 labels; L17 with LAB's det K, Codex L2) and rank_7(8T_S4) <= 28 (L4, L22).
            # score = -(primes < 20000 with the wrong exponent parity) - (cofactor not a square) - excess of rank_7
            if min(lt, lu) > -1e-9 and nul_num >= 14:
                rex, dex, _ = sym_pivot_det(M8.tolist())
                if rex is None:
                    s2 = -60.0
                elif rex < 30:
                    s2 = 0.0
                    print("move %d: PSD with EXACT rank %d < 30 (c = (%d,%d))" % (mv, rex, cl, cm), flush=True)
                else:
                    oddp, cof = small_odd_primes(int(dex))
                    A7 = [[int(x) % 7 for x in row] for row in M8.tolist()]
                    r7 = 0
                    for c in range(n):
                        pv = next((i for i in range(r7, n) if A7[i][c]), None)
                        if pv is None:
                            continue
                        A7[r7], A7[pv] = A7[pv], A7[r7]
                        iv = pow(A7[r7][c], 5, 7)
                        A7[r7] = [(x * iv) % 7 for x in A7[r7]]
                        for i in range(n):
                            if i != r7 and A7[i][c]:
                                f7 = A7[i][c]
                                A7[i] = [(x - f7 * y) % 7 for x, y in zip(A7[i], A7[r7])]
                        r7 += 1
                    wrong = len(set(oddp) ^ {2}) + (0 if math.isqrt(cof) ** 2 == cof else 1) + max(0, r7 - 28)
                    s2 = -float(wrong)
                    bw = getattr(main, "bestwrong", 99)
                    if wrong < bw:
                        main.bestwrong = wrong
                        print("move %d: rank-30 PSD, DISC defect %d (odd primes %s, cofactor %s, rank_7 %d), c = (%d,%d)"
                              % (mv, wrong, oddp, "1" if cof == 1 else "big", r7, cl, cm), flush=True)
                    if wrong == 0:
                        kd = getattr(main, "kd", 0) + 1
                        main.kd = kd
                        if kd <= 200:
                            json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "rank7": r7,
                                       "det8T_I_odd_primes": oddp, "lambda_T": lt, "lambda_U": lu,
                                       "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                      open(out + "_DISC_%d.json" % kd, "w"))
                        if kd <= 5:
                            print("move %d: DISC AND rank_7 PASS (saved %s_DISC_%d.json)" % (mv, out, kd), flush=True)
            elif min(lt, lu) > -1e-9:
                # rank > 30: penalty DISCRANKW per missing relation (env, default 1.0; 15/10: 10 per relation froze the
                # walk on two isolated rank-30 structures)
                s2 = -4.0 - float(os.environ.get("DISCRANKW", "1.0")) * float(14 - nul_num)
            else:
                s2 = -100.0 + 3.0 * min(lt, lu)
        elif mode == "odd9":
            # ODD9 stress test (15/10): push the m-odd vectors f_y (y outer) towards an extra relation beyond X_l (and the
            # l-odd ones beyond X_m).  Gram of V2 = X_l + span(f_y) (34 x 34): it has >= c(l) + 2 zero eigenvalues
            # (ker T_X and the star difference); score = -(the next smallest |eigenvalue|), min over both lines.
            # ODD9PSD=1: only T, U >= 0 structures count.
            if os.environ.get("ODD9PSD") and min(lt, lu) <= -1e-9:
                s2 = -100.0 + 3.0 * min(lt, lu)
            else:
                gaps = []
                for (Xi, odd_ix, cc) in ((Xl, oddv_m, cl), (Xm, oddv_l, cm)):
                    # Schur complement S_f = G_f - C^T T_X^+ C (T_X >= 0 always, P3; rank 23 - c), S_f 1 = 0;
                    # gap = least |eigenvalue| of S_f on the complement of 1 (0 <=> odd gain 8 < 9)
                    Fm = np.zeros((n, 10))
                    for k2, (p2, q2) in enumerate(odd_ix):
                        Fm[p2, k2] = 1.0
                        Fm[q2, k2] = -1.0
                    TX = T[np.ix_(Xi, Xi)]
                    wX, VX = np.linalg.eigh(TX)
                    keep = wX > 1e-9
                    Cm = (T @ Fm)[Xi, :]
                    W2 = VX[:, keep].T @ Cm
                    Sf = Fm.T @ T @ Fm - W2.T @ (W2 / wX[keep][:, None])
                    evs = np.linalg.eigvalsh(Q9.T @ Sf @ Q9)
                    gaps.append(float(np.min(np.abs(evs))))
                gmin = min(gaps)
                s2 = -gmin
                bg = getattr(main, "bestgap", 99.0)
                if gmin < bg:
                    main.bestgap = gmin
                    if gmin < 0.2 or mv % 50 == 0:
                        print("move %d: odd gap %.5f (l-side %.5f, m-side %.5f), c = (%d,%d), PSD %s"
                              % (mv, gmin, gaps[0], gaps[1], cl, cm, min(lt, lu) > -1e-9), flush=True)
                if gmin < 1e-6:
                    ko = getattr(main, "ko", 0) + 1
                    main.ko = ko
                    if ko <= 50:
                        json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "gaps": gaps,
                                   "lambda_T": lt, "lambda_U": lu,
                                   "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                  open(out + "_ODD9_%d.json" % ko, "w"))
                        print("move %d: ODD9 DEGENERATE CANDIDATE (gap %.2e), saved %s_ODD9_%d.json"
                              % (mv, gmin, out, ko), flush=True)
        elif mode == "b1x":
            # 15/10 loop: targeted (B') search.  A counterexample needs a line with c = 1 whose odd gain drops to 8
            # (odd Schur block S_f singular on 1^perp) AND a complete absorption of the even vectors of the other line
            # (all its outer letters transversals).  Score on PSD structures with a c = 1 line (call it l):
            # -3 (14 - nullity)_+ - 4 (odd gap beyond X_l) + 0.3 (outer transversals of the other line); else -60 / -100.
            if min(lt, lu) > -1e-9 and min(cl, cm) == 1:
                if cl == 1:
                    Xi, odd_ix, other_t = Xl, oddv_m, sum(1 for (i0, i1) in trans_m[2:] if G[i0, i1])
                else:
                    Xi, odd_ix, other_t = Xm, oddv_l, sum(1 for (i0, i1) in trans_l[2:] if G[i0, i1])
                Fm = np.zeros((n, 10))
                for k2, (p2, q2) in enumerate(odd_ix):
                    Fm[p2, k2] = 1.0
                    Fm[q2, k2] = -1.0
                TX = T[np.ix_(Xi, Xi)]
                wX, VX = np.linalg.eigh(TX)
                keep = wX > 1e-9
                W2 = VX[:, keep].T @ (T @ Fm)[Xi, :]
                Sf = Fm.T @ T @ Fm - W2.T @ (W2 / wX[keep][:, None])
                gap = float(np.min(np.abs(np.linalg.eigvalsh(Q9.T @ Sf @ Q9))))
                s2 = -3.0 * max(0, 14 - nul_num) - 4.0 * gap + 0.3 * other_t
                bx = getattr(main, "bestb1x", -999.0)
                if s2 > bx:
                    main.bestb1x = s2
                    print("move %d: c = 1 PSD: nullity %d, odd gap %.5f, outer transversals of the other line %d, score %.3f"
                          % (mv, nul_num, gap, other_t, s2), flush=True)
                if nul_num >= 14:
                    print("move %d: RANK <= 30 PSD WITH A NON-SPECIAL LINE (c = (%d,%d)) [b1x]" % (mv, cl, cm), flush=True)
                    json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt,
                               "lambda_U": lu, "nullity_numeric": nul_num,
                               "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                              open(out + "_B1X_%d.json" % mv, "w"))
            elif min(lt, lu) > -1e-9:
                s2 = -60.0
            else:
                s2 = -100.0 + 3.0 * min(lt, lu)
        elif mode == "b1":
            # (B') test (15/10): a PSD four-star structure of rank <= 30 with a NON-special line (c = 1); in a Conway graph
            # every line is special iff no such structure occurs.  score on PSD: -3 (missing relations below 14)
            # - 2 (min(c) - 1); records and saves (cap 50) every PSD structure with nullity >= 14 and min(c) = 1
            if min(lt, lu) > -1e-9:
                # 15/10 audit options: NULTARGET (default 14; 15 tests (N15)), CPEN (weight of min(c) - 1, default 2),
                # TPEN (weight of min(t(l), t(m)) - 7 when positive, default 0; tests the transversal bridge (T8))
                ntar = int(os.environ.get("NULTARGET", "14"))
                s2 = (-3.0 * max(0, ntar - nul_num) - float(os.environ.get("CPEN", "2.0")) * (min(cl, cm) - 1)
                      - float(os.environ.get("TPEN", "0")) * max(0, min(tl, tm) - 7)
                      - float(os.environ.get("TSUMPEN", "0")) * max(0, tl + tm - 14))
                if os.environ.get("B1KEEP1") and min(cl, cm) != 1:
                    s2 = -60.0          # stay among structures with a non-special line, push the nullity up
                if os.environ.get("HBREAK"):
                    # HBREAK (15/10 morning): all 331 rank-30 objects are invariant under h = (0 1)(2 3); stay among
                    # PSD structures with h BROKEN and push the nullity up (a rank-30 one would test (SQ30) and (H-INV))
                    hp = getattr(main, "hperm", None)
                    if hp is None:
                        hm = {0: 1, 1: 0, 2: 3, 3: 2}
                        hp = [idx[frozenset(hm.get(y, y) for y in S[i])] for i in range(n)]
                        main.hperm = hp
                    hasym = int(np.abs(G[np.ix_(hp, hp)] - G).sum()) // 2
                    if os.environ.get("HMATCH"):
                        # HMATCH: only the four star matchings M_a (pairs of labels sharing a star letter a) count;
                        # (H-MATCH) = M_1 = h(M_0), M_3 = h(M_2) at nullity >= 14 would exclude Conway (Hamming points)
                        sl = getattr(main, "starpairs", None)
                        if sl is None:
                            sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
                            main.starpairs = sl
                        hasym = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
                    if hasym == 0:
                        s2 = s2 - float(os.environ["HPEN"]) if os.environ.get("HPEN") else -60.0
                    else:
                        hb = getattr(main, "hbrec", -1)
                        if nul_num > hb:
                            main.hbrec = nul_num
                            print("move %d: HBREAK RECORD: PSD with h broken (%d asymmetric pairs), nullity %d, c = (%d,%d), "
                                  "t = (%d,%d)" % (mv, hasym, nul_num, cl, cm, tl, tm), flush=True)
                        if nul_num >= 13:
                            kh = getattr(main, "kh", 0) + 1
                            main.kh = kh
                            if kh <= 50:
                                json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "t": [tl, tm],
                                           "hasym": hasym, "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                                           "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                          open(out + "_HB_%d.json" % kh, "w"))
                            if nul_num >= 14:
                                print("move %d: HBREAK TARGET HIT: rank <= 30 PSD with h broken, saved %s_HB_%d.json"
                                      % (mv, out, kh), flush=True)
                bb = getattr(main, "bestb1", -999.0)
                if s2 > bb:
                    main.bestb1 = s2
                    print("move %d: PSD, numerical nullity %d, c = (%d,%d), score %.1f (new best)" % (mv, nul_num, cl, cm, s2),
                          flush=True)
                if nul_num >= 15 or (nul_num >= 14 and min(tl, tm) <= 7):
                    kz = getattr(main, "kz", 0) + 1
                    main.kz = kz
                    if kz <= 50:
                        json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "t": [tl, tm],
                                   "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                                   "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                  open(out + "_AUD_%d.json" % kz, "w"))
                        print("move %d: AUDIT TARGET HIT: PSD, nullity %d, c = (%d,%d), t = (%d,%d), saved %s_AUD_%d.json"
                              % (mv, nul_num, cl, cm, tl, tm, out, kz), flush=True)
                if nul_num >= 14 and min(cl, cm) == 1:
                    kb = getattr(main, "kb", 0) + 1
                    main.kb = kb
                    if kb <= 50:
                        json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "lambda_T": lt,
                                   "lambda_U": lu, "nullity_numeric": nul_num,
                                   "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                  open(out + "_B1_%d.json" % kb, "w"))
                        print("move %d: RANK <= 30 PSD WITH A NON-SPECIAL LINE (c = (%d,%d)), saved %s_B1_%d.json"
                              % (mv, cl, cm, out, kb), flush=True)
            else:
                s2 = -100.0 + 3.0 * min(lt, lu)
        elif mode == "lowrank":
            s2 = -float(absev[:14].sum()) if both else -99.0
        elif mode == "zero":
            s2 = min(-float(absev[13]), lt, lu) if both else -99.0
        else:
            s2 = min(lt, lu) if both else -99.0
        if os.environ.get("HREQ"):
            # HREQ (15/10 morning, any mode): penalise structures whose four star matchings M_0..M_3 are h-related
            # (M_1 = h(M_0), M_3 = h(M_2)); records the numerical nullity of the matching-broken ones, PSD or not
            hp = getattr(main, "hperm", None)
            if hp is None:
                hm = {0: 1, 1: 0, 2: 3, 3: 2}
                hp = [idx[frozenset(hm.get(y, y) for y in S[i])] for i in range(n)]
                main.hperm = hp
            sl = getattr(main, "starpairs", None)
            if sl is None:
                sl = [(i, j) for i in range(n) for j in range(i + 1, n) if S[i] & S[j] & {0, 1, 2, 3}]
                main.starpairs = sl
            masym = sum(1 for (i, j) in sl if G[i, j] != G[hp[i], hp[j]])
            if masym == 0:
                s2 -= float(os.environ["HREQ"])
            else:
                hr = getattr(main, "hreqrec", -1)
                if nul_num > hr:
                    main.hreqrec = nul_num
                    print("move %d: HREQ RECORD: matchings NOT h-related (%d pairs), numerical nullity %d, PSD %s "
                          "(lambda_T %.4f, lambda_U %.4f), c = (%d,%d)" % (mv, masym, nul_num, min(lt, lu) > -1e-9, lt, lu, cl, cm),
                          flush=True)
                if nul_num >= 14:
                    kq = getattr(main, "kq", 0) + 1
                    main.kq = kq
                    if kq <= 50:
                        json.dump({"labels": [sorted(l) for l in S], "gens": gens_s, "c": [cl, cm], "masym": masym,
                                   "lambda_T": lt, "lambda_U": lu, "nullity_numeric": nul_num,
                                   "edges": [[i, j] for i in range(n) for j in range(i + 1, n) if G[i, j]]},
                                  open(out + "_HQ_%d.json" % kq, "w"))
                    if kq <= 3:
                        print("move %d: HREQ TARGET HIT: nullity %d with matchings not h-related (PSD %s), saved %s_HQ_%d.json"
                              % (mv, nul_num, min(lt, lu) > -1e-9, out, kq), flush=True)
        if cur is None or s2 >= cur or rng.random() < math.exp((s2 - cur) / temp):
            model, cur = m2, s2
        temp = max(float(os.environ.get("TFLOOR", "0.003")), temp * 0.999)   # TFLOOR (15/10): constant-temperature tail
        if mv % 200 == 0:
            print("move %d: numerical nullity histogram (c(l)=c(m)=1) %s, PSD visits %d, best exact nullity %d, "
                  "score %.4f (%.0f s)" % (mv, dict(sorted(hist.items())), npsd, best_null, cur, time.time() - t0),
                  flush=True)
    print("end: histogram %s, PSD visits %d, best exact nullity %d" % (dict(sorted(hist.items())), npsd, best_null),
          flush=True)


if __name__ == "__main__":
    main()
