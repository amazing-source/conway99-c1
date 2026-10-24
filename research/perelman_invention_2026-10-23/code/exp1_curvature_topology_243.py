"""Expérience 1 : sur les quatre srg(243,22,1,2) connus,
(a) parité de transport / courbure d'Ollivier des paires non adjacentes,
(b) dim H_1(X; F_p) du complexe triangles + quadrangles, p = 2, 3, 5, 7,
(c) profil de Hamming (paires de droites engendrant une grille) par sommet."""
import sys, json, time
from collections import Counter
sys.path.insert(0, '.')
from srg_tools import *

ROOT = '/home/user/conway99-c1/data/srg243/'
files = {'BvLS': ROOT + 'bvls243.edges', 'twin': ROOT + 'twin243_switched.edges',
         'Gamma3': ROOT + 'family/gamma3_aut864.edges', 'Gamma4': ROOT + 'family/gamma4_aut3888.edges'}
res = {}
for name, f in files.items():
    t0 = time.time()
    n, edges, adj = load_edges(f)
    assert check_srg(n, adj, 22, 1, 2)
    L = lines_of(n, adj); Q = squares_of(n, adj)
    par = nonedge_transport_parity(n, adj)
    epsc = Counter(v[0] for v in par.values())
    cyc = Counter(v[2] for v in par.values())
    paths = Counter(v[1] for v in par.values())
    b1 = {}
    for p in (2, 3, 5, 7):
        b, info = betti1_mod_p(n, edges, adj, p, L, Q)
        b1[p] = b
    hp = Counter(hamming_profile(n, adj, L))
    res[name] = dict(n_lines=len(L), n_squares=len(Q), eps=dict(epsc),
                     cycle_types=len(cyc), top_cycle_types=[(list(k), v) for k, v in cyc.most_common(6)],
                     path_types=[(list(k), v) for k, v in paths.most_common(6)],
                     betti1=b1, hamming_profile=dict(sorted(hp.items())), seconds=round(time.time() - t0, 1))
    print(name, json.dumps(res[name]), flush=True)
json.dump(res, open('../data/exp1_curvature_topology_243.json', 'w'), indent=1)
