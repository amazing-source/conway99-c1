"""C1, lab session, 2026-10-09. PILOT of a second-level necessary system on the 14-vertex cores (rank-free).
  python twisted_core_level2.py <twisted_core_check.json> <json list of bits to test> <out json> <first> <step> <max cores>
Codex's first level (its note 222): the 85 outside vertices are described by their masks b = N(w) ∩ H (at most one point
of S, any set of doubles) with multiplicities x_b; linear equations: each h of H has 14 - deg_H(h) outside neighbours,
each pair u, v of H has (1 or 2) - c_H(u, v) outside common neighbours.
Second level added here: Y[b, b'] = number of ordered ADJACENT pairs (w, w') of outside vertices with masks b, b'.
For every outside vertex w of mask b, exactly (strongly regular graph equations of the pairs (w, h), h in H):
   (a) w has 14 - |b| outside neighbours:            sum_b' Y[b, b'] = (14 - |b|) x_b ;
   (b) for h in H, w and h have 1 (h in b) or 2 (h not in b) common neighbours, |b ∩ N_H(h)| of them in H:
                                                       sum_{b' containing h} Y[b, b'] = (q - |b ∩ N_H(h)|) x_b ;
   Y symmetric, Y[b, b'] = 0 unless two adjacent outside vertices may carry b, b' (at most one common neighbour in H, and
   the two projector blocks of H + w + w' positive semidefinite), Y[b, b'] <= ub(b') x_b, Y[b, b] <= (ub(b) - 1) x_b.
All of this is linear in (x, Y) and necessary for an integer completion, at every rank. An infeasible LP would exclude
the core. HERE THE LP IS SOLVED IN FLOATING POINT ONLY: "infeasible" is a diagnostic to be certified exactly afterwards
(integer Farkas multipliers, as in Codex's first level); the mask and pair filters use exact integer certificates for
rejections. One process, below 2 GB."""
import sys, json, time, os
from itertools import combinations
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "twisted_core_check.py"), encoding="utf-8").read().split("def psd_or_vector")[1].split("\nout = ")[0]
ns = {"Fr": __import__("fractions").Fraction}; exec("def psd_or_vector" + src, ns); psd_or_vector = ns["psd_or_vector"]
D = json.load(open(sys.argv[1])); keep = json.load(open(sys.argv[2])); first, step, maxc = (int(x) for x in sys.argv[4:7]); t00 = time.time()
SUP = {6: (0, 3), 7: (1, 4), 8: (2, 3), 9: (2, 4), 10: (0, 5), 11: (1, 5), 12: (2, 5), 13: (2, 5)}; CLASS = [9, 9, 8, 9, 9, 8]
def psd_ok(a):
    n = len(a); A = a.astype(float); I = np.eye(n)
    for Qf, Qi in ((27 * I - 9 * A + 1, 27 * np.eye(n, dtype=object) - 9 * a.astype(object) + 1), (44 * I + 11 * A - 2, 44 * np.eye(n, dtype=object) + 11 * a.astype(object) - 2)):
        w, v = np.linalg.eigh(Qf)
        if w[0] > -1e-7: continue
        for scale in (10 ** 3, 10 ** 5, 10 ** 7):
            z = np.array([int(round(x)) for x in v[:, 0] / np.abs(v[:, 0]).max() * scale], dtype=object)
            if int(z @ Qi @ z) < 0: return False
        al = a.tolist(); Qm = [[27 * int(i == j) - 9 * al[i][j] + 1 for j in range(n)] for i in range(n)]; Qp = [[44 * int(i == j) + 11 * al[i][j] - 2 for j in range(n)] for i in range(n)]
        if psd_or_vector(Qm) is not None or psd_or_vector(Qp) is not None: return False
    return True
