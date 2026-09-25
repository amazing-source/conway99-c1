"""Max degeneracy d(L) per pair of star types (tau_a, tau_abar), annealing the holonomy sigma (notes/99)."""
import sys, random, math
import numpy as np
import line_ball as lb, line_ball_sa as sa, kbound_star as ks

others = lb.others


def anneal_sigma(ta, tb, seed, iters, free):
    rng = random.Random(seed)
    perm = others[:]; rng.shuffle(perm); sg = {b: perm[i] for i, b in enumerate(others)}
    cfg = (ta, tb, sg); tries = 0
    while not (free or lb.local_ok(*cfg)) and tries < 20000:
        u, v = rng.sample(others, 2); sg = dict(cfg[2]); sg[u], sg[v] = sg[v], sg[u]; cfg = (ta, tb, sg); tries += 1
    if not (free or lb.local_ok(*cfg)):
        return (-1, cfg)
    cur = sa.dval(cfg); best = (cur, cfg)
    for it in range(iters):
        T = (1 - it / iters) + 0.05
        u, v = rng.sample(others, 2); sg = dict(cfg[2]); sg[u], sg[v] = sg[v], sg[u]; new = (ta, tb, sg)
        if not (free or lb.local_ok(*new)):
            continue
        dv = sa.dval(new)
        if dv >= cur or rng.random() < math.exp((dv - cur) / T):
            cfg, cur = new, dv
            if cur > best[0]:
                best = (cur, cfg)
    return best


def main():
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    reps = ks.type_reps()
    reps['(6;-)'] = {b: lb.mate(b) for b in others}
    names = list(reps)
    for i, na in enumerate(names):
        for nb in names[i:]:
            res = []
            for free in (False, True):
                b = max((anneal_sigma(reps[na], reps[nb], s, iters, free) for s in range(3)), key=lambda z: z[0])
                res.append((b[0], sum(1 for x in others if b[1][2][x] == x)))
            print(f'{na:10s} {nb:10s} admissible max d {res[0][0]} (fix {res[0][1]}) | unconstrained max d {res[1][0]} (fix {res[1][1]})', flush=True)


if __name__ == '__main__':
    main()
