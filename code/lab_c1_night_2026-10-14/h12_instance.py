"""Target H12: a line l = {x, c, -c} with prism number 12, seen from x (block 7 = {13, 14} is the block of c).

Hypothesis in the local view: for every inner vertex a outside block 7, the matching M_a pairs 13 with 14
(the line {a, [a,13], [a,14]} is a prism on l). Nothing else is assumed: the other pairs of the 12 matchings M_a
and the two matchings M_13, M_14 are free.

usage: python h12_instance.py out.cnf
"""
import itertools
import sys

import srg_sat as S


def build(share):
    """share(a, b, b2) -> True / False / None for the adjacency of the outer vertices [a,b], [a,b2]."""
    inner = list(range(1, 15))
    mate = {a: (a + 1 if a % 2 == 1 else a - 1) for a in inner}
    outer = [(a, b) for a in inner for b in inner if a < b and mate[a] != b]
    idx = {p: 15 + i for i, p in enumerate(outer)}
    fixed = {}

    def setf(u, v, val):
        if u > v:
            u, v = v, u
        assert fixed.get((u, v), val) == val
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
        common = set(p) & set(q)
        if len(common) == 1:
            (a,) = common
            (b,) = set(p) - common
            (b2,) = set(q) - common
            val = share(a, b, b2)
            if val is not None:
                setf(idx[p], idx[q], val)
    return 99, 14, 1, 2, fixed, mate, outer, idx


def h12_share(a, b, b2):
    C = {13, 14}
    if a in C:
        return None
    if {b, b2} == C:
        return True
    if b in C or b2 in C:
        return False
    return None


if __name__ == "__main__":
    n, k, lam, mu, fixed, mate, outer, idx = build(h12_share)
    enc, e = S.encode(n, k, lam, mu, fixed)
    S.write_dimacs(enc, sys.argv[1])
    free = sum(1 for x in e.values() if x not in (S.T, S.F))
    print("H12: free pairs=%d, variables=%d, clauses=%d" % (free, enc.nv, len(enc.clauses)))
