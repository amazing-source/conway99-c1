"""One-rectangle moment tests in the block-graph form of the rows (LAB, 18/10/2026).  Measurement tool.

Rows h_w as in jhat_rows.py.  For a non-grid target q = {a, b} with e = e(q) in {0, 1, 2} (E3):
  corners u of q: h_u(q) = 2 - o_u, own counts o_u with the histogram of a corner graph with e edges;
  labels sharing one line with q:  sum of h_w(q) = -(16 - 4e);
  labels disjoint from q:          sum of h_w(q) =   8 - 2e;
  all labels:                      sum of h_w(q)^2 = 7 R_qq = 7 (8 - 2e)   (column q of H^T H = 7R).
These are the identities of Codex's check_rectangle (root_component_z_distribution.py) written with h = base - z.
Level M1 ("projection"): every label w of class G takes h_w(q) in the exact projection V_G(q) of the rows of G.
Level M2 ("symmetry"):   in addition, for every class G != q, sum_{w in G} h_w(q) = R_Gq = R_qG = sum_{u in q} h_u(G),
                         with the four corner rows of q chosen among the rows of class q (CP-SAT model).
Projections are exact: one CP-SAT feasibility test per value (bounds kept in Python, see feedback-cp-positive-control).
usage: python jhat_moment.py <catalogue> <first> <last> [--m2] [--only-survivors FG.jsonl]"""
import json
import sys
from itertools import combinations

from ortools.sat.python import cp_model

from jhat_rows import RECT, block_graph, box, forced_grid_walk, records   # noqa: E402

HIST = {0: [(0, 0, 0, 0)], 1: [(0, 0, 1, 1)], 2: [(1, 1, 1, 1), (0, 1, 1, 2)]}   # sorted own counts o_u


def row_model(m, graph, q, name):
    edges, ends, at = graph
    h = {}
    for e in edges:
        lo, hi = box(q, e)
        h[e] = m.NewIntVar(lo, hi, "%s_%d%d" % ((name,) + e))
    for es in at.values():
        m.Add(sum(h[e] for e in es) == 0)
    return h


def feasible(graph, q, fixed, seconds=5.0):
    m = cp_model.CpModel()
    h = row_model(m, graph, q, "r")
    for e, v in fixed.items():
        if e in h:
            m.Add(h[e] == v)
        elif v != 0:
            return False
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1
    r = s.Solve(m)
    if r == cp_model.UNKNOWN:
        raise RuntimeError("projection test undecided")
    return r in (cp_model.OPTIMAL, cp_model.FEASIBLE)


def projection(graph, G, q):
    """Exact set of values h(q) over the rows of class G (q an edge of the block graph)."""
    lo, hi = box(G, q)
    return [v for v in range(lo, hi + 1) if feasible(graph, G, {q: v})]


def attainable(domains):
    st = {(0, 0)}
    for d in domains:
        st = {(s + v, c + v * v) for s, c in st for v in d}
    return st


def m1(graph, q, proj):
    """True if the projection-level moment system of target q has a solution."""
    shared = [proj[G] for G in RECT if G != q and set(G) & set(q) for _ in range(4)]
    disjoint = [proj[G] for G in RECT if not set(G) & set(q) for _ in range(4)]
    sh, dj = attainable(shared), attainable(disjoint)
    for e, hs in HIST.items():
        for o in hs:
            if not all((2 - x) in proj[q] for x in o):
                continue
            corner_sq = sum((2 - x) ** 2 for x in o)
            need = 7 * (8 - 2 * e) - corner_sq
            s_sq = {c for s, c in sh if s == -(16 - 4 * e)}
            d_sq = {c for s, c in dj if s == 8 - 2 * e}
            if any(need - c in d_sq for c in s_sq):
                return True
    return False


def m2(graph, q, proj, seconds=20.0):
    """Symmetry level: corner rows explicit; returns True (feasible), False (infeasible) or None (unknown)."""
    edges, ends, at = graph
    m = cp_model.CpModel()
    corners = [row_model(m, graph, q, "u%d" % i) for i in range(4)]
    o = [m.NewIntVar(0, 2, "o%d" % i) for i in range(4)]
    for i in range(4):
        m.Add(o[i] == 2 - corners[i][q])
    for i in range(3):
        m.Add(o[i] <= o[i + 1])
    # corner histogram: allowed sorted tuples
    m.AddAllowedAssignments(o, [t for hs in HIST.values() for t in hs])
    esum = sum(o)                                   # = 2e
    sq_terms = []
    total_sq = []
    for i in range(4):
        hq = corners[i][q]
        sqv = m.NewIntVar(0, 4, "csq%d" % i)
        m.AddMultiplicationEquality(sqv, [hq, hq])
        total_sq.append(sqv)
    shared_sum, disjoint_sum = [], []
    for G in RECT:
        if G == q:
            continue
        vals = proj[G]
        ws = []
        for i in range(4):
            w = m.NewIntVarFromDomain(cp_model.Domain.FromValues(vals), "t%d%d_%d" % (G + (i,)))
            ws.append(w)
            sqv = m.NewIntVarFromDomain(cp_model.Domain.FromValues(sorted({v * v for v in vals})), "s%d%d_%d" % (G + (i,)))
            m.AddMultiplicationEquality(sqv, [w, w])
            total_sq.append(sqv)
        for i in range(3):
            m.Add(ws[i] <= ws[i + 1])
        # symmetry R_Gq = R_qG
        rq = sum(c[G] for c in corners) if G in corners[0] else 0
        m.Add(sum(ws) == rq)
        (shared_sum if set(G) & set(q) else disjoint_sum).extend(ws)
    # sums and diagonal, with 2e = esum
    m.Add(sum(shared_sum) == -16 + 2 * esum)
    m.Add(sum(disjoint_sum) == 8 - esum)
    m.Add(sum(total_sq) == 56 - 7 * esum)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1
    r = s.Solve(m)
    if r == cp_model.INFEASIBLE:
        return False
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return True
    return None


if __name__ == "__main__":
    path, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    do_m2 = "--m2" in sys.argv
    for idx, t in enumerate(records(path)):
        if idx < first:
            continue
        if idx >= last:
            break
        graph = block_graph(t)
        edges = graph[0]
        out = {"index": idx, "k": 21 - len(edges), "dim": t.get("kernel_dimension"),
               "fg": [q for q in edges if forced_grid_walk(t, q, graph)]}
        if not out["fg"]:
            m1_dead, m2_dead, m2_unknown = [], [], []
            for q in edges:
                proj = {G: projection(graph, G, q) for G in RECT}
                if not m1(graph, q, proj):
                    m1_dead.append(q)
                    continue
                if do_m2:
                    r = m2(graph, q, proj)
                    if r is False:
                        m2_dead.append(q)
                    elif r is None:
                        m2_unknown.append(q)
            out.update(m1=m1_dead, m2=m2_dead, m2_unknown=m2_unknown)
        print(json.dumps(out), flush=True)
