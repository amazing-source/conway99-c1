"""Anchored family of the Sigma != 0 motifs (every non-sib pair anchored: both orbits pivot at the same block).
Hand-derived rules (motif version of C2's tail lemma 25.1/25.2, notes/129 companion):
 - orientation j -> k on each non-sib pair jk anchored at k; d_k = in-degree, s_k = Sigma-degree, w_k = d_k + s_k,
   o_k = 6 - w_k (out-degree);
 - d_k != 1 (a single anchored pair at k would be D-paired with itself = sib);
 - at each pivot i with d_i >= 2, the D-graph on In(i) is a 2-regular loopless multigraph (digons allowed);
 - tail rule: for D-adjacent arms j, k at a pivot, o_k >= 3 + [k -> j] (equilibrium at k on X_Out(k), which is a union
   of components: In(k) is closed (D-cycles), sib partners are prisms).
Exhaustive over orientations of K7 - Sigma; reports survivors."""
import itertools, sys
MOTIFS = {'K2': [(6, 7)], 'P3': [(2, 3), (3, 4)], '2K2': [(1, 7), (5, 6)], 'K3': [(1, 3), (1, 5), (3, 5)],
          'P4': [(1, 7), (5, 6), (6, 7)], 'P3+K2': [(2, 3), (3, 4), (6, 7)], '3K2': [(1, 5), (2, 4), (6, 7)],
          'P5': [(1, 2), (2, 3), (3, 4), (4, 5)], '2P3': [(1, 4), (1, 5), (3, 6), (3, 7)]}
B = range(1, 8)
def two_factor_exists(V, allowed):
    """2-regular loopless multigraph on V (edge multiplicity <= 2) using allowed pairs."""
    V = list(V)
    if not V: return True
    if len(V) == 1: return False
    need = {v: 2 for v in V}
    pairs = [p for p in itertools.combinations(V, 2) if allowed(*p)]
    def rec(idx, need):
        # pick first vertex with need > 0
        v = next((u for u in V if need[u] > 0), None)
        if v is None: return True
        for (a, b) in pairs:
            if v not in (a, b): continue
            u = b if a == v else a
            if need[u] <= 0: continue
            need[v] -= 1; need[u] -= 1
            ok = rec(idx, need)
            need[v] += 1; need[u] += 1
            if ok: return True
        return False
    return rec(0, dict(need))
def analyse(name, sig):
    S = set(frozenset(p) for p in sig)
    sdeg = {k: sum(1 for p in S if k in p) for k in B}
    edges = [(a, b) for a, b in itertools.combinations(B, 2) if frozenset((a, b)) not in S]
    surv = []
    for bits in range(1 << len(edges)):
        arc = {}   # arc[(a,b)] = True if a -> b
        indeg = {k: 0 for k in B}; In = {k: [] for k in B}
        for t, (a, b) in enumerate(edges):
            if bits >> t & 1: tail, head = a, b
            else: tail, head = b, a
            arc[(tail, head)] = True; indeg[head] += 1; In[head].append(tail)
        if any(indeg[k] == 1 for k in B): continue
        w = {k: indeg[k] + sdeg[k] for k in B}; o = {k: 6 - w[k] for k in B}
        def allowed_at(i):
            def f(j, k):
                # D-edge {j,k} at pivot i: need o_k >= 3 + [k->j] and o_j >= 3 + [j->k]
                return o[k] >= 3 + (1 if (k, j) in arc else 0) and o[j] >= 3 + (1 if (j, k) in arc else 0)
            return f
        ok = True
        for i in B:
            if indeg[i] >= 2 and not two_factor_exists(In[i], allowed_at(i)):
                ok = False; break
        if ok: surv.append(dict(indeg))
    return surv

