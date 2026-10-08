"""C1, lab session, 2026-10-09. INDEPENDENT re-implementation of ONE witness of the laptop session's result on (6,6) lines
(repo conway99-c2-aws, folder c1_rank37_girth5_lines, commit 15a3cfe3f; division of work agreed with Codex, who audits
the model). Scope: this single ball only.
  python lap_witness_check.py <comp66_types.json of that folder> <out json> [comb]
Ball: type 0 + type 0 of comp66_types.json, identity order of the layers, vertex u = 0, c0 = 1. Only the DATA convention
of that folder is reused (a component key (iota, t1, t2, pi): vertices 0..17, layer v // 6; mates i ~ iota[i],
6+i ~ 6+t1[i], 12+i ~ 12+t2[i]; cross edges i ~ 6+i, i ~ 12+i, 6+i ~ 12+pi[i]; second component shifted by 18).
None of its search code is used, and the quadratic data are computed differently:
  the 36 near vectors have Gram M0 = 3J - H (H = 3I - G) with radical z0 = 1_C1 - 1_C2; W = (M0 + z0 z0^T)^(-1) mod 7
  (z0.z0 = 36 = 1 mod 7), and for shadows n, n' (three points in each component, so 3.1 + n is orthogonal to z0)
        g(n, n') = (3.1 + n)^T W (3.1 + n') mod 7.
  A far vertex f is  p_f = (combination of near vectors) + nu_f n0,  q(n0) = c0, hence
        g(f, f) + c0 nu_f^2 = 0,      g(f, f') + c0 nu_f nu_f' = 3 + A_ff'  (so the left side must be 3 or 4),
        sum of nu_f over the ten far neighbours of a ball vertex = 0.
Star of u: ten shadows through u (two points per layer, three per component, no two mates, a member has at most one
G-neighbour inside, an outside vertex at most two, every pair inside has K > 0), one for each of the ten points a of
the layer of u with K[u][a] = 1; sum = K e_u; the two shadows through a transversal neighbour of u are adjacent to no
other; the eight others are matched in four adjacent pairs; adjacent shadows meet only in u, non-adjacent ones in at most
two points. Expected from the laptop session: 10 584 candidate shadows, 11 232 with a scalar, no star.
Mode "comb": positive control, the conditions mod 7 are ignored (any scalar, adjacency free): a star must be found.
Exhaustive depth-first search with forward checking and exact-cover propagation; integer arithmetic only. The order
of the root branches is deterministic, and TOP_START / TOP_END (environment) restrict a run to a range of them, so that
the search can be completed in several runs of less than five minutes. One process, below 2 GB."""
import sys, json, time
from itertools import combinations
import numpy as np
t0 = time.time(); types = json.load(open(sys.argv[1])); comb = len(sys.argv) > 3 and sys.argv[3] == "comb"; c0 = 1; u = 0
def comp_edges(key, base):
    iota, t1, t2, pi = key; E = set()
    for i in range(6):
        for x, y in ((i, iota[i]), (6 + i, 6 + t1[i]), (12 + i, 12 + t2[i]), (i, 6 + i), (i, 12 + i), (6 + i, 12 + pi[i])): E.add((min(x, y) + base, max(x, y) + base))
    return E