cores = [c for c in D["cores"] if c["bits"] in set(keep)]; out = {"tested_from": len(cores), "results": []}
for ci in range(first, len(cores), step)[:maxc]:
    c = cores[ci]; t0 = time.time(); a = np.zeros((14, 14), dtype=np.int64)
    for u, v in [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5), (4, 5), (0, 3), (1, 4)] + [(d, s) for d, sp in SUP.items() for s in sp] + [tuple(e) for e in c["edges_among_doubles"]]: a[u, v] = a[v, u] = 1
    cn = a @ a; deficit = (2 - a) - cn; np.fill_diagonal(deficit, 0); assert (deficit >= 0).all()
    masks = []
    for s in [None] + list(range(6)):
        for sub in range(256):
            b = np.zeros(14, dtype=np.int64)
            if s is not None: b[s] = 1
            for k in range(8):
                if (sub >> k) & 1: b[6 + k] = 1
            if ((a @ b) > 2 - b).any(): continue                                      # at most 1 (h in b) or 2 common neighbours with h inside H
            idx = np.flatnonzero(b)
            if any(deficit[u, v] < 1 for u, v in combinations(idx.tolist(), 2)): continue  # w would exceed the quota of the pair u, v
            e = np.zeros((15, 15), dtype=np.int64); e[:14, :14] = a; e[14, :14] = b; e[:14, 14] = b
            if psd_ok(e): masks.append(b)
    print("   masks %d  [%.1f s]" % (len(masks), time.time() - t0), flush=True)
    M = np.array(masks); nm = len(M); size = M.sum(axis=1); ab = M @ a                    # ab[i, h] = |b_i ∩ N_H(h)|
    cls = [(-1 if not b[:6].any() else int(np.flatnonzero(b[:6])[0])) for b in M]
    ub = np.array([min([33 if cls[i] < 0 else CLASS[cls[i]]] + [int(deficit[u, v]) for u, v in combinations(np.flatnonzero(M[i]).tolist(), 2)]) for i in range(nm)])
    ov = M @ M.T; pairs = []                                                             # admissible adjacent pairs of masks (i <= j)
    for i in range(nm):
        for j in range(i, nm):
            if ov[i, j] > 1 or (i == j and ub[i] < 2): continue
            e = np.zeros((16, 16), dtype=np.int64); e[:14, :14] = a; e[14, :14] = M[i]; e[:14, 14] = M[i]; e[15, :14] = M[j]; e[:14, 15] = M[j]; e[14, 15] = e[15, 14] = 1
            if ((e @ e)[np.triu_indices(16, 1)] > (2 - e)[np.triu_indices(16, 1)]).any(): continue
            if psd_ok(e): pairs.append((i, j))
    print("   adjacent mask pairs %d  [%.1f s]" % (len(pairs), time.time() - t0), flush=True)
    npair = len(pairs); nv = nm + npair; rr, cc, vv, rhs = [], [], [], []                 # variables: x_b, then Yu[i, j] (unordered-pair variable: Y[i,j] = Y[j,i] = Yu, Y[i,i] = 2 Yu)
    def eq(terms, r):
        k = len(rhs)
        for col, val in terms:
            if val: rr.append(k); cc.append(col); vv.append(float(val))
        rhs.append(float(r))
    eq([(i, 1) for i in range(nm)], 85)
    for h in range(14): eq([(i, 1) for i in range(nm) if M[i, h]], 14 - int(a[h].sum()))
    for u, v in combinations(range(14), 2): eq([(i, 1) for i in range(nm) if M[i, u] and M[i, v]], int(deficit[u, v]))
    inc = [[] for _ in range(nm)]
    for k, (i, j) in enumerate(pairs): inc[i].append((k, j)); (inc[j].append((k, i)) if i != j else None)
    for i in range(nm):
        eq([(nm + k, 2 if j == i else 1) for k, j in inc[i]] + [(i, -(14 - int(size[i])))], 0)                                   # (a)
        for h in range(14):
            q = 1 if M[i, h] else 2; eq([(nm + k, 2 if j == i else 1) for k, j in inc[i] if M[j, h]] + [(i, -(q - int(ab[i, h])))], 0)   # (b)
    Aeq = coo_matrix((vv, (rr, cc)), shape=(len(rhs), nv)).tocsr(); r2, c2, v2 = [], [], []; nb = 0
    for k, (i, j) in enumerate(pairs):                                                    # Y[i,j] <= ub_j x_i and <= ub_i x_j ; Y[i,i] = 2 Yu <= (ub_i - 1) x_i
        if i == j: r2 += [nb, nb]; c2 += [nm + k, i]; v2 += [2.0, -float(ub[i] - 1)]; nb += 1
        else:
            r2 += [nb, nb]; c2 += [nm + k, i]; v2 += [1.0, -float(ub[j])]; nb += 1
            r2 += [nb, nb]; c2 += [nm + k, j]; v2 += [1.0, -float(ub[i])]; nb += 1
    Aub = coo_matrix((v2, (r2, c2)), shape=(nb, nv)).tocsr(); bounds = [(0, float(ub[i])) for i in range(nm)] + [(0, None)] * npair
    lvl1 = linprog(np.zeros(nm), A_eq=Aeq[:1 + 14 + 91, :nm], b_eq=np.array(rhs[:1 + 14 + 91]), bounds=bounds[:nm], method="highs")
    print("   level 1 done  [%.1f s]; level-2 LP: %d variables, %d equalities, %d inequalities" % (time.time() - t0, nv, len(rhs), nb), flush=True)
    lvl2 = linprog(np.zeros(nv), A_eq=Aeq, b_eq=np.array(rhs), A_ub=Aub, b_ub=np.zeros(nb), bounds=bounds, method="highs-ipm", options={"time_limit": 60})
    st = lambda o: {0: "feasible", 2: "INFEASIBLE"}.get(o.status, "status %d" % o.status)
    out["results"].append({"bits": c["bits"], "edges_among_doubles": len(c["edges_among_doubles"]), "masks": nm, "adjacent_mask_pairs": npair, "level1": st(lvl1), "level2": st(lvl2), "seconds": round(time.time() - t0, 1)})
    print("core bits %d (e(D) = %d): %d masks, %d admissible adjacent mask pairs of %d; level 1: %s; level 2: %s  [%.0f s]" % (c["bits"], len(c["edges_among_doubles"]), nm, npair, nm * (nm + 1) // 2, st(lvl1), st(lvl2), time.time() - t0), flush=True)
    if time.time() - t00 > 240: break
json.dump(out, open(sys.argv[3], "w"), indent=0); R = out["results"]
print("cores tested %d: level 1 infeasible %d; level 2 infeasible %d (floating diagnostic, to be certified exactly)  [%.0f s]" % (len(R), sum(r["level1"] == "INFEASIBLE" for r in R), sum(r["level2"] == "INFEASIBLE" for r in R), time.time() - t00))
