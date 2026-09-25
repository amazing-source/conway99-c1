"""Simulated annealing for the maximal degeneracy d(L) = dim ker_7(A_{G(L)} - 3I) of a line ball (notes/99).
Usage: line_ball_sa.py seed iters restarts [--free]   (--free: ignore the local admissibility check)
"""
import sys, math, random
import numpy as np
import line_ball as lb

others = lb.others


def dval(cfg):
    return 36 - lb.rank_mod(lb.cubic_graph(*cfg) - 3 * np.eye(36, dtype=np.int64))


def mutate(cfg, rng):
    ta, tb, sg = dict(cfg[0]), dict(cfg[1]), dict(cfg[2])
    w = rng.randrange(4)
    if w < 2:
        t = ta if w == 0 else tb
        u, v = rng.sample(others, 2)
        if t[u] != v:
            pu, pv = t[u], t[v]
            if rng.random() < 0.5:
                t[u], t[v], t[pu], t[pv] = pv, pu, v, u
            else:
                t[u], t[v], t[pu], t[pv] = v, u, pv, pu
    else:
        u, v = rng.sample(others, 2)
        sg[u], sg[v] = sg[v], sg[u]
    return ta, tb, sg


def grid_cfg():
    m = {b: lb.mate(b) for b in others}
    return dict(m), dict(m), {b: b for b in others}


def main():
    seed, iters, restarts = map(int, sys.argv[1:4])
    free = '--free' in sys.argv
    rng = random.Random(seed)
    best = (-1, None)
    g = grid_cfg()
    print('grid config: d =', dval(g), ' admissible:', lb.local_ok(*g), flush=True)
    for r in range(restarts):
        if r % 2 == 0:
            cfg = grid_cfg()
        else:
            ta, tb = lb.random_matching(rng), lb.random_matching(rng)
            perm = others[:]; rng.shuffle(perm)
            cfg = (ta, tb, {b: perm[i] for i, b in enumerate(others)})
        while not (free or lb.local_ok(*cfg)):
            cfg = mutate(cfg, rng)
        cur = dval(cfg)
        T0 = 1.0
        for it in range(iters):
            T = T0 * (1 - it / iters) + 0.05
            new = mutate(cfg, rng)
            if not (free or lb.local_ok(*new)):
                continue
            dv = dval(new)
            if dv >= cur or rng.random() < math.exp((dv - cur) / T):
                cfg, cur = new, dv
                if cur > best[0]:
                    best = (cur, cfg)
        fix = sum(1 for b in others if best[1][2][b] == b)
        print(f'restart {r}: best d so far {best[0]} (rank S24 = {23 - best[0]}), components '
              f'{lb.ncomp(lb.cubic_graph(*best[1]))}, sigma fixed points {fix}', flush=True)
    d, cfg = best
    print('BEST d =', d, 'tau_a =', cfg[0], 'tau_abar =', cfg[1], 'sigma =', cfg[2])


if __name__ == '__main__':
    main()
