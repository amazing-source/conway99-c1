"""Anchored motif survivors (notes/130) through structures' pair-level model extended to sib pairs (ad/sib_model.py).
An orientation dies iff every D-graph choice (2-factor per pivot passing the tail rule and T+) is infeasible."""
import sys, time, itertools
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import feasible_sib, from_anchored_motif
from motiflib import *
def tplus_ok(sig, arc, o, In, Dg, sibp):
    Out = {k: [m for m in B if (k, m) in arc] for k in B}
    inc = {p: (components(In[p], Dg[p]) if p in Dg else []) for p in B}
    dedges = [(i, a, b) for i, E in Dg.items() for x, y in E for (a, b) in ((x, y), (y, x))]
    Popts = {p: list(set_partitions_min2(Out[p])) for p in B}
    for parts in itertools.product(*[Popts[p] for p in B]):
        P = dict(zip(B, parts))
        CS = {p: set(inc[p]) | set(frozenset([m]) for m in sibp[p]) | set(P[p]) for p in B}
        ok = True
        for (i, j, k) in dedges:
            Sk = next((c for c in P[k] if i in c), None)
            if Sk is None: ok = False; break
            Pi = [p for p in Sk if p not in (i, j) and frozenset((i, k)) in CS[p]]
            if len(Sk) < 3 + (j in Sk) + len(Pi): ok = False; break
        if ok: return True
    return False
name = sys.argv[1]; tlim = float(sys.argv[2]) if len(sys.argv) > 2 else 250
sig = MOTIFS[name]; Sset = set(frozenset(p) for p in sig)
sibp = {k: [m for m in B if frozenset((k, m)) in Sset] for k in B}
res = survivors_full(name, sig)
t0 = time.time(); alive = 0; dead = 0; unknown = 0
for n_or, (arc, indeg, o, In) in enumerate(res):
    if time.time() - t0 > tlim: print('time limit; stopped at orientation', n_or); break
    piv = [i for i in B if indeg[i] >= 2]
    allowed_at = lambda i: (lambda j, k: o[k] >= 3 + ((k, j) in arc) and o[j] >= 3 + ((j, k) in arc))
    Dopts = [two_factors(In[i], allowed_at(i)) for i in piv]
    status = 'dead'
    for Dchoice in itertools.product(*Dopts):
        Dg = dict(zip(piv, Dchoice))
        if not tplus_ok(sig, arc, o, In, Dg, sibp): continue
        sig0 = [(a - 1, b - 1) for a, b in sig]
        In0 = {k - 1: [m - 1 for m in v] for k, v in In.items()}
        Dg0 = {k - 1: [(a - 1, b - 1) for a, b in E] for k, E in Dg.items()}
        orbs = from_anchored_motif(sig0, In0, Dg0)
        r = feasible_sib(orbs, time_limit=60)
        if r is None: continue
        status = 'alive' if not isinstance(r, str) else 'unknown'
        break
    if status == 'alive': alive += 1
    elif status == 'dead': dead += 1
    else: unknown += 1
    print('orientation', n_or, status, {k: sorted(v) for k, v in In.items() if v}, '(%.0fs)' % (time.time() - t0)); sys.stdout.flush()
print(name, 'anchored survivors tested:', alive + dead + unknown, 'dead', dead, 'alive', alive, 'unknown', unknown)
