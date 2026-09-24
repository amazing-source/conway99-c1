"""Positive control of the rooted-model equation generator on REAL graphs (no SAT involved).
For a real srg(n, 2(t+1), 1, 2) (srg(9,4,1,2), BvLS srg(243,22,1,2)) and a root x:
  - relabel N(x) as labels (class c, sign s) with mate = sign flip, X-vertices as pairs of labels;
  - read tau from the real graph;
  - rebuild the adjacency ORACLE exactly as rooted_model.py does (fixed parts from tau, 'unknown' disjoint edges read
    from the real graph) and check it reproduces the real adjacency matrix;
  - evaluate every SRG equation in the form the model emits it (const + number of true unknown literals == wanted)
    and the degree constraint of X-vertices (2t - 2 disjoint neighbours).
A single failure would reveal a conceptual error shared by hamming_point.py / rooted_model.py / rooted_family.py.
"""
import itertools, sys
import numpy as np
import graphs, rooted


def check(A, x=0):
    R = rooted.Rooted(A, x)
    n = len(A)
    t = len(R.L) // 2 - 1
    lab = {}
    for i, (a, ab) in enumerate(R.classes()):
        lab[a], lab[ab] = (i, 0), (i, 1)
    inv = {v: k for k, v in lab.items()}
    LABELS = sorted(inv)
    mate = lambda l: (l[0], 1 - l[1])
    tau = {lab[a]: {lab[b]: lab[c] for b, c in R.tau[a].items()} for a in R.L}
    Xv = [frozenset((a, b)) for a, b in itertools.combinations(LABELS, 2) if a[0] != b[0]]
    real = {'x': x}
    for l in LABELS:
        real[l] = inv[l]
    for u in Xv:
        a, b = tuple(u)
        real[u] = R.vertex_of[frozenset((inv[a], inv[b]))]
    V = ['x'] + LABELS + Xv
    assert len(V) == n and len(set(real[v] for v in V)) == n

    def adj(u, v):  # identical logic to rooted_model.build (unknown -> read from real graph)
        if u == v:
            return ('c', 0)
        if u == 'x' or v == 'x':
            o = v if u == 'x' else u
            return ('c', 1 if isinstance(o, tuple) else 0)
        ul, vl = isinstance(u, tuple), isinstance(v, tuple)
        if ul and vl:
            return ('c', 1 if mate(u) == v else 0)
        if ul:
            return ('c', 1 if u in v else 0)
        if vl:
            return ('c', 1 if v in u else 0)
        com = u & v
        if com:
            (a,) = com
            (b,) = u - com
            (c,) = v - com
            return ('c', 1 if tau[a][b] == c else 0)
        return ('v', int(A[real[u], real[v]]))
    # 1) oracle reproduces the real graph
    mism = sum(1 for u in V for v in V if adj(u, v)[1] != A[real[u], real[v]])
    # 2) degrees of X-vertices (disjoint neighbours = 2t - 2)
    degbad = sum(1 for u in Xv if sum(adj(u, w)[1] for w in Xv if w != u and adj(u, w)[0] == 'v') != 2 * t - 2)
    # 3) every SRG equation as emitted
    bad = 0
    for p in range(n):
        for q in range(p + 1, n):
            u, v = V[p], V[q]
            auv = adj(u, v)
            const, lits_true = 0, 0
            for w in V:
                if w in (u, v):
                    continue
                a1, a2 = adj(u, w), adj(v, w)
                if a1 == ('c', 0) or a2 == ('c', 0):
                    continue
                if a1[0] == 'c' and a2[0] == 'c':
                    const += 1
                else:
                    lits_true += a1[1] * a2[1]
            want = 1 if auv[1] else 2
            if const + lits_true != want:
                bad += 1
    return t, mism, degbad, bad


if __name__ == '__main__':
    for name in ['srg9', 'bvls']:
        A = graphs.ALL[name]()
        for x in ([0, 5] if name == 'srg9' else [0, 17, 142]):
            t, mism, degbad, bad = check(A, x)
            print(f'{name} root {x} (t = {t}): oracle mismatches {mism}, degree violations {degbad}, '
                  f'SRG-equation violations {bad}', flush=True)
