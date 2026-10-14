"""Flip lemma check (14/10/2026). For a vertex x and a line l = {x,a,a'} through x, the flip s_l fixes x and every
vertex of N(x) - l, swaps a and a', and sends z_uv to z_(s u)(s v). Lemma (hand proof in NOTE part 3):
s_l preserves the first-order data F_x  <=>  (i) l has the maximal number 2(m-1) of parallel lines (pi_u(a) = a' for
every u in N(x) - l) and (ii) pi_a = pi_a'. This script tests both sides on every line through one vertex of each orbit.
usage: python flip_check.py file.edges [...]"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firstorder as FO
import pairgroup243 as PG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T


def local(A, x):
    n = len(A)
    adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    N = adj[x]
    mate = {a: (adj[a] & N).pop() for a in N}
    lab = {z: frozenset(adj[z] & N) for z in range(n) if z != x and z not in N}
    inv = {s: z for z, s in lab.items()}

    def pi(u, b):            # pi_u(b): z_{u,pi_u(b)} is the special neighbour of z_ub via u
        z = inv[frozenset((u, b))]
        w = ((adj[z] & adj[u]) - {x}).pop()      # third point of the line {u, z, w}
        return next(iter(lab[w] - {u}))
    return adj, N, mate, lab, inv, pi


if __name__ == "__main__":
    for f in sys.argv[1:]:
        A = T.load(f)
        n = len(A)
        o, s, gens = PG.common_group([A])
        orbs = T.vertex_orbits(n, gens)
        tally = {}
        for O in orbs:
            x = O[0]
            B = FO.first_order(A, x)
            adj, N, mate, lab, inv, pi = local(A, x)
            lines = sorted({tuple(sorted((a, mate[a]))) for a in N})
            for (a, a2) in lines:
                p = list(range(n))
                p[a], p[a2] = a2, a
                sw = {a: a2, a2: a}
                for z, st in lab.items():
                    p[z] = inv[frozenset(sw.get(u, u) for u in st)]
                in_fx = bool(np.array_equal(B, B[np.ix_(p, p)]))
                in_g = bool(np.array_equal(A, A[np.ix_(p, p)]))
                flat = all(pi(u, a) == a2 for u in N - {a, a2})
                same = all(pi(a, b) == pi(a2, b) for b in N - {a, a2})
                key = (in_fx, flat and same, flat, in_g)
                tally[key] = tally.get(key, 0) + len(O)
        print("%s: (flip in Aut(F_x), (i)&(ii), (i) flat, flip in Aut(G)) -> number of (vertex, line) pairs: %s"
              % (os.path.basename(f), dict(sorted(tally.items()))), flush=True)
