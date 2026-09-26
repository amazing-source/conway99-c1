"""Anchored motif survivors (notes/130): sib pair model + Alt identities between sib pairs (alt_sib3.py).
An orientation dies iff every D-graph choice passing the tail rule and T+ is infeasible.
Usage: python run_alt_anchored.py <motif> <first_orientation> <seconds>   (resumable in chunks)"""
import sys, time, itertools
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
sys.path.insert(0, r"C:/home/researcher/Desktop/c99_structures_lab/ad")
from sib_model import from_anchored_motif
from motiflib import MOTIFS, B, survivors_full, two_factors, components, set_partitions_min2
from sib_labeled import build_sib_labeled
from alt_sib3 import add_alt_sib_all


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
            if Sk is None:
                ok = False
                break
            Pi = [p for p in Sk if p not in (i, j) and frozenset((i, k)) in CS[p]]
            if len(Sk) < 3 + (j in Sk) + len(Pi):
                ok = False
                break
        if ok:
            return True
    return False


def solve(orbs, alt):
    A, lo, hi, lb, ub, nvar, phi, ns, y, lab = build_sib_labeled(orbs)
    if alt:
        A, lo, hi, lb, ub, nvar, _ = add_alt_sib_all(A, lo, hi, lb, ub, nvar, phi, orbs)
    if np.any(lb > ub):
        return 'dead'
    res = milp(np.zeros(nvar), constraints=[LinearConstraint(A, lo, hi)], integrality=np.ones(nvar),
               bounds=Bounds(lb, ub), options={'time_limit': 40})
    return {0: 'alive', 2: 'dead'}.get(res.status, 'unknown')


name = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
tlim = float(sys.argv[3]) if len(sys.argv) > 3 else 270
sig = MOTIFS[name]
Sset = set(frozenset(p) for p in sig)
sibp = {k: [m for m in B if frozenset((k, m)) in Sset] for k in B}
res = survivors_full(name, sig)
print(name, 'orientations after tail rule:', len(res))
t0 = time.time()
tally = {}
for n_or in range(start, len(res)):
    if time.time() - t0 > tlim:
        print('time limit; resume at orientation', n_or)
        break
    arc, indeg, o, In = res[n_or]
    piv = [i for i in B if indeg[i] >= 2]
    allowed_at = lambda i: (lambda j, k: o[k] >= 3 + ((k, j) in arc) and o[j] >= 3 + ((j, k) in arc))
    Dopts = [two_factors(In[i], allowed_at(i)) for i in piv]
    base_alive = 0
    alt_alive = 0
    unknown = 0
    for Dchoice in itertools.product(*Dopts):
        Dg = dict(zip(piv, Dchoice))
        if not tplus_ok(sig, arc, o, In, Dg, sibp):
            continue
        orbs = from_anchored_motif([(a - 1, b - 1) for a, b in sig], {k - 1: [m - 1 for m in v] for k, v in In.items()},
                                   {k - 1: [(a - 1, b - 1) for a, b in E] for k, E in Dg.items()})
        sb = solve(orbs, False)
        if sb == 'dead':
            continue
        base_alive += 1
        sa = solve(orbs, True)
        if sa == 'alive':
            alt_alive += 1
            break
        if sa == 'unknown':
            unknown += 1
    status = 'alive' if alt_alive else ('unknown' if unknown else ('dead-by-alt' if base_alive else 'dead-base'))
    tally[status] = tally.get(status, 0) + 1
    print('orientation', n_or, status, {k: sorted(v) for k, v in In.items() if v}, '(%.0fs)' % (time.time() - t0))
    sys.stdout.flush()
print(name, 'tally', tally)
