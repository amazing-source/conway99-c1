"""What is the extra symmetry of the first-order data F_x when |Aut(F_x)| > |Aut(G)_x|? (14/10/2026)
For a vertex x: compute generators of Aut(F_x) (F_x = G minus the edges of the outer lines, see firstorder.py), keep
those that are not automorphisms of G, and describe their action on N(x): the permutation of the k/2 lines through x
and the set of lines whose two points are swapped. Also test the opposite-corner involution tau_x of note 176 s.5.2
(swap the two points of every line through x, z_ab -> z_a'b') on F_x.
usage: python extra_fx.py file.edges [...]"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import firstorder as FO
import pairgroup243 as PG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "spreadfree_243_2026-10-12"))
import aut_tools as T


def tau(A, x):
    n = len(A)
    adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    N = adj[x]
    mate = {a: (adj[a] & N).pop() for a in N}
    lab = {}
    for z in range(n):
        if z != x and z not in N:
            lab[z] = frozenset(adj[z] & N)
    inv = {v: k for k, v in lab.items()}
    p = list(range(n))
    for a in N:
        p[a] = mate[a]
    for z, s in lab.items():
        p[z] = inv[frozenset(mate[a] for a in s)]
    return p


def describe(A, x, g):
    n = len(A)
    adj = [set(np.nonzero(A[v])[0].tolist()) for v in range(n)]
    N = sorted(adj[x])
    mate = {a: (adj[a] & set(N)).pop() for a in N}
    lines = sorted({tuple(sorted((a, mate[a]))) for a in N})
    idx = {a: i for i, l in enumerate(lines) for a in l}
    perm = [idx[g[l[0]]] for l in lines]
    swapped = sum(1 for l in lines if g[l[0]] == l[1])
    fixed_lines = sum(1 for i, l in enumerate(lines) if perm[i] == i)
    cyc, seen = [], set()
    for i in range(len(lines)):
        if i in seen:
            continue
        c, j = 0, i
        while j not in seen:
            seen.add(j)
            j = perm[j]
            c += 1
        cyc.append(c)
    return "lines: cycle type %s, %d fixed, %d swapped in place" % (sorted(cyc, reverse=True), fixed_lines, swapped)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        A = T.load(f)
        n = len(A)
        o, s, gens = PG.common_group([A])
        orbs = T.vertex_orbits(n, gens)
        print(os.path.basename(f), flush=True)
        for O in orbs:
            x = O[0]
            B = FO.first_order(A, x)
            o1, g1 = FO.group_plain([B])
            t = tau(A, x)
            t_fx = np.array_equal(B, B[np.ix_(t, t)])
            t_g = np.array_equal(A, A[np.ix_(t, t)])
            extra = [g for g in g1 if not np.array_equal(A, A[np.ix_(g, g)])]
            print("  orbit %3d: |Aut_x| %d, |Aut(F_x)| %d; tau_x in Aut(F_x): %s, in Aut(G): %s; %d extra generators%s"
                  % (len(O), o // len(O), o1, t_fx, t_g, len(extra),
                     ("; first: " + describe(A, x, extra[0])) if extra else ""), flush=True)
