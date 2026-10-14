"""Positive and negative control of the LOCAL-VIEW construction on the only small graph of the family:
srg(9,4,1,2) seen from a vertex (2 blocks, 4 inner vertices, 4 outer vertices). Same rules as h12_instance.build
(x - inner, block edges, inner - outer incidence, outer vertices sharing an inner vertex adjacent iff matched).
With the true matchings (M_a pairs the two vertices of the other block) the completion must be SAT; with a wrong
prescription (outer vertices sharing a declared non-adjacent) it must be UNSAT.
usage: python control_local9.py good.cnf bad.cnf
"""
import itertools
import sys
import srg_sat as S


def build9(matched):
    inner = [1, 2, 3, 4]
    mate = {1: 2, 2: 1, 3: 4, 4: 3}
    outer = [(a, b) for a in inner for b in inner if a < b and mate[a] != b]
    idx = {p: 5 + i for i, p in enumerate(outer)}
    fixed = {}

    def setf(u, v, val):
        if u > v:
            u, v = v, u
        fixed[(u, v)] = val

    for a in inner:
        setf(0, a, True)
        for b in inner:
            if a < b:
                setf(a, b, mate[a] == b)
    for p in outer:
        setf(0, idx[p], False)
        for c in inner:
            setf(c, idx[p], c in p)
    for p, q in itertools.combinations(outer, 2):
        if len(set(p) & set(q)) == 1:
            setf(idx[p], idx[q], matched)
    return 9, 4, 1, 2, fixed


for path, matched in ((sys.argv[1], True), (sys.argv[2], False)):
    n, k, lam, mu, fixed = build9(matched)
    enc, e = S.encode(n, k, lam, mu, fixed)
    S.write_dimacs(enc, path)
