"""Moment test of one rectangle Gram R, written from scratch (LAB, 18/10/2026), independent of Codex's code.

Setting (audit 18/10, section 3): T is the 84 x 84 matrix on the labels, T >= 0 and T^2 = 7T; P has one column 1_Q
per rectangle (its 4 corners); R = P^T T P on the m non-grid rectangles.  Put H = T P (84 x m), row h_w for a label w.
  (M)  H^T H = P^T T^2 P = 7 R, i.e. sum over the 84 labels of h_w h_w^T = 7 R          (exact);
  h_{w,f} = base - |N(w) cap Q_f|, base = 2 (w in Q_f), 0 (Q_f shares one root line with the rectangle of w), 1 (else);
  coordinate bounds: [0,2], [-2,0], [-3,1] respectively (lambda = 1, mu = 2 at the letters, see the note);
  Schur: the Gram of {e_w : w in Q} and the m vectors 1_Q' under T is PSD, so h_w in im R, h_w^T R^+ h_w <= 5/2
  (T_ww = 5/2) and T_QQ - H_Q R^+ H_Q^T >= 0, with T_QQ = 5/2 on the diagonal, -adj - 1/4 for two corners sharing a
  letter, -adj for opposite corners; corner graph: e(Q) = (8 - R_QQ)/2 edges (4 for a grid rectangle), a corner is
  adjacent to at most one corner containing a given mate letter (mu(w, a*) = 2 at the letter a*);
  column sums: sum over w in Q of h_w = R e_Q (non-grid Q), = 0 (grid Q, T 1_Q = 0 since 1_Q is a component vector).
Per rectangle, every realization (corner graph, four signatures) passing all of this is enumerated, with its moment
M_Q = sum_{w in Q} h_w h_w^T.  Then (M) needs sum_Q M_Q = 7R:
  bounds test : for some pair (e, f), sum_Q min_Q <= 7 R_ef <= sum_Q max_Q fails  -> R impossible (certificate);
  design test : no choice of one realization per rectangle has sum_Q M_Q = 7 R exactly (CP-SAT, small) -> impossible.
usage: python moment_bounds.py <cover json(.gz)> [gram numbers ...] [--design SECONDS]"""
import gzip
import json
import sys
import time
from fractions import Fraction
from itertools import combinations, product

import sympy as sp

LINES = tuple(combinations(range(7), 2))          # the 21 rectangles = pairs of root lines
CORNERS = ((0, 2), (0, 3), (1, 2), (1, 3))       # letters: 0, 1 = the two letters of line i; 2, 3 = of line j
PAIRS6 = [(a, b) for a in range(4) for b in range(a + 1, 4)]


def share_letter(a, b):
    return bool(set(CORNERS[a]) & set(CORNERS[b]))


def corner_graphs(edge_count):
    """Edge sets on the 4 corners with edge_count edges, a corner adjacent to at most one corner of each letter."""
    out = []
    for es in combinations(PAIRS6, edge_count):
        adj = [[0] * 4 for _ in range(4)]
        for a, b in es:
            adj[a][b] = adj[b][a] = 1
        ok = True
        for w in range(4):
            for letter in range(4):
                if letter in CORNERS[w]:
                    continue
                if sum(adj[w][u] for u in range(4) if letter in CORNERS[u]) > 1:
                    ok = False
        if ok:
            out.append(adj)
    return out


def psd(a):
    a = [row[:] for row in a]
    while a:
        p = a[0][0]
        if p < 0 or (p == 0 and any(a[0][1:])):
            return False
        if p == 0:
            a = [row[1:] for row in a[1:]]
        else:
            a = [[a[i][j] - a[i][0] * a[0][j] / p for j in range(1, len(a))] for i in range(1, len(a))]
    return True


