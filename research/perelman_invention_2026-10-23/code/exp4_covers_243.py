"""Expérience 4 : revêtements triples (voltage = cocycle d'étalement) des srg(243,22,1,2) ;
appartenance à K_22, croissance comparée à H(11,3), propriété (L), H^1 mod 3 du revêtement."""
import sys, json
sys.path.insert(0, '.')
from srg_tools import *
from exp2_spread_cocycle import regular_spreads, spread_cocycle
from exp3_growth_comparison import check_K, spheres, analyse

ROOT = '/home/user/conway99-c1/data/srg243/'
files = {'BvLS': ROOT + 'bvls243.edges', 'twin': ROOT + 'twin243_switched.edges',
         'Gamma3': ROOT + 'family/gamma3_aut864.edges', 'Gamma4': ROOT + 'family/gamma4_aut3888.edges'}
out = {}
for name, fpath in files.items():
    n, edges, adj = load_edges(fpath)
    L = lines_of(n, adj)
    S = regular_spreads(n, adj, L)[0]
    f = spread_cocycle(n, edges, adj, S)
    eidx = edge_index(edges)
    def volt(u, v):
        return f[eidx[(u, v)]] if u < v else -f[eidx[(v, u)]]
    N = 3 * n
    cadj = [set() for _ in range(N)]
    for (u, v) in edges:
        for s in range(3):
            t = (s + volt(u, v)) % 3
            cadj[3 * u + s].add(3 * v + t); cadj[3 * v + t].add(3 * u + s)
    # connexité
    seen = {0}; st = [0]
    while st:
        z = st.pop()
        for w in cadj[z]:
            if w not in seen: seen.add(w); st.append(w)
    print(name, 'revêtement triple connexe :', len(seen) == N, flush=True)
    out[name] = analyse(name + ' 3-cover', N, cadj)
json.dump(out, open('../data/exp4_covers_243.json', 'w'), indent=1)
