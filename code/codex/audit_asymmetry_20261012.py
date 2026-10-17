"""Independent audit of the four deposited (243,22,1,2) graphs.

No import from the campaign's graph library. Integer neighbourhood checks,
explicit grid closures, BLISS full automorphism generators, Schreier-Sims.
Requires numpy, sympy, igraph. Optional --deps adds an isolated package folder.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]


def read_graph(path):
    import numpy as np
    pairs = [tuple(map(int, s.split())) for s in path.read_text().splitlines()
             if s.strip() and not s.startswith('#')]
    assert all(len(e) == 2 and 0 <= e[0] < e[1] < 243 for e in pairs)
    assert len(set(pairs)) == len(pairs)
    a = np.zeros((243, 243), dtype=np.int64)
    for u, v in pairs:
        a[u, v] = a[v, u] = 1
    return a, pairs


def grids(a, ns):
    found = set()
    for x in range(len(a)):
        lines = [(u, v) for u, v in combinations(sorted(ns[x]), 2) if a[u, v]]
        for (u, v), (w, z) in combinations(lines, 2):
            corners = []
            for p, q in ((u, w), (u, z), (v, w), (v, z)):
                common = (ns[p] & ns[q]) - {x}
                assert len(common) == 1
                corners.append(next(iter(common)))
            # Explicit 3x3 coordinates: [x,w,z; u,uw,uz; v,vw,vz].
            order = [x, w, z, u, corners[0], corners[1], v, corners[2], corners[3]]
            if len(set(order)) != 9:
                continue
            if all(bool(a[order[i], order[j]]) == (i // 3 == j // 3 or i % 3 == j % 3)
                   for i, j in combinations(range(9), 2)):
                found.add(tuple(sorted(order)))
    per_vertex = Counter(v for g in found for v in g)
    return len(found), dict(sorted(Counter(per_vertex.get(v, 0) for v in range(len(a))).items()))


def audit(path):
    import numpy as np
    import igraph as ig
    from sympy.combinatorics import Permutation, PermutationGroup
    a, pairs = read_graph(path)
    ns = [set(map(int, np.flatnonzero(row))) for row in a]
    assert len(pairs) == 2673 and all(len(s) == 22 for s in ns)
    counts = Counter()
    for u, v in combinations(range(243), 2):
        common = len(ns[u] & ns[v])
        assert common == (1 if a[u, v] else 2), (u, v, common)
        counts[(int(a[u, v]), common)] += 1
    assert np.array_equal(a @ a + a, 20 * np.eye(243, dtype=np.int64) + 2)
    g = ig.Graph(n=243, edges=pairs, directed=False)
    gens = g.automorphism_group()
    for p in gens:
        assert sorted(p) == list(range(243)) and np.array_equal(a[np.ix_(p, p)], a)
    group = PermutationGroup([Permutation(p) for p in gens])
    grid_count, grid_distribution = grids(a, ns)
    triangles = [(u, v, w) for u, v in pairs for w in ns[u] & ns[v] if w > v]
    assert len(triangles) == 891
    joins = Counter()
    for t, s in combinations(triangles, 2):
        if set(t).isdisjoint(s):
            joins[sum(int(a[u, v]) for u in t for v in s)] += 1
    row = dict(file=str(path.relative_to(ROOT)).replace('\\', '/'),
               sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
               srg_parameters=[243, 22, 1, 2], pairs_checked=sum(counts.values()),
               automorphism_order=int(group.order()),
               vertex_orbits=sorted(map(len, group.orbits())),
               bliss_generator_count=len(gens), grids=grid_count,
               grids_per_vertex_distribution=grid_distribution,
               triangles=len(triangles), twisted_triangle_pairs=joins[2],
               prisms=joins[3])
    assert joins[2] == 10 * len(pairs) - 3 * joins[3]
    print(json.dumps(row), flush=True)
    return row


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--deps')
    p.add_argument('--output', default='data/codex_asymmetry_audit_20261012.json')
    args = p.parse_args()
    if args.deps:
        sys.path.insert(0, args.deps)
    files = ['data/srg243/bvls243.edges', 'data/srg243/twin243_switched.edges',
             'data/srg243/family/gamma3_aut864.edges',
             'data/srg243/family/gamma4_aut3888.edges']
    rows = [audit(ROOT / f) for f in files]
    assert len(set(r['grids'] for r in rows)) == 4
    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dict(source_commit='640ffe1', graphs=rows,
                                  conclusion='Four pairwise nonisomorphic SRGs, none asymmetric.'),
                               indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
