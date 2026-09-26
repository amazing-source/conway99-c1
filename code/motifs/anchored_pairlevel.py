"""Anchored motifs, third stage: single-root pair-level test (structures' AD method, NOTE_S28) on every surviving
(orientation, D-graphs, Out-partitions).  For a root w of W in pair P={a,t} anchored at t (a -> t):
  pivot zeros: phi(t m2) = 2 for D(W) in {t,m2}, phi(t m) = 0 otherwise (incl. own pair);
  F1 at a: sum_{m != a} phi(a m) = 2;  anchored zeros at a: phi(a m) = 0 for m in In(a);
  balance at every k not in P, on every component S of G_k: sum_{m in S} phi(k m) = |S| - |S & P|.
Integer 0 <= phi <= 3.  A configuration dies if some orbit is infeasible for every choice of its D-partner."""
import itertools, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from motiflib import *
PAIRS = [frozenset(p) for p in itertools.combinations(B, 2)]
PI = {p: i for i, p in enumerate(PAIRS)}
def feasible(eqs, lb, ub):
    A = np.zeros((len(eqs), 21)); v = np.zeros(len(eqs))
    for r, (c, val) in enumerate(eqs):
        for Q, x in c.items(): A[r, PI[Q]] += x
        v[r] = val
    res = milp(c=np.zeros(21), constraints=[LinearConstraint(A, v, v)], integrality=np.ones(21),
               bounds=Bounds([lb[Q] for Q in PAIRS], [ub[Q] for Q in PAIRS]))
    return res.status == 0
def config_alive(sig, arc, indeg, o, In, Dg, P):
    S = set(frozenset(p) for p in sig)
    sibp = {k: [m for m in B if frozenset((k, m)) in S] for k in B}
    comps = {}
    for k in B:
        cs = []
        if k in Dg: cs += [set(c) for c in components(In[k], Dg[k])]
        cs += [{m} for m in sibp[k]]
        cs += [set(c) for c in P[k]]
        comps[k] = cs
    for (a, t) in arc:           # pair {a,t} anchored at t
        Pp = frozenset((a, t))
        # D-neighbours of a at pivot t
        nbrs = [b if x == a else x for (x, b) in Dg[t] if a in (x, b)]
        ok_any = False
        for m2 in set(nbrs):
            lb = {Q: 0 for Q in PAIRS}; ub = {Q: 3 for Q in PAIRS}
            for m in B:
                if m == t: continue
                Q = frozenset((t, m))
                if m == m2: lb[Q] = ub[Q] = 2
                else: ub[Q] = 0
            for m in In[a]:
                ub[frozenset((a, m))] = 0
            eqs = [({frozenset((a, m)): 1 for m in B if m != a}, 2)]
            for k in B:
                if k in Pp: continue
                for Sc in comps[k]:
                    eqs.append(({frozenset((k, m)): 1 for m in Sc}, len(Sc) - len(Sc & Pp)))
            if any(lb[Q] > ub[Q] for Q in PAIRS): continue
            if feasible(eqs, lb, ub): ok_any = True; break
        if not ok_any: return False
    return True
def run(name):
    sig = MOTIFS[name]
    res = survivors_full(name, sig)
    alive_orient = 0; alive_list = []
    for arc, indeg, o, In in res:
        Sset = set(frozenset(p) for p in sig)
        sibp = {k: [m for m in B if frozenset((k, m)) in Sset] for k in B}
        Out = {k: [m for m in B if (k, m) in arc] for k in B}
        piv = [i for i in B if indeg[i] >= 2]
        allowed_at = lambda i: (lambda j, k: o[k] >= 3 + ((k, j) in arc) and o[j] >= 3 + ((j, k) in arc))
        Dopts = [two_factors(In[i], allowed_at(i)) for i in piv]
        Popts = {p: list(set_partitions_min2(Out[p])) for p in B}
        found = False
        for Dchoice in itertools.product(*Dopts):
            Dg = dict(zip(piv, Dchoice))
            inc = {p: (components(In[p], Dg[p]) if p in Dg else []) for p in B}
            dedges = [(i, a, b) for i, E in Dg.items() for x, y in E for (a, b) in ((x, y), (y, x))]
            for parts in itertools.product(*[Popts[p] for p in B]):
                Pp = dict(zip(B, parts))
                CS = {p: set(inc[p]) | set(frozenset([m]) for m in sibp[p]) | set(Pp[p]) for p in B}
                ok = True
                for (i, j, k) in dedges:
                    Sk = next((c for c in Pp[k] if i in c), None)
                    if Sk is None: ok = False; break
                    Pi = [p for p in Sk if p not in (i, j) and frozenset((i, k)) in CS[p]]
                    if len(Sk) < 3 + (j in Sk) + len(Pi): ok = False; break
                if not ok: continue
                if config_alive(sig, arc, indeg, o, In, Dg, Pp):
                    found = True; alive_list.append((In, Dg, Pp)); break
            if found: break
        if found: alive_orient += 1
    print('%-6s anchored: tail-rule %d -> alive after T+ and single-root pair level: %d' % (name, len(res), alive_orient))
    for In, Dg, Pp in alive_list[:2]:
        print('    In', {k: sorted(v) for k, v in In.items() if v}, 'Dg', Dg, 'Out-parts', {k: [sorted(c) for c in v] for k, v in Pp.items() if v})
for name in sys.argv[1:]:
    run(name)
