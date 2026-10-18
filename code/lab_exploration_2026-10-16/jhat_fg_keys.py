"""Lemma FG on S7 classes of the census, read from the sorted key files of compare_census_aws.py (LAB, 18/10/2026).

Key format (compare_census_aws.py, run verif1a): "<J mask>|<blocks of root 0>|...|<blocks of root 6>", J mask over
combinations(range(7), 2) in order, each root field a '.'-joined list of 2-digit hex masks of its blocks of size >= 2.
One key = one template up to S7.  The template is rebuilt, FG (jhat_rows.forced_grid_walk) is applied, and the key of
every survivor is written out unchanged.
usage: python jhat_fg_keys.py <keys.sorted.gz> <first> <last> <out prefix>
       -> <out prefix>.surv.keys.gz and <out prefix>.sum.json"""
import gzip
import json
import sys
import time
from collections import Counter
from itertools import combinations

from jhat_rows import block_graph, forced_grid_walk

EDGES = list(combinations(range(7), 2))


def decode(key):
    f = key.strip().split("|")
    mask = int(f[0])
    nongrid = [list(e) for k, e in enumerate(EDGES) if mask >> k & 1]
    groups = []
    for r in range(7):
        fld = f[1 + r]
        groups.append([[j for j in range(7) if int(b, 16) >> j & 1] for b in fld.split(".")] if fld else [])
    t = {"nongrid_edges": nongrid, "nontrivial_component_groups": groups}
    # kernel dimension of the block graph = m - n + number of bipartite components
    graph = block_graph(t)
    edges, ends, at = graph
    verts = list(at)
    col, comps, bip = {}, 0, 0
    for v in verts:
        if v in col:
            continue
        comps += 1
        col[v] = 0
        stack, ok = [v], True
        while stack:
            x = stack.pop()
            for e in at[x]:
                a, b = ends[e]
                y = b if a == x else a
                if y not in col:
                    col[y] = 1 - col[x]
                    stack.append(y)
                elif col[y] == col[x]:
                    ok = False
        bip += ok
    t["kernel_dimension"] = len(edges) - len(verts) + bip
    t["component_count_by_root_line"] = [len(groups[r]) + 6 - sum(len(p) for p in groups[r]) for r in range(7)]
    return t, graph


if __name__ == "__main__":
    src, first, last, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    t0 = time.time()
    n = killed = 0
    dk, da = Counter(), Counter()
    with gzip.open(src, "rt") as fh, gzip.open(out + ".surv.keys.gz", "wt") as fo:
        for i, line in enumerate(fh):
            if i < first:
                continue
            if i >= last:
                break
            if not line.strip():
                continue
            n += 1
            t, graph = decode(line)
            hit = next((q for q in graph[0] if forced_grid_walk(t, q, graph)), None)
            if hit is not None:
                killed += 1
                dk[t["kernel_dimension"]] += 1
            else:
                da[t["kernel_dimension"]] += 1
                fo.write(line if line.endswith("\n") else line + "\n")
    s = {"source": src, "range": [first, last], "classes": n, "forced_grid": killed, "survivors": n - killed,
         "by_kernel_dimension": {str(d): {"forced_grid": dk[d], "survivors": da[d]} for d in sorted(set(dk) | set(da))},
         "seconds": round(time.time() - t0, 1)}
    json.dump(s, open(out + ".sum.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in s.items() if k != "by_kernel_dimension"}))