import sys
def survivors_full(name, sig):
    S = set(frozenset(p) for p in sig)
    sdeg = {k: sum(1 for p in S if k in p) for k in B}
    edges = [(a, b) for a, b in itertools.combinations(B, 2) if frozenset((a, b)) not in S]
    out = []
    for bits in range(1 << len(edges)):
        arc = set(); indeg = {k: 0 for k in B}; In = {k: [] for k in B}
        for t, (a, b) in enumerate(edges):
            tail, head = (a, b) if bits >> t & 1 else (b, a)
            arc.add((tail, head)); indeg[head] += 1; In[head].append(tail)
        if any(indeg[k] == 1 for k in B): continue
        w = {k: indeg[k] + sdeg[k] for k in B}; o = {k: 6 - w[k] for k in B}
        def allowed_at(i):
            return lambda j, k: o[k] >= 3 + ((k, j) in arc) and o[j] >= 3 + ((j, k) in arc)
        if all(indeg[i] < 2 or two_factor_exists(In[i], allowed_at(i)) for i in B):
            out.append((arc, indeg, o, In))
    return out


import itertools, sys
def two_factors(V, allowed):
    V = list(V); res = []
    pairs = [p for p in itertools.combinations(V, 2) if allowed(*p)]
    def rec(need, chosen):
        v = next((u for u in V if need[u] > 0), None)
        if v is None:
            res.append(tuple(sorted(chosen))); return
        for (a, b) in pairs:
            if v not in (a, b): continue
            u = b if a == v else a
            if need[u] <= 0: continue
            need[v] -= 1; need[u] -= 1; chosen.append((a, b))
            rec(need, chosen)
            chosen.pop(); need[v] += 1; need[u] += 1
    rec({v: 2 for v in V}, [])
    return sorted(set(res))
def components(V, edges):
    parent = {v: v for v in V}
    def f(x):
        while parent[x] != x: x = parent[x]
        return x
    for a, b in edges: parent[f(a)] = f(b)
    comp = {}
    for v in V: comp.setdefault(f(v), set()).add(v)
    return [frozenset(c) for c in comp.values()]
def set_partitions_min2(items):
    items = list(items)
    if not items: yield []; return
    first, rest = items[0], items[1:]
    for r in range(1, len(rest) + 1):
        for comb in itertools.combinations(rest, r):
            block = frozenset((first,) + comb)
            remaining = [x for x in rest if x not in comb]
            for p in set_partitions_min2(remaining):
                yield [block] + p
def check_orientation(sig, arc, indeg, o, In):
    S = set(frozenset(p) for p in sig)
    sibp = {k: [m for m in B if frozenset((k, m)) in S] for k in B}
    Out = {k: [m for m in B if (k, m) in arc] for k in B}
    piv = [i for i in B if indeg[i] >= 2]
    def allowed_at(i):
        return lambda j, k: o[k] >= 3 + ((k, j) in arc) and o[j] >= 3 + ((j, k) in arc)
    Dopts = [two_factors(In[i], allowed_at(i)) for i in piv]
    Popts = {p: list(set_partitions_min2(Out[p])) for p in B}
    blocks_list = list(B)
    for Dchoice in itertools.product(*Dopts):
        Dg = dict(zip(piv, Dchoice))
        # components of G_p from In side and sib singletons
        inc = {p: (components(In[p], Dg[p]) if p in Dg else []) for p in B}
        # D-edges: list of (i, j, k) meaning X in ij via i, D(X) in ik  (both orders)
        dedges = []
        for i, E in Dg.items():
            for a, b in E:
                dedges.append((i, a, b)); dedges.append((i, b, a))
        # search Out-partitions block by block (constraint uses partition at k and components at p in S)
        def comp_sets(p, part):
            return set(inc[p]) | set(frozenset([m]) for m in sibp[p]) | set(part)
        for parts in itertools.product(*[Popts[p] for p in blocks_list]):
            P = dict(zip(blocks_list, parts))
            CS = {p: comp_sets(p, P[p]) for p in B}
            ok = True
            for (i, j, k) in dedges:
                Sk = next((c for c in P[k] if i in c), None)
                if Sk is None: ok = False; break
                Pi = [p for p in Sk if p not in (i, j) and frozenset((i, k)) in CS[p]]
                if len(Sk) < 3 + (j in Sk) + len(Pi): ok = False; break
            if ok: return True
    return False
