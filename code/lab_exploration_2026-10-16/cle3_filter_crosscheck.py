"""Independent cross-check of the template filters of cle3_templates.py / cle_templates.cpp (LAB, 18/10/2026).

For every J-graph with 21 - k edges (graph list = cle3_templates.graph_reps(), whose total 588 is OEIS A004110(7), graphs
on 7 nodes without a node of degree 1) and every choice of component partitions (blocks of size >= 2, all c_r >= c_min),
the rejection rules are re-derived by EXACT LINEAR ALGEBRA on C (component nodes x non-grid rectangles), not by the
signed union-find of the enumerators.  The realisation vectors satisfy V C^t = 0, so every row of V lies in ker C:
  Z : e_e in rowspace(C)                -> v_e = 0, but R_ee >= 4 on a non-grid rectangle;
  EQ: e_e -+ e_f in rowspace(C), e and f at one root r  -> v_e = +-v_f in every realisation:
        different blocks of r          -> R_ef = +-R_ee != 0, but R_ef = 0 across components of one line;
        same block of size >= 3        -> '+': R_ef = R_ee > 0, but R_ef <= 0 on a shared line;
                                          '-': the cut {e, f} of the block has weight (v_e + v_f).(...) = 0 > -2;
  K : dim ker C < max_r (6 - c_r).
The linear algebra sees every forced +-equality, so it can only reject MORE than the union-find.  The survivors are
canonicalised under Aut(J) (brute force, own code) and compared with the C++ jsonl survivor lists.
usage: python cle3_filter_crosscheck.py <c_min> <k> <cpp survivors .jsonl> [--exact]"""
import json
import sys
import time
from fractions import Fraction
from itertools import combinations, permutations

import cle3_templates as CT          # only graph_reps() and EDGES are taken from here

EDGES = list(combinations(range(7), 2))
assert EDGES == list(CT.EDGES)


def set_partitions_min2(items):
    """All partitions of items into blocks of size >= 2 (own generator)."""
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for size in range(1, len(rest) + 1):
        for mates in combinations(rest, size):
            left = [x for x in rest if x not in mates]
            for tail in set_partitions_min2(left):
                yield [(first,) + mates] + tail


def rref_rows(rows, ncols):
    """Exact RREF (list of (pivot, row)) of integer rows."""
    basis = []
    for r in rows:
        v = [Fraction(x) for x in r]
        for p, b in basis:
            if v[p]:
                c = v[p]
                v = [x - c * y for x, y in zip(v, b)]
        piv = next((i for i in range(ncols) if v[i]), None)
        if piv is None:
            continue
        c = v[piv]
        v = [x / c for x in v]
        new = []
        for p, b in basis:
            if b[piv]:
                cb = b[piv]
                b = [x - cb * y for x, y in zip(b, v)]
            new.append((p, b))
        basis = new + [(piv, v)]
    return basis


def in_rowspace(basis, u):
    v = [Fraction(x) for x in u]
    for p, b in basis:
        if v[p]:
            c = v[p]
            v = [x - c * y for x, y in zip(v, b)]
    return not any(v)


def verdict(nongrid, parts, cmin, exact):
    """parts[r] = list of blocks (tuples of other roots) of root r; returns None (survives) or a reason."""
    c = [(6 - sum(len(B) for B in parts[r])) + len(parts[r]) for r in range(7)]
    if min(c) < cmin or (exact and min(c) != cmin):
        return "c"
    m = len(nongrid)
    eidx = {e: i for i, e in enumerate(nongrid)}
    nodes = [(r, B) for r in range(7) for B in parts[r]]
    rows = []
    for r, B in nodes:
        row = [0] * m
        for j in B:
            row[eidx[tuple(sorted((r, j)))]] = 1
        rows.append(row)
    basis = rref_rows(rows, m)
    dimker = m - len(basis)
    for i in range(m):
        u = [0] * m
        u[i] = 1
        if in_rowspace(basis, u):
            return "Z"
    for r in range(7):
        links = [(j, bi) for bi, B in enumerate(parts[r]) for j in B]
        for (j1, b1), (j2, b2) in combinations(links, 2):
            e, f = eidx[tuple(sorted((r, j1)))], eidx[tuple(sorted((r, j2)))]
            for sign in (1, -1):
                u = [0] * m
                u[e], u[f] = 1, -sign
                if in_rowspace(basis, u):
                    if b1 != b2:
                        return "EQ-two-blocks"
                    if len(parts[r][b1]) >= 3:
                        return "EQ-big-block"
    if dimker < max(6 - x for x in c):
        return "K"
    return None


def automorphisms(mask):
    adj = {e for k, e in enumerate(EDGES) if mask >> k & 1}
    out = []
    for p in permutations(range(7)):
        if all(tuple(sorted((p[a], p[b]))) in adj for a, b in adj):
            out.append(p)
    return out


def key(parts, perm):
    img = [None] * 7
    for r in range(7):
        img[perm[r]] = tuple(sorted(tuple(sorted(perm[j] for j in B)) for B in parts[r]))
    return tuple(img)


def canonical(parts, auts):
    return min(key(parts, p) for p in auts)


def main():
    cmin, k, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    exact = "--exact" in sys.argv
    t0 = time.time()
    reps = [g for g in CT.graph_reps() if bin(g).count("1") == 21 - k]
    t1 = time.time()
    mine, reasons, labelled = set(), {}, 0
    for g in reps:
        nongrid = [e for kk, e in enumerate(EDGES) if g >> kk & 1]
        nbrs = [[j for j in range(7) if j != r and tuple(sorted((r, j))) in set(nongrid)] for r in range(7)]
        auts = automorphisms(g)
        options = [list(set_partitions_min2(nbrs[r])) for r in range(7)]

        def rec(r, chosen):
            nonlocal labelled
            if r == 7:
                labelled += 1
                why = verdict(nongrid, chosen, cmin, exact)
                if why is None:
                    mine.add((g, canonical(chosen, auts)))
                else:
                    reasons[why] = reasons.get(why, 0) + 1
                return
            for opt in options[r]:
                rec(r + 1, chosen + [opt])
        rec(0, [])
    cpp = set()
    for line in open(path):
        t = json.loads(line)
        g = t["graph_mask"]
        parts = [[tuple(B) for B in blocks] for blocks in t["nontrivial_component_groups"]]
        cpp.add((g, canonical(parts, automorphisms(g))))
    report = {"c_min": cmin, "k": k, "exact": exact, "graphs": len(reps), "labelled_templates": labelled,
              "rejections": reasons, "survivors_linear_algebra": len(mine), "survivors_cpp": len(cpp),
              "only_cpp": len(cpp - mine), "only_linear_algebra": len(mine - cpp), "identical": mine == cpp,
              "seconds": round(time.time() - t0, 1), "graph_reps_seconds": round(t1 - t0, 1)}
    print(json.dumps(report))
    if cpp - mine:
        print("ONLY CPP (C++ keeps, linear algebra rejects):", sorted(cpp - mine)[:5])
    if mine - cpp:
        print("ONLY LINEAR ALGEBRA (C++ rejects, linear algebra keeps -> FALSE REJECTION):", sorted(mine - cpp)[:5])


if __name__ == "__main__":
    main()