G = np.zeros((36, 36), dtype=np.int64)
for x, y in comp_edges(types[0]["key"], 0) | comp_edges(types[0]["key"], 18): G[x, y] = G[y, x] = 1
lay = np.array([(v % 18) // 6 for v in range(36)]); comp = np.array([v // 18 for v in range(36)])
assert (G.sum(axis=1) == 3).all() and all(sum(G[v, w] for w in range(36) if lay[w] == l) == 1 for v in range(36) for l in range(3))
G2 = G @ G; assert np.trace(G @ G2) == 0 and ((G2 - np.diag(np.diag(G2))) <= 1).all(), "girth >= 5 expected"
K = 12 * np.eye(36, dtype=np.int64) - G - G2 + 2 - (lay[:, None] == lay[None, :]).astype(np.int64); assert (K >= 0).all() and (K.sum(axis=1) == 60).all()
def inv7(M):
    n = len(M); A = [[int(x) % 7 for x in row] + [int(i == j) for j in range(n)] for i, row in enumerate(M)]
    for c in range(n):
        p = next(i for i in range(c, n) if A[i][c]); A[c], A[p] = A[p], A[c]; iv = pow(A[c][c], -1, 7); A[c] = [(x * iv) % 7 for x in A[c]]
        for i in range(n):
            if i != c and A[i][c]: f = A[i][c]; A[i] = [(x - f * y) % 7 for x, y in zip(A[i], A[c])]
    return np.array([row[n:] for row in A], dtype=np.int64)
H = 3 * np.eye(36, dtype=np.int64) - G; M0 = (3 - H) % 7; z0 = np.where(comp == 0, 1, -1); assert not ((M0 @ z0) % 7).any()
W = inv7((M0 + np.outer(z0, z0)) % 7); assert (((M0 + np.outer(z0, z0)) @ W) % 7 == np.eye(36, dtype=np.int64)).all()
mate = [int(next(z for z in range(36) if G[w, z] and lay[z] == lay[w])) for w in range(36)]; cross = [z for z in range(36) if G[u, z] and lay[z] != lay[u]]
Ls = [[w for w in range(36) if lay[w] == l] for l in range(3)]; o1, o2 = [l for l in range(3) if l != lay[u]]; shadows = []
for a in Ls[lay[u]]:
    if a == u or K[u, a] == 0: continue
    for b1, b2 in combinations(Ls[o1], 2):
        if mate[b1] == b2 or K[u, b1] == 0 or K[u, b2] == 0: continue
        for c1, c2 in combinations(Ls[o2], 2):
            if mate[c1] == c2 or K[u, c1] == 0 or K[u, c2] == 0: continue
            n = (u, a, b1, b2, c1, c2)
            if sum(int(comp[x]) for x in n) != 3: continue
            v = np.zeros(36, dtype=np.int64); v[list(n)] = 1; gn = G @ v
            if (gn[list(n)] > 1).any() or (gn[v == 0] > 2).any() or any(K[x, y] == 0 for x, y in combinations(n, 2)): continue
            shadows.append(n)
ns = len(shadows); Nsh = np.zeros((ns, 36), dtype=np.int64)
for i, n in enumerate(shadows): Nsh[i, list(n)] = 1
R = (3 + Nsh) % 7; assert not ((R @ z0) % 7).any(); gdiag = np.einsum("ij,jk,ik->i", R, W, R) % 7
sq = {}
for x in range(7): sq.setdefault((-c0 * x * x) % 7, []).append(x)              # g + c0 nu^2 = 0  <=>  g = -c0 nu^2
ent = [(i, nu) for i in range(ns) for nu in ([0] if comb else sq.get(int(gdiag[i]), []))]; m = len(ent)
print("candidate shadows %d (expected 10584); with a scalar %d (expected 11232)   [%.0f s]" % (ns, m if not comb else sum(len(sq.get(int(x), [])) for x in gdiag), time.time() - t0), flush=True)
labels = sorted(set(n[1] for n in shadows)); assert len(labels) == 10; eidx = [np.array([k for k, (i, nu) in enumerate(ent) if shadows[i][1] == a]) for a in labels]
EN = Nsh[[i for i, nu in ent]]; ENU = np.array([nu for i, nu in ent]); EAP = np.array([int(any(z in shadows[i] for z in cross)) for i, nu in ent]); ER = (3 + EN) % 7; ERW = (ER @ W) % 7
target = K[u].copy(); target[u] = 10
C0 = {}; C1 = {}                                                             # allowed as non-adjacent / as adjacent
for x in range(10):
    for y in range(10):
        if x == y: continue
        ix, iy = eidx[x], eidx[y]; ov = EN[ix] @ EN[iy].T
        cover_ok = ((EN[ix][:, None, :] + EN[iy][None, :, :]) <= target[None, None, :]).all(axis=2) if len(ix) * len(iy) * 36 < 4e8 else None
        if cover_ok is None:
            cover_ok = np.ones((len(ix), len(iy)), dtype=bool)
            for p in range(36):
                if p != u and target[p] == 1: cover_ok &= ~(EN[ix][:, p][:, None].astype(bool) & EN[iy][:, p][None, :].astype(bool))
        if comb: a0 = np.ones(ov.shape, dtype=bool); a1 = np.ones(ov.shape, dtype=bool)
        else: val = (ERW[ix] @ ER[iy].T + c0 * np.outer(ENU[ix], ENU[iy])) % 7; a0 = val == 3; a1 = val == 4
        nap = (EAP[ix][:, None] == 0) & (EAP[iy][None, :] == 0)
        C0[x, y] = a0 & (ov <= 2) & cover_ok; C1[x, y] = a1 & (ov == 1) & nap & cover_ok
print("pair tables built   [%.0f s]" % (time.time() - t0), flush=True)
import os
TOP_START = int(os.environ.get("TOP_START", "0")); TOP_END = int(os.environ.get("TOP_END", "10**9").replace("10**9", "1000000000"))   # resumable: range of root branches (deterministic order)
nodes = [0]; sols = []; BUDGET = 255.0; timed = [False]; top = [TOP_START - 1, 0]
ENB = [EN[eidx[l]].astype(bool) for l in range(10)]; PTS = [p for p in range(36) if p != u]
def propagate(masks, cover):
    """Exact cover reasoning to a fixed point: every point p needs target - cover more shadows through it; the labels that
    can still supply it must be at least that many, and when they are exactly that many each of them must go through p."""
    need = target - cover
    while True:
        changed = False; sup = np.zeros(36, dtype=np.int64); has = {}
        for l, mk in masks.items():
            if not mk.any(): return None
            h = ENB[l][mk].any(axis=0); has[l] = h; sup += h
        for p in PTS:
            if need[p] > sup[p]: return None
            if need[p] > 0 and need[p] == sup[p]:
                for l in masks:
                    if has[l][p]:
                        mk = masks[l] & ENB[l][:, p]
                        if mk.sum() != masks[l].sum(): masks[l] = mk; changed = True
        if not changed: return masks
def search(chosen, masks, cover, partner):
    """chosen: {label index: local candidate index}; masks: label -> bool array; partner: label -> partner label or None."""
    if timed[0] or sols: return
    nodes[0] += 1
    if nodes[0] % 200 == 0 and time.time() - t0 > BUDGET: timed[0] = True; return
    if len(chosen) < 10:
        masks = propagate(dict(masks), cover)
        if masks is None: return
    if len(chosen) == 10:
        if (cover == target).all() and (comb or int(sum(ENU[eidx[x][k]] for x, k in chosen.items())) % 7 == 0) and all(EAP[eidx[x][k]] or partner[x] is not None for x, k in chosen.items()):
            sols.append({labels[x]: (list(shadows[ent[eidx[x][k]][0]]), int(ENU[eidx[x][k]])) for x, k in chosen.items()})
        return
    x = min((l for l in range(10) if l not in chosen), key=lambda l: int(masks[l].sum())); live = np.flatnonzero(masks[x])
    if not chosen: top[1] = len(live)
    for pos, k in enumerate(live):
        if not chosen:
            if pos < TOP_START or pos >= TOP_END: continue
            top[0] = pos
        e = eidx[x][k]; ncov = cover + EN[e]
        if (ncov > target).any(): continue
        adjs = [y for y, ky in chosen.items() if C1[y, x][ky, k] and not C0[y, x][ky, k]] if not comb else []
        both = [y for y, ky in chosen.items() if C1[y, x][ky, k] and C0[y, x][ky, k]]          # comb mode only: status free
        if len(adjs) > 1 or any(partner[y] is not None for y in adjs) or (EAP[e] and adjs): continue
        options = [adjs[0]] if adjs else ([None] + [y for y in both if partner[y] is None and not EAP[e]] if comb else [None])
        for par in options:
            np2 = dict(partner); np2[x] = par
            if par is not None: np2[par] = x
            nm = {}; ok = True; full = np.flatnonzero(ncov == target)
            for l in range(10):
                if l in chosen or l == x: continue
                mk = masks[l] & (C0[x, l][k] | C1[x, l][k]) & ~(EN[eidx[l]][:, full].any(axis=1))
                if EAP[e] or np2[x] is not None: mk = mk & C0[x, l][k]                                # saturated: no further neighbour
                if par is not None: mk = mk & C0[par, l][chosen[par]]
                if not mk.any(): ok = False; break
                nm[l] = mk
            if not ok: continue
            ch2 = dict(chosen); ch2[x] = int(k)
            if not comb and any(np2[y] is None and not EAP[eidx[y][ky]] and not any((nm[l] & C1[y, l][ky]).any() for l in nm) for y, ky in ch2.items()): continue   # an unmatched member needs a possible partner
            search(ch2, nm, ncov, np2)
            if timed[0] or sols: return
c_start = np.zeros(36, dtype=np.int64); search({}, {l: np.ones(len(eidx[l]), dtype=bool) for l in range(10)}, c_start, {l: None for l in range(10)})
status = "UNFINISHED (time budget)" if timed[0] else ("STAR FOUND" if sols else "NO STAR (exhaustive)")
done_to = top[0] if timed[0] else min(TOP_END, top[1])
print("mode %s: %s; nodes %d; root branches [%d, %d) of %d exhausted in this run%s   [%.0f s]" % ("comb (control, mod 7 ignored)" if comb else "mod 7", status, nodes[0], TOP_START, done_to, top[1], "" if not timed[0] else " (branch %d interrupted)" % top[0], time.time() - t0))
json.dump({"ball": "type 0 + type 0, identity layer order, u = 0, c0 = 1", "mode": "comb" if comb else "mod7", "candidate_shadows": ns, "with_scalar": m, "candidates_per_label": [int(len(e)) for e in eidx],
           "status": status, "nodes": nodes[0], "root_branches_total": top[1], "root_range_exhausted": [TOP_START, done_to], "solution": sols[:1], "seconds": round(time.time() - t0, 1)}, open(sys.argv[2], "w"), indent=0)
