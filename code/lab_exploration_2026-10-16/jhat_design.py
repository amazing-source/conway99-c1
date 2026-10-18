"""Global count designs in the block-graph form of the rows (LAB, 18/10/2026).  Measurement tool (CP-SAT verdicts).

Unknowns: for every one of the 21 rectangle classes F, the rows h_{F,0..3} of its four labels (jhat_rows.py: integer
zero-sum weightings of the block graph Jh, in the box of F).  R_FG := sum_i h_{F,i}(G) (= R of the Gram matrix; it is
0 when G is a grid, because then h(G) = 0).
Level R1 (first order, no products):
  symmetry      R_FG = R_GF for all classes F != G            (R = P^T T P is symmetric; Codex's block_symmetry);
  E3 and corners for a non-grid F: own counts o_i = 2 - h_{F,i}(F) form the degree multiset of a corner graph with
                e(F) <= 2 edges: sorted (0,0,0,0), (0,0,1,1), (1,1,1,1) or (0,1,1,2)   (so R_FF = 8 - 2e >= 4).
Level R1D: R1 + diagonal moments  sum_w h_w(F)^2 = 7 R_FF for every non-grid F   (diagonal of H^T H = 7R).
Level R2:  R1 + all moments  sum_w h_w(F) h_w(G) = 7 R_FG for all F, G             (H^T H = 7R = 7 P^T H).
Also, for every F, sum_w h_w(F) = 0 (1^T H = 0) is added at all levels.
Bounds are kept in Python (OR-Tools 9.15 domain[-1] pitfall).
usage: python jhat_design.py <catalogue> <first> <last> [--level R1|R1D|R2] [--seconds S] [--only i,j,...]"""
import json
import sys
from itertools import combinations

from ortools.sat.python import cp_model

from jhat_rows import RECT, block_graph, box, records

ALLOWED = [(0, 0, 0, 0), (0, 0, 1, 1), (1, 1, 1, 1), (0, 1, 1, 2)]


def design(t, level="R1", seconds=30.0):
    graph = block_graph(t)
    edges, ends, at = graph
    E = set(edges)
    m = cp_model.CpModel()
    H = {}
    for F in RECT:
        for i in range(4):
            for e in edges:
                lo, hi = box(F, e)
                H[F, i, e] = m.NewIntVar(lo, hi, "h_%d%d_%d_%d%d" % (F + (i,) + e))
            for es in at.values():
                m.Add(sum(H[F, i, e] for e in es) == 0)

    def hv(F, i, G):
        return H[F, i, G] if G in E else 0

    for F, G in combinations(RECT, 2):
        a = sum(hv(F, i, G) for i in range(4))
        b = sum(hv(G, i, F) for i in range(4))
        if not (isinstance(a, int) and isinstance(b, int)):
            m.Add(a == b)
    for F in edges:
        o = [m.NewIntVar(0, 2, "o_%d%d_%d" % (F + (i,))) for i in range(4)]
        for i in range(4):
            m.Add(o[i] == 2 - H[F, i, F])
        for i in range(3):
            m.Add(o[i] <= o[i + 1])
        m.AddAllowedAssignments(o, ALLOWED)
    for G in edges:
        m.Add(sum(H[F, i, G] for F in RECT for i in range(4)) == 0)
    sq = {}
    if level in ("R1D", "R2"):
        for F in RECT:
            for i in range(4):
                for G in edges:
                    lo, hi = box(F, G)
                    v = m.NewIntVar(0, max(lo * lo, hi * hi), "sq_%d%d_%d_%d%d" % (F + (i,) + G))
                    m.AddMultiplicationEquality(v, [H[F, i, G], H[F, i, G]])
                    sq[F, i, G] = v
        for G in edges:
            m.Add(sum(sq[F, i, G] for F in RECT for i in range(4)) == 7 * sum(H[G, i, G] for i in range(4)))
    if level == "R2":
        for G1, G2 in combinations(edges, 2):
            prods = []
            for F in RECT:
                for i in range(4):
                    l1, h1 = box(F, G1)
                    l2, h2 = box(F, G2)
                    c = [l1 * l2, l1 * h2, h1 * l2, h1 * h2]
                    p = m.NewIntVar(min(c), max(c), "p_%d%d_%d_%d%d_%d%d" % (F + (i,) + G1 + G2))
                    m.AddMultiplicationEquality(p, [H[F, i, G1], H[F, i, G2]])
                    prods.append(p)
            m.Add(sum(prods) == 7 * sum(H[G1, i, G2] for i in range(4)))
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1
    r = s.Solve(m)
    if r == cp_model.INFEASIBLE:
        return "INFEASIBLE", s.WallTime()
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        # independent check of the witness (first-order part)
        val = {k: s.Value(v) for k, v in H.items()}
        for F, G in combinations(RECT, 2):
            a = sum(val[F, i, G] for i in range(4)) if G in E else 0
            b = sum(val[G, i, F] for i in range(4)) if F in E else 0
            assert a == b, (F, G)
        return "FEASIBLE", s.WallTime()
    return "UNKNOWN", s.WallTime()


if __name__ == "__main__":
    path, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    level = sys.argv[sys.argv.index("--level") + 1] if "--level" in sys.argv else "R1"
    seconds = float(sys.argv[sys.argv.index("--seconds") + 1]) if "--seconds" in sys.argv else 30.0
    only = None
    if "--only" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    for idx, t in enumerate(records(path)):
        if idx < first or (only is not None and idx not in only):
            continue
        if idx >= last:
            break
        st, wall = design(t, level, seconds)
        print(json.dumps({"index": idx, "k": 21 - len(t["nongrid_edges"]), "dim": t.get("kernel_dimension"),
                          "level": level, "status": st, "wall": round(wall, 2)}), flush=True)
