"""Necessary endpoint templates for the unique edge of D, using note253.

Templates are quotiented only by Aut(Z), retaining the order of the two
labelled D endpoints. Spectral tests use exact scaled Schur entries.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json

import networkx as nx
import numpy as np

from norm16_schur_data import ROOT, matrices, source_data


def bits(mask):
    return [i for i in range(11) if mask >> i & 1]


@lru_cache(None)
def templates(fid, refined=False):
    forest = next(f for f in source_data()[2] if f['id'] == fid)
    az = forest['adjacency_Z']
    deg = list(map(sum, az))
    if refined and max(deg) > 2:
        return []
    zr = [sum(1 << i for i, x in enumerate(row) if x) for row in az]
    graph = nx.from_numpy_array(np.array(az))
    autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
    result = {}
    for star in range(11):
        if deg[star] > 1:
            continue
        if refined and deg[star] != 0:
            continue
        for u, v in combinations([z for z in range(11) if z != star], 2):
            if deg[u]+deg[v] != 4+deg[star] or zr[star] & ~((1 << u) | (1 << v)):
                continue
            if refined and (deg[u] != 2 or deg[v] != 2 or az[u][v] or zr[u] & zr[v]):
                continue
            rest = [z for z in range(11) if z not in (star, u, v)]
            for aa in combinations(rest, 4):
                bb = [z for z in rest if z not in aa]
                if sum(deg[z] for z in aa) != 4-deg[star]:
                    continue
                r = (1 << star) | sum(1 << z for z in aa)
                t = (1 << star) | sum(1 << z for z in bb)
                if any((r & zr[z]).bit_count()+((t >> z) & 1) > 2-((r >> z) & 1)
                       or (t & zr[z]).bit_count()+((r >> z) & 1) > 2-((t >> z) & 1)
                       for z in range(11)):
                    continue
                if any(((r >> z) & (r >> w) & 1)+((t >> z) & (t >> w) & 1)
                       > 2-az[z][w]-(zr[z] & zr[w]).bit_count()
                       for z, w in combinations(range(11), 2)):
                    continue
                key = min((sum(1 << a[z] for z in bits(r)), sum(1 << a[z] for z in bits(t))) for a in autos)
                result[key] = {'rows': list(key)}
    return list(result.values())


def main():
    sources = json.loads((ROOT/'data/codex_norm16_D_edge_reduction.json').read_text())
    out = []
    for f in source_data()[2]:
        if not f['edges_D']:
            continue
        ts = templates(f['id'])
        records = []
        for case in sources['cases']:
            ci = case['case']
            for orbit in case['orbits']:
                oi = orbit['orbit']
                scale, h, w = matrices(ci, oi, f['id'])
                h, w = np.array(h, dtype=np.int64), np.array(w, dtype=np.int64)
                costs = []
                for template in ts:
                    k = np.array([[3-7*((mask >> z) & 1) for z in range(11)] for mask in template['rows']], dtype=np.int64)
                    costs.append(k @ w @ k.T)
                for d, e in orbit['eligible_edges']:
                    live = []
                    for ti, cost in enumerate(costs):
                        a, b, c = int(h[d, d]-cost[0, 0]), int(h[e, e]-cost[1, 1]), int(h[d, e]-scale-cost[0, 1])
                        if a >= 0 and b >= 0 and a*b-c*c >= 0:
                            live.append(ti)
                    records.append({'case': ci, 'orbit': oi, 'edge': [d, e], 'templates': live})
        item = {'forest': f['id'], 'templates': ts, 'records': records}
        out.append(item)
        print(json.dumps({'forest': f['id'], 'local_templates': len(ts), 'live_edges': sum(bool(r['templates']) for r in records), 'live_templates': sum(len(r['templates']) for r in records)}), flush=True)
    target = ROOT/'data/codex_norm16_edge_endpoints.json'
    target.write_text(json.dumps({'scope': __doc__, 'forests': out}, indent=2)+'\n')


if __name__ == '__main__':
    main()
