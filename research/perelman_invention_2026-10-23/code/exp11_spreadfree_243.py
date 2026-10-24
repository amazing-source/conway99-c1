"""Expérience 11 : topologie du complexe X pour les srg(243,22,1,2) SANS étalement régulier trouvés par l'équipe
(code/lab_spreadfree_243_2026-10-12, NEW_GRAPHS_2026-10-13.md et NOTE_SPREADFREE.md). Ce sont les graphes « du type de
Conway » (pas d'étalement régulier). Test de la Conjecture 3.10 transposée : H^1(X; F_3) = 0 ?

Pour chaque graphe : vérification srg, nombre d'étalements réguliers, H_1(X; F_p) pour p = 2, 3, 5, 7, ordre de pi_1
par énumération de classes (exp9), parité d'appariement eta et cycles des graphes d'appariement (exp10)."""
import sys, json, time
from collections import Counter
sys.path.insert(0, '.')
import srg_tools as T
from exp2_spread_cocycle import regular_spreads
from exp9_universal_cover import universal_cover
from exp10_transport_graphs import transport_stats

LAB = '/home/user/conway99-c1/code/lab_spreadfree_243_2026-10-12/'
files = {'Gamma5_tricayley': LAB + 'new243_tricayley_Z3x4_grids25.edges',
         'Gamma6_trade_aut108': LAB + 'new243_trade_aut108.edges',
         'Gamma7_trade_aut162': LAB + 'new243_trade_aut162.edges',
         'Gamma8_trade_aut108_b': LAB + 'new243_trade_aut108_b.edges'}

if __name__ == '__main__':
    out = {}
    for name, f in files.items():
        t0 = time.time()
        n, edges, adj = T.load_edges(f)
        ok = T.check_srg(n, adj, 22, 1, 2)
        L = T.lines_of(n, adj)
        spreads = regular_spreads(n, adj, L)
        h1 = {}
        for p in (2, 3, 5, 7):
            d, info = T.betti1_mod_p(n, edges, adj, p, lines=L)
            h1[p] = d
        U = universal_cover(n, adj)
        tr = transport_stats(n, adj, sample=range(0, n, 9))
        out[name] = dict(srg=ok, n=n, regular_spreads=len(spreads), h1=h1, universal_cover_vertices=U,
                         pi1_order=None if U is None else U // n, transport=tr,
                         grids_per_vertex=dict(Counter(T.hamming_profile(n, adj, L))), seconds=round(time.time() - t0, 1))
        print(name, out[name], flush=True)
    json.dump(out, open('../data/exp11_spreadfree_243.json', 'w'), indent=1)
