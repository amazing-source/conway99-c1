"""Explore the forced neighbourhood extension of a co-Heawood core in C1."""
from itertools import combinations
import json
from pathlib import Path
import numpy as np
import sympy as sp


def core_with_rows(rows=(0,)):
    # Fano line l is orthogonal to the nonzero vector l over F_2^3.
    b = [[(s & t).bit_count() % 2 for t in range(1, 8)] for s in range(1, 8)]
    names = [('s', s) for s in range(7)] + [('t', t) for t in range(7)]
    edges = [(s, 7+t) for s in range(7) for t in range(7) if b[s][t]]
    cells = {}
    for s in rows:
        for t in range(7):
            cells[s, t] = []
            for k in range(2-b[s][t]):
                r = len(names)
                names.append(('r', s, t, k))
                cells[s, t].append(r)
                edges.extend([(s, r), (7+t, r)])
        zero = [t for t in range(7) if not b[s][t]]
        e0, e1, e2 = [cells[s, t] for t in zero]
        edges.extend([(e0[0], e1[0]), (e1[1], e2[0]), (e2[1], e0[1])])
    a = np.zeros((len(names), len(names)), dtype=int)
    for u, v in edges:
        a[u, v] = a[v, u] = 1
    return a, names, b, cells


def main():
    a, names, b, cells = core_with_rows()
    p = 27*np.eye(len(a), dtype=int) - 9*a + np.ones_like(a)
    q = 44*np.eye(len(a), dtype=int) + 11*a - 2*np.ones_like(a)
    bad = [(names[u], names[v], int((a@a)[u,v])) for u, v in combinations(range(len(a)), 2)
           if (a@a)[u,v] > 2-a[u,v]]
    print(json.dumps(dict(order=len(a), bad_pairs=bad,
        adjacency_spectrum=np.linalg.eigvalsh(a).round(8).tolist(),
        p_min=float(np.linalg.eigvalsh(p)[0]), q_min=float(np.linalg.eigvalsh(q)[0]))), flush=True)
    for label, mat in [('p3',p), ('p4',q)]:
        ns = sp.Matrix(mat.tolist()).nullspace()
        basis = []
        for v in ns:
            den = sp.ilcm(*[c.q for c in v])
            basis.append([int(c*den) for c in v])
        print(json.dumps(dict(matrix=label, nullity=len(basis), nullspace=basis)), flush=True)
    # Any 6-cycle in the union of row/column mate matchings projects to
    # a Fano incidence hexagon. Its only possible chords are diameters.
    # Two diameters create a nonedge with at least three common neighbours.
    ss = [0,1,3]  # nonzero vectors 1,2,4 are a noncollinear Fano triple
    tt = [next(t for t in range(7) if not b[ss[i]][t] and not b[ss[(i+1)%3]][t])
          for i in range(3)]
    labs = [(ss[0],tt[0]),(ss[1],tt[0]),(ss[1],tt[1]),
            (ss[2],tt[1]),(ss[2],tt[2]),(ss[0],tt[2])]
    for chord in [False,True]:
        c = np.zeros((20,20), dtype=int)
        c[:14,:14] = a[:14,:14]
        for k,(s,t) in enumerate(labs):
            c[14+k,s] = c[s,14+k] = 1
            c[14+k,7+t] = c[7+t,14+k] = 1
            j = 14+(k+1)%6
            c[14+k,j] = c[j,14+k] = 1
        if chord:
            c[14,17] = c[17,14] = 1
        p = 27*np.eye(20,dtype=int)-9*c+np.ones_like(c)
        q = 44*np.eye(20,dtype=int)+11*c-2*np.ones_like(c)
        print(json.dumps(dict(configuration='mate_hexagon', chord=chord, labels=labs,
                              p_min=float(np.linalg.eigvalsh(p)[0]),
                              q_min=float(np.linalg.eigvalsh(q)[0]),
                              p_nullity=20-sp.Matrix(p.tolist()).rank(),
                              q_nullity=20-sp.Matrix(q.tolist()).rank())), flush=True)


if __name__ == '__main__':
    main()
