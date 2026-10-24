"""Expérience 5 : les revêtements triples des quatre srg(243) sont-ils isomorphes ? (spectre, régularité de distance,
nombre de grilles par sommet) ; dim H^1(X; F_3) du revêtement par esquisse aléatoire."""
import sys, json, itertools
import numpy as np
from collections import Counter, deque
sys.path.insert(0, '.')
import srg_tools as T
import exp2_spread_cocycle as E2

ROOT = '/home/user/conway99-c1/data/srg243/'
files = {'BvLS': ROOT + 'bvls243.edges', 'twin': ROOT + 'twin243_switched.edges',
         'Gamma3': ROOT + 'family/gamma3_aut864.edges', 'Gamma4': ROOT + 'family/gamma4_aut3888.edges'}

def cover(fpath):
    n, edges, adj = T.load_edges(fpath)
    L = T.lines_of(n, adj)
    S = E2.regular_spreads(n, adj, L)[0]
    f = E2.spread_cocycle(n, edges, adj, S)
    eidx = T.edge_index(edges)
    volt = lambda u, v: f[eidx[(u, v)]] if u < v else -f[eidx[(v, u)]]
    N = 3 * n
    cadj = [set() for _ in range(N)]
    for (u, v) in edges:
        for s in range(3):
            t = (s + volt(u, v)) % 3
            cadj[3 * u + s].add(3 * v + t); cadj[3 * v + t].add(3 * u + s)
    return N, cadj

def intersection_array(N, adj):
    arr = set()
    for x in range(N):
        dist = [-1] * N; dist[x] = 0; dq = deque([x])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if dist[w] < 0: dist[w] = dist[u] + 1; dq.append(w)
        row = []
        for y in range(N):
            i = dist[y]
            c = sum(1 for w in adj[y] if dist[w] == i - 1)
            b = sum(1 for w in adj[y] if dist[w] == i + 1)
            row.append((i, c, b))
        arr.add(tuple(sorted(set(row))))
    return arr

if __name__ == '__main__':
    res = {}
    for name, fpath in files.items():
        N, cadj = cover(fpath)
        A = np.zeros((N, N))
        for u in range(N):
            for w in cadj[u]: A[u, w] = 1
        ev = np.round(np.linalg.eigvalsh(A), 6)
        spec = Counter(ev)
        ia = intersection_array(N, cadj)
        edges = sorted({(min(u, w), max(u, w)) for u in range(N) for w in cadj[u]})
        L = T.lines_of(N, cadj)
        grids = Counter(T.hamming_profile(N, cadj, L))
        res[name] = dict(spectrum={str(k): v for k, v in sorted(spec.items())},
                         distance_regular=len(ia) == 1, intersection=[list(map(list, a)) for a in ia][:3],
                         grids_per_vertex=dict(grids))
        print(name, json.dumps(res[name])[:900], flush=True)
    json.dump(res, open('../data/exp5_cover_invariants.json', 'w'), indent=1)
