"""Rows of a root template as zero-sum weightings of its block graph (LAB, 18/10/2026).

Facts used (all in AUDIT_EXCLUSIONS_2026-10-18.md, items 1-7):
  H = TP, h_w(F) = base(w, F) - z_w(F), base = 2 (own rectangle), 0 (one shared line), 1 (disjoint);
  T sigma = 0 on every component (item 5): for every root r and block P at r, sum_{j in P} h_w(Q_rj) = 0;
  a grid rectangle F has R_FF = 0, so h_w(F) = 0 for every label w;
  bounds 0 <= z <= 2 (F meets the rectangle of w), 0 <= z <= 4 (F disjoint).
Block graph Jh: one vertex (r, P) per block P of size >= 2 at root r; one edge per non-grid rectangle {r, s}, joining
(r, block of s at r) and (s, block of r at s).  So a row h_w is an integer vector on the edges of Jh, with sum zero at
every vertex of Jh, and with the box of its rectangle q = {a, b}:
  h(q) in [0, 2];  h(e) in [-2, 0] for e != q meeting q;  h(e) in [-3, 1] for e disjoint from q.
For a grid label (q grid) the same box applies; q itself is not an edge of Jh.

FORCED GRID (for a non-grid q = {a, b}).  If no row of a corner of q has h(q) >= 1, every corner has own count 2, so
e(q) = 4 and q is a grid: contradiction.  A row with h(q) >= 1 splits into closed walks of Jh that alternate the signs
of their edges (pair the positive and negative units at each vertex of Jh); one of them uses q positively.  Positive
edges are q or edges disjoint from q; negative edges are edges meeting q (and disjoint ones).  So:
  forced_grid_walk : no alternating closed walk through q exists (sound sufficient condition, multiplicities ignored);
  forced_grid_ilp  : no integer row with h(q) >= 1 exists (exact, CP-SAT; measurement only).
usage: python jhat_rows.py <catalogue (.json/.json.gz with open/survivors/templates, or census .jsonl.gz)> [first last]
       [--ilp]   prints one JSON line per template"""
import gzip
import json
import sys
from collections import deque
from itertools import combinations

RECT = list(combinations(range(7), 2))


def blocks_of(t):
    """bl[r][j] = index of the block of j at root r (None if {r, j} is a grid)."""
    bl = [[None] * 7 for _ in range(7)]
    for r, groups in enumerate(t["nontrivial_component_groups"]):
        for i, part in enumerate(groups):
            for j in part:
                bl[r][j] = i
    return bl


def block_graph(t):
    bl = blocks_of(t)
    edges = [tuple(e) for e in t["nongrid_edges"]]
    for r, s in edges:
        assert bl[r][s] is not None and bl[s][r] is not None, "non-grid edge without blocks"
    ends = {e: ((e[0], bl[e[0]][e[1]]), (e[1], bl[e[1]][e[0]])) for e in edges}
    at = {}
    for e, (x, y) in ends.items():
        at.setdefault(x, []).append(e)
        at.setdefault(y, []).append(e)
    return edges, ends, at


def box(q, e):
    if e == q:
        return 0, 2
    if set(e) & set(q):
        return -2, 0
    return -3, 1


def forced_grid_walk(t, q, graph=None):
    """True if no alternating closed walk of Jh uses q positively (then the template is impossible)."""
    edges, ends, at = graph or block_graph(t)
    if q not in ends:
        return False
    a_end, b_end = ends[q]
    allowed = {e: tuple(s for s in (1, -1) if (box(q, e)[1] if s > 0 else -box(q, e)[0]) > 0) for e in edges}
    start, goal = (b_end, 1), (a_end, -1)        # traversed q from a to b; must come back to a by a negative edge
    seen = {start}
    todo = deque([start])
    while todo:
        x, s_in = todo.popleft()
        for e in at[x]:
            s = -s_in
            if s not in allowed[e]:
                continue
            u, v = ends[e]
            y = v if u == x else u
            if u == v:                              # loop at one block (cannot happen: r != s)
                continue
            st = (y, s)
            if st == goal:
                return False
            if st not in seen:
                seen.add(st)
                todo.append(st)
    return True


def forced_grid_ilp(t, q, graph=None, seconds=10.0):
    """Exact test: does an integer row of a corner of q with h(q) >= 1 exist?  Returns 'FORCED', 'NOT_FORCED' or
    'UNKNOWN'.  Bounds are kept in Python (OR-Tools 9.15 domain[-1] pitfall)."""
    from ortools.sat.python import cp_model
    edges, ends, at = graph or block_graph(t)
    m = cp_model.CpModel()
    h = {}
    for e in edges:
        lo, hi = box(q, e)
        if e == q:
            lo = 1
        h[e] = m.NewIntVar(lo, hi, "h%d%d" % e)
    for x, es in at.items():
        m.Add(sum(h[e] for e in es) == 0)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = seconds
    s.parameters.num_workers = 1
    r = s.Solve(m)
    if r == cp_model.INFEASIBLE:
        return "FORCED"
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        row = {e: s.Value(h[e]) for e in edges}
        # independent check of the witness
        assert all(box(q, e)[0] <= v <= box(q, e)[1] for e, v in row.items()) and row[q] >= 1
        assert all(sum(row[e] for e in es) == 0 for es in at.values())
        return "NOT_FORCED"
    return "UNKNOWN"


def records(path):
    if path.endswith(".keys.gz") or path.endswith(".sorted.gz"):
        from jhat_fg_keys import decode          # S7 keys of compare_census_aws.py, one template per line
        with gzip.open(path, "rt") as fh:
            for line in fh:
                if line.strip():
                    t, _ = decode(line)
                    t["key"] = line.strip()
                    yield t
        return
    if path.endswith(".jsonl.gz") or path.endswith(".jsonl"):
        op = gzip.open if path.endswith(".gz") else open
        with op(path, "rt") as fh:
            for line in fh:
                if line.strip():
                    yield json.loads(line)
        return
    raw = open(path, "rb").read()
    doc = json.loads(gzip.decompress(raw) if path.endswith(".gz") else raw)
    for rec in doc.get("open") or doc.get("survivors") or doc.get("templates"):
        yield rec.get("template", rec)


if __name__ == "__main__":
    path = sys.argv[1]
    nums = [int(x) for x in sys.argv[2:] if x.lstrip("-").isdigit()]
    first, last = (nums + [0, 10 ** 12])[:2]
    use_ilp = "--ilp" in sys.argv
    for idx, t in enumerate(records(path)):
        if idx < first:
            continue
        if idx >= last:
            break
        graph = block_graph(t)
        walk = [q for q in graph[0] if forced_grid_walk(t, q, graph)]
        out = {"index": idx, "k": 21 - len(t["nongrid_edges"]), "c": t["component_count_by_root_line"],
               "dim": t.get("kernel_dimension"), "forced_walk": walk}
        if use_ilp:
            out["forced_ilp"] = [q for q in graph[0] if forced_grid_ilp(t, q, graph) == "FORCED"]
        print(json.dumps(out), flush=True)
