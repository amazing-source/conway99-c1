"""Rooted SAT model of srg(v,k,1,2) WITH symmetry breaking of the local group W(B_{k/2}) (14/10/2026).

For mu = 2 every non-collinear pair {i,j} of neighbours of x has exactly one outer common neighbour, so the outer
vertices are in bijection with these pairs; with the columns sorted (rooted_pq.py) the label of outer vertex o is the
o-th pair in decreasing lexicographic order: the a-variables are fixed here by unit clauses.
The remaining symmetry is W(B_{k/2}) (permutations of the lines through x and swaps of the two points of a line). An
element s acts on the inner vertices, hence on the pairs, hence on the outer vertices (o -> o' with pair(o') =
s(pair(o))), hence on the e-variables: e[o,q] -> e[s o, s q]. This is a permutation of the variables mapping solutions
to solutions; the lexicographically smallest solution of each orbit satisfies X <=_lex X o pi for every group element
pi, so adding these constraints (on a prefix of the variable order, for a chosen set of group elements) is sound.
Group elements used: all transpositions of two lines, all point swaps on one line, and products of a line
transposition with a point swap.
usage: python rooted_pq_sb.py v k out.cnf [prefix length, default 600]
"""
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rooted_pq as RP


def build_sb(v, k, path, prefix):
    mu = 2
    F, a, e, n = RP.build(v, k, mu, path)
    inner = list(range(k))
    # labels: pairs of inner vertices on different lines, as bit vectors with bit for inner vertex 0 most significant
    pairs = [(i, j) for i, j in itertools.combinations(inner, 2) if i // 2 != j // 2]
    assert len(pairs) == n

    def key(p):
        return tuple(1 if t in p else 0 for t in inner)
    order = sorted(pairs, key=key, reverse=True)
    pos = {p: o for o, p in enumerate(order)}
    for o, p in enumerate(order):
        for i in inner:
            F.add([a[i][o]] if i in p else [-a[i][o]])
    # variable order for the lex-leader constraints: e[o,q] for o < q in increasing (o, q)
    evars = [(o, q) for o, q in itertools.combinations(range(n), 2)]
    index = {pq: t for t, pq in enumerate(evars)}

    def outer_perm(s):            # s: permutation of inner vertices (list)
        return [pos[tuple(sorted((s[i], s[j])))] for (i, j) in order]

    elements = []
    m = k // 2
    for l1, l2 in itertools.combinations(range(m), 2):
        s = list(inner)
        s[2 * l1], s[2 * l2] = 2 * l2, 2 * l1
        s[2 * l1 + 1], s[2 * l2 + 1] = 2 * l2 + 1, 2 * l1 + 1
        elements.append(s)
    for l in range(m):
        s = list(inner)
        s[2 * l], s[2 * l + 1] = 2 * l + 1, 2 * l
        elements.append(s)
    for l1, l2 in itertools.combinations(range(m), 2):
        s = list(inner)
        s[2 * l1], s[2 * l2] = 2 * l2 + 1, 2 * l1
        s[2 * l1 + 1], s[2 * l2 + 1] = 2 * l2, 2 * l1 + 1
        elements.append(s)
    count = 0
    for s in elements:
        op = outer_perm(s)
        # pi on e-variables: position t = (o,q) -> image (op[o], op[q]) sorted
        X = [e[pq] for pq in evars[:prefix]]
        Y = []
        for (o, q) in evars[:prefix]:
            oo, qq = sorted((op[o], op[q]))
            Y.append(e[(oo, qq)])
        if X == Y:
            continue
        # X <=_lex Y (bit vectors, first position most significant): forbid the first difference with X=1, Y=0
        eq = True
        for xi, yi in zip(X, Y):
            if xi == yi:
                continue
            if eq is True:
                F.add([-xi, yi])
            else:
                F.add([-eq, -xi, yi])
            same = F.var()
            F.add([-same, -xi, yi])
            F.add([-same, xi, -yi])
            F.add([same, xi, yi])
            F.add([same, -xi, -yi])
            eq = same if eq is True else F.AND(eq, same)
        count += 1
    return F, a, e, n, count


if __name__ == "__main__":
    v, k, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    prefix = int(sys.argv[4]) if len(sys.argv) > 4 else 600
    assert k * (k - 2) == 2 * (v - k - 1)
    F, a, e, n, count = build_sb(v, k, out, prefix)
    F.finish()
    meta = {"v": v, "k": k, "mu": 2, "n": n, "a": a, "e": {"%d,%d" % key: val for key, val in e.items() if key[0] < key[1]}}
    json.dump(meta, open(out + ".meta.json", "w"))
    print("srg(%d,%d,1,2) with W(B%d) lex-leader constraints for %d group elements (prefix %d): %d variables, %d clauses"
          % (v, k, k // 2, count, prefix, F.n, F.m), flush=True)
