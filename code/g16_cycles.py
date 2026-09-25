"""Floor target g(x) <= 16 (notes/112).  By R0 + L13 + L12 (pattern form) the incomplete-pair graph N has minimum
degree >= 2 on the classes it touches, so |N| = 4 forces N = 4-cycle 0-1-2-3-0.  A label of class v twists either
nothing or both cycle-neighbours of v.  Enumerate the patterns (T_v = twisting labels of class v) up to symmetry,
then test every (tau, rho) configuration with the first-order slot calculus (propagation, then exact-certified LP)."""
import itertools, sys, time
from collections import Counter
from slot_calculus import LAB, CL, build, propagate
from slot_tests import configs
from slot_lp import lp_check

CYC = [0, 1, 2, 3]
def nbrs(v): return {CYC[(CYC.index(v) - 1) % 4], CYC[(CYC.index(v) + 1) % 4]}

def pattern(ts):            # ts: tuple of 4 frozensets of sides, T_v
    return {(v, s): frozenset(nbrs(v)) for v, T in zip(CYC, ts) for s in T}

def ok(W):
    N = {frozenset((l[0], c)) for l, s in W.items() for c in s}
    if N != {frozenset((CYC[i], CYC[(i + 1) % 4])) for i in range(4)}:
        return False
    for c in CL:                                           # L13
        if sum(1 for s in W.values() if c in s) == 1:
            return False
    for a, s in W.items():                                 # L12, pattern form
        for j in s:
            for side in (0, 1):
                if a[0] in W.get((j, side), ()):
                    continue
                if any(j in W.get(y, ()) for y in LAB if y[0] not in (a[0], j)):
                    continue
                return False
    return True

def canon(ts):
    """ts up to the dihedral group of the cycle and side swaps: only the sizes |T_v| matter up to side swaps"""
    sizes = [len(T) for T in ts]
    best = None
    for r in range(4):
        for refl in (False, True):
            seq = sizes[r:] + sizes[:r]
            if refl:
                seq = [seq[0]] + seq[1:][::-1]
            t = tuple(seq)
            best = t if best is None or t < best else best
    return best

reps = {}
for ts in itertools.product([frozenset(), frozenset({0}), frozenset({0, 1})], repeat=4):
    W = pattern(ts)
    if ok(W):
        reps.setdefault(canon(ts), ts)
print('4-cycle patterns (sizes |T_0..T_3|, up to symmetry):', sorted(reps), flush=True)
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 600
for key in sorted(reps):
    ts = reps[key]
    W = pattern(ts)
    t0 = time.time(); cnt = Counter(); n = 0
    for cfg in configs({l: set(s) for l, s in W.items()}):
        n += 1
        var, lo, hi, eqs, inc = build(cfg)
        good, lo2, hi2, log = propagate(lo, hi, eqs)
        if not good:
            cnt['refuted by propagation'] += 1
        else:
            st, _ = lp_check(cfg)
            cnt[st] += 1
        if time.time() - t0 > budget:
            cnt['(time budget reached)'] = 1
            break
    print(f'  sizes {key}: configurations tested {n} -> {dict(cnt)}  [{time.time() - t0:.0f}s]', flush=True)
