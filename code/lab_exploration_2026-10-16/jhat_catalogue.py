"""Exact row catalogue of a root template by depth-first search on its block graph (LAB, 18/10/2026).

Same set as Codex's row_catalogue (root_component_z_distribution.py): all integral z with the component equations and
the quota bounds; written with h = base - z (jhat_rows.py), so: integer zero-sum weightings of the block graph Jh in the
box of the class, h = 0 on grid rectangles.  Codex enumerates the product of the free coordinates (5^d points, d <= 6
by default); here a DFS assigns the edges one by one and prunes a vertex as soon as its remaining edges cannot bring its
sum back to zero, so only valid rows are visited.  Output: Codex's catalogue format (states as z-vectors of length 21),
so that Codex's linear_system / find_certificate can be applied unchanged.
usage: python jhat_catalogue.py <catalogue> <index> [--compare]   (--compare: also run Codex's row_catalogue)"""
import json
import sys

from jhat_rows import RECT, block_graph, box, records


def base(q, f):
    return 2 if f == q else (0 if set(f) & set(q) else 1)


def rows_of_class(graph, q, limit=None):
    edges, ends, at = graph
    verts = list(at)
    vid = {x: i for i, x in enumerate(verts)}
    # order edges so that vertices close early (greedy: edge touching the most-assigned vertices first)
    order = []
    left = {x: len(at[x]) for x in verts}
    rem = list(edges)
    while rem:
        rem.sort(key=lambda e: (min(left[ends[e][0]], left[ends[e][1]]), left[ends[e][0]] + left[ends[e][1]]))
        e = rem.pop(0)
        order.append(e)
        left[ends[e][0]] -= 1
        left[ends[e][1]] -= 1
    lo = {e: box(q, e)[0] for e in edges}
    hi = {e: box(q, e)[1] for e in edges}
    # for each position, remaining min/max per vertex after this position
    n = len(order)
    remmin = [[0] * len(verts) for _ in range(n + 1)]
    remmax = [[0] * len(verts) for _ in range(n + 1)]
    for p in range(n - 1, -1, -1):
        e = order[p]
        remmin[p] = list(remmin[p + 1])
        remmax[p] = list(remmax[p + 1])
        for x in ends[e]:
            remmin[p][vid[x]] += lo[e]
            remmax[p][vid[x]] += hi[e]
    out = []
    val = {}
    s = [0] * len(verts)

    def dfs(p):
        if limit is not None and len(out) >= limit:
            return
        if p == n:
            if all(v == 0 for v in s):
                out.append(dict(val))
            return
        e = order[p]
        u, v = vid[ends[e][0]], vid[ends[e][1]]
        for h in range(lo[e], hi[e] + 1):
            s[u] += h
            s[v] += h
            if (s[u] + remmin[p + 1][u] <= 0 <= s[u] + remmax[p + 1][u]
                    and s[v] + remmin[p + 1][v] <= 0 <= s[v] + remmax[p + 1][v]):
                val[e] = h
                dfs(p + 1)
            s[u] -= h
            s[v] -= h
        val.pop(e, None)

    dfs(0)
    return out


def catalogue(t, limit=None):
    graph = block_graph(t)
    E = set(graph[0])
    cat = []
    for q in RECT:
        rs = rows_of_class(graph, q, limit)
        states = [[base(q, f) - (r[f] if f in E else 0) for f in RECT] for r in rs]
        cat.append({"rectangle": list(q), "states": states, "state_count": len(states)})
    return {"status": "ROW_CATALOGUE_COMPLETE" if limit is None else "ROW_CATALOGUE_TRUNCATED",
            "free_dimension": t.get("kernel_dimension"), "row_types": cat}


if __name__ == "__main__":
    path, index = sys.argv[1], int(sys.argv[2])
    t = next(r for i, r in enumerate(records(path)) if i == index)
    import time
    t0 = time.time()
    cat = catalogue(t)
    counts = [r["state_count"] for r in cat["row_types"]]
    print(json.dumps({"index": index, "dim": t.get("kernel_dimension"), "states_total": sum(counts),
                      "states_max": max(counts), "seconds": round(time.time() - t0, 2)}))
    if "--compare" in sys.argv:
        sys.path.insert(0, sys.argv[sys.argv.index("--compare") + 1])
        from root_component_z_distribution import row_catalogue
        ref = row_catalogue(t, max_free=21)
        same = all(sorted(map(tuple, a["states"])) == sorted(map(tuple, b["states"]))
                   for a, b in zip(cat["row_types"], ref["row_types"]))
        print("identical to Codex's row_catalogue:", same)