def analyse(edges, R, design_seconds=0.0):
    m = len(edges)
    M = sp.Matrix(R)
    A = list(M.rref()[1])                          # pivot columns: R = R[:, A] X^-1 R[A, :]
    X = M.extract(A, A)
    Xi = [[Fraction(int(sp.fraction(v)[0]), int(sp.fraction(v)[1])) for v in row] for row in X.inv().tolist()]
    RA = [[Fraction(R[i][a]) for a in A] for i in range(m)]
    lift = [[sum(RA[i][k] * Xi[k][l] for k in range(len(A))) for l in range(len(A))] for i in range(m)]
    real = {}
    for Q in LINES:
        q = edges.index(Q) if Q in edges else None
        lo_hi = [(0, 2) if Q == f else ((-2, 0) if set(Q) & set(f) else (-3, 1)) for f in edges]
        dom = []
        for z in product(*(range(lo_hi[a][0], lo_hi[a][1] + 1) for a in A)):
            zf = [Fraction(v) for v in z]
            if 2 * sum(zf[k] * Xi[k][l] * zf[l] for k in range(len(A)) for l in range(len(A))) > 5:
                continue
            h = [sum(lift[i][l] * zf[l] for l in range(len(A))) for i in range(m)]
            if any(x.denominator != 1 for x in h):
                continue
            h = tuple(int(x) for x in h)
            if all(lo <= x <= hi for x, (lo, hi) in zip(h, lo_hi)):
                dom.append(h)
        target = tuple(R[i][q] for i in range(m)) if q is not None else (0,) * m
        e_Q = (8 - R[q][q]) // 2 if q is not None else 4
        moments = {}
        for adj in corner_graphs(e_Q):
            need = [2 - sum(adj[w]) for w in range(4)]
            cand = [[h for h in dom if q is None or h[q] == need[w]] for w in range(4)]
            half = {}
            for h3, h4 in product(cand[2], cand[3]):
                half.setdefault(tuple(a + b for a, b in zip(h3, h4)), []).append((h3, h4))
            T4 = [[Fraction(5, 2) if a == b else Fraction(-adj[a][b]) - (Fraction(1, 4) if share_letter(a, b) else 0)
                   for b in range(4)] for a in range(4)]
            for h1, h2 in product(cand[0], cand[1]):
                rest = tuple(t - a - b for t, a, b in zip(target, h1, h2))
                for h3, h4 in half.get(rest, []):
                    Hs = (h1, h2, h3, h4)
                    HA = [[Fraction(h[a]) for a in A] for h in Hs]
                    S = [[T4[a][b] - sum(HA[a][k] * Xi[k][l] * HA[b][l] for k in range(len(A)) for l in range(len(A)))
                          for b in range(4)] for a in range(4)]
                    if not psd(S):
                        continue
                    mom = tuple(sum(h[e] * h[f] for h in Hs) for e in range(m) for f in range(e, m))
                    moments[mom] = moments.get(mom, 0) + 1
        real[Q] = moments
        if not moments:
            return {"status": "EXCLUDED", "reason": "no corner realization", "rectangle": Q}
    pairs = [(e, f) for e in range(m) for f in range(e, m)]
    for idx, (e, f) in enumerate(pairs):
        lo = sum(min(mom[idx] for mom in real[Q]) for Q in LINES)
        hi = sum(max(mom[idx] for mom in real[Q]) for Q in LINES)
        if not lo <= 7 * R[e][f] <= hi:
            return {"status": "EXCLUDED", "reason": "moment bounds", "pair": [list(edges[e]), list(edges[f])],
                    "target_7R": 7 * R[e][f], "sum_min": lo, "sum_max": hi,
                    "per_rectangle_max": [max(mom[idx] for mom in real[Q]) for Q in LINES],
                    "per_rectangle_min": [min(mom[idx] for mom in real[Q]) for Q in LINES]}
    res = {"status": "PASSES_BOUNDS", "realizations": {"%d%d" % Q: len(real[Q]) for Q in LINES}}
    if design_seconds > 0:
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        choice = {}
        for Q in LINES:
            choice[Q] = [model.new_bool_var("c") for _ in real[Q]]
            model.add_exactly_one(choice[Q])
        for idx, (e, f) in enumerate(pairs):
            model.add(sum(mom[idx] * v for Q in LINES for mom, v in zip(real[Q], choice[Q])) == 7 * R[e][f])
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = 1
        solver.parameters.max_time_in_seconds = design_seconds
        st = solver.solve(model)
        res["design"] = solver.status_name(st)
        if st == cp_model.INFEASIBLE:
            res["status"] = "EXCLUDED"
            res["reason"] = "no moment design"
    return res


if __name__ == "__main__":
    args = sys.argv[1:]
    design = 0.0
    if "--design" in args:
        i = args.index("--design")
        design = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    path, picks = args[0], [int(x) for x in args[1:]]
    cover = json.load(gzip.open(path, "rt") if path.endswith(".gz") else open(path))
    edges = [tuple(e) for e in cover["edges"]]
    for k in picks or range(len(cover["grams"])):
        t0 = time.time()
        r = analyse(edges, cover["grams"][k], design)
        r.update(gram=k, seconds=round(time.time() - t0, 1))
        print(json.dumps(r), flush=True)
