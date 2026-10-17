"""Linear Gram test for root templates (exploration, LAB 17/10/2026).
For a template, the vectors v_e (e in E(J)) satisfy the node relations; with a basis b_e (columns, k = dim ker C) of the
scalar solution space, v_e = Q^{1/2} b_e for a k x k PSD matrix Q, R_ef = b_e^t Q b_f.  Exact constraints that are
LINEAR in Q: R_ef = 0 for two links at one root in different blocks (fact (O)).  Let S = {symmetric Q satisfying them}.
If S = 0 the template is impossible.  We report dim S, and for dim S = 1 whether the unique ray has a PSD
representative with R_ee > 0 on every link and R_ef <= 0 inside each block (facts (S)).
usage: python cle3_qspace.py <templates.json> [max]"""
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations

import sympy as sp


def kernel_basis(nodes, links):
    """basis of {w in Q^links : sum_{links at node} w = 0}; returns list of columns b_e (tuples) for each link."""
    M = sp.zeros(len(nodes), len(links))
    for k, (a, b) in enumerate(links):
        M[a, k] += 1
        M[b, k] += 1
    ns = M.nullspace()
    if not ns:
        return 0, []
    Bm = sp.Matrix.hstack(*ns)          # links x k
    return Bm.shape[1], [Bm.row(e) for e in range(len(links))]


def analyse(t):
    edges = [tuple(e) for e in t["nongrid_edges"]]
    groups = t["nontrivial_component_groups"]
    nodes, lookup = [], {}
    for r, parts in enumerate(groups):
        for part in parts:
            nd = len(nodes)
            nodes.append((r, tuple(part)))
            for j in part:
                lookup[(r, j)] = nd
    links = [(lookup[(a, b)], lookup[(b, a)]) for a, b in edges]
    eidx = {}
    for k, (a, b) in enumerate(edges):
        eidx[(a, b)] = eidx[(b, a)] = k
    k, bs = kernel_basis(nodes, links)
    pairs_orth, pairs_block = [], []
    for r, parts in enumerate(groups):
        for p1, p2 in combinations(range(len(parts)), 2):
            for j in parts[p1]:
                for jj in parts[p2]:
                    pairs_orth.append((eidx[(r, j)], eidx[(r, jj)]))
        for part in parts:
            for j, jj in combinations(part, 2):
                pairs_block.append((eidx[(r, j)], eidx[(r, jj)]))
    # unknown symmetric Q: entries q_st, s <= t
    idx = [(s, u) for s in range(k) for u in range(s, k)]
    rows = []
    for e, f in pairs_orth:
        be, bf = bs[e], bs[f]
        row = []
        for s, u in idx:
            c = be[s] * bf[u] + (be[u] * bf[s] if s != u else 0)
            row.append(c)
        rows.append(row)
    if rows:
        A = sp.Matrix(rows)
        sol = A.nullspace()
    else:
        sol = [sp.Matrix([1 if i == j else 0 for j in range(len(idx))]) for i in range(len(idx))]
    dimS = len(sol)
    out = {"k": k, "dimS": dimS}
    if dimS == 1:
        q = sol[0]
        Q = sp.zeros(k, k)
        for (s, u), val in zip(idx, q):
            Q[s, u] = Q[u, s] = val
        for sign in (1, -1):
            Qs = sign * Q
            R = lambda e, f: (bs[e] * Qs * bs[f].T)[0, 0]
            ok = all(R(e, e) > 0 for e in range(len(edges))) and all(R(e, f) <= 0 for e, f in pairs_block)
            if ok:
                ev = [complex(x).real for x in Qs.eigenvals(multiple=True)] if k <= 4 else None
                psd = Qs.is_positive_semidefinite
                out["ray_ok"] = bool(psd)
                out["diag"] = sorted(set(str(R(e, e)) for e in range(len(edges))))
                break
        else:
            out["ray_ok"] = False
    return out


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
    agg = Counter()
    for t in data["survivors"][:mx]:
        r = analyse(t)
        key = (r["k"], r["dimS"], r.get("ray_ok"))
        agg[key] += 1
    print("(k = dim ker C, dim S, unique-ray feasible?) : count")
    for key, v in sorted(agg.items(), key=lambda x: (x[0][0], x[0][1], str(x[0][2]))):
        print("  ", key, v)
