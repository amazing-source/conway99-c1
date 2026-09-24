"""Check of a local identity (notes/80): for a vertex x and a line l = {x, c, c'} through x,
  f_l(x) := number of lines contained in Gamma_2(x) that contain a neighbour of c AND a neighbour of c'
  equals t_l(x) := number of labels b (neighbours of x off l) for which the matching tau_b does not pair c with c'
  (i.e. 12 - (number of prisms containing l), in general 2t - (prisms on l)).
Checked on every vertex / line of the available twisted local-axiom geometries and of BvLS.
"""
import json
import numpy as np
import graphs, rooted


def check(name, A):
    A = np.asarray(A)
    n = len(A)
    adj = rooted.adjacency_lists(A)
    L = [tuple(l) for l in rooted.lines(A)]
    bad = tot = 0
    for x in range(n):
        Nx = adj[x]
        dist2 = {v for v in range(n) if v != x and v not in Nx and (adj[v] & Nx)}
        inX = [l for l in L if not any(v == x or v in Nx for v in l)]   # lines avoiding the ball B1(x) (= inside Gamma_2 when diameter 2)
        for l in L:
            if x not in l:
                continue
            c, cb = [v for v in l if v != x]
            f = sum(1 for m in inX if any(c in adj[v] for v in m) and any(cb in adj[v] for v in m))
            # t: labels b off l such that the point adjacent to b and c (other than x) and the one adjacent to b and cb
            # are NOT on a common line through b  <=>  tau_b does not pair c with cb
            t = 0
            for b in Nx:
                if b in l:
                    continue
                zc = next(iter((adj[b] & adj[c]) - {x}))
                zcb = next(iter((adj[b] & adj[cb]) - {x}))
                if zcb not in adj[zc]:
                    t += 1
            tot += 1
            bad += (f != t)
    print(f'{name}: {tot} (vertex, line) pairs checked, mismatches: {bad}')


if __name__ == '__main__':
    check('twist t=2 (20)', json.load(open('../data/t2_twisted.json')))
    check('twist t=3 (39)', json.load(open('../data/t3_twisted.json')))
    check('twist t=3 (42)', json.load(open('../data/t3_twisted_42.json')))
    check('BvLS', graphs.bvls())
