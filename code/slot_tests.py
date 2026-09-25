"""notes/109: run the slot calculus on the Hamming point (sanity: must NOT be refuted by slots alone),
the star and path configurations of notes/108 (must be refuted), and the L14 configurations."""
import itertools, sys
from slot_calculus import Config, build, propagate, LAB, CL, mate

def base():
    tau = {l: {z: mate(z) for z in LAB if z[0] != l[0]} for l in LAB}
    rho = {c: {z: z for z in LAB if z[0] != c} for c in CL}
    return tau, rho

def matchings_no_mate(labels):
    labels = list(labels)
    if not labels:
        yield []
        return
    a = labels[0]
    for b in labels[1:]:
        if b == mate(a):
            continue
        rest = [l for l in labels if l not in (a, b)]
        for m in matchings_no_mate(rest):
            yield [(a, b)] + m

def fpf_perms(items):
    items = list(items)
    for p in itertools.permutations(items):
        if all(p[i] != items[i] for i in range(len(items))):
            yield dict(zip(items, p))

def configs(twist):
    """twist: dict label -> set of classes it twists.  Yields all Config with these twisting sets."""
    tw_labels = [l for l in LAB if twist.get(l)]
    choices = []
    for l in tw_labels:
        labs = [(c, s) for c in sorted(twist[l]) for s in (0, 1)]
        choices.append(list(matchings_no_mate(labs)))
    Z = {c: [l for l in tw_labels if c in twist[l]] for c in CL}
    rchoices = [list(fpf_perms(Z[c])) if Z[c] else [dict()] for c in CL]
    for ms in itertools.product(*choices):
        for rs in itertools.product(*rchoices):
            tau, rho = base()
            for l, m in zip(tw_labels, ms):
                for a, b in m:
                    tau[l][a] = b; tau[l][b] = a
            for c, r in zip(CL, rs):
                for z, w in r.items():
                    rho[c][z] = w
            yield Config(tau, rho)

def run(name, twist):
    tot = ref = 0
    for cfg in configs(twist):
        tot += 1
        var, lo, hi, eqs, inc = build(cfg)
        ok, lo2, hi2, log = propagate(lo, hi, eqs)
        if not ok:
            ref += 1
    print(f'{name:40s} configurations {tot:5d}, refuted by slot propagation: {ref}', flush=True)

# run('Hamming point (no twist)', {})
# run('star |C|=2 (g=19)', {(0, 0): {1, 2}, (0, 1): {1, 2}})
# run('star |C|=3', {(0, 0): {1, 2, 3}, (0, 1): {1, 2, 3}})
# run('triangle (L11)', {(0, 0): {1, 2}, (0, 1): {1, 2}, (1, 0): {0, 2}, (1, 1): {0, 2}, (2, 0): {0, 1}, (2, 1): {0, 1}})
# run('path {02,01,13}', {(0, 0): {1, 2}, (0, 1): {1, 2}, (1, 0): {0, 3}, (1, 1): {0, 3}})
# run('L14 |C|=2 (a0 in 0, b0 in 1 twist {2,3})', {(0, 0): {2, 3}, (1, 0): {2, 3}})
# run('L14 |C|=3', {(0, 0): {2, 3, 4}, (1, 0): {2, 3, 4}})
