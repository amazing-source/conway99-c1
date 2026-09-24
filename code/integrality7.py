"""Integrality of the order-<=7 counts of srg(99,14,1,2): which (P, S) make every count an integer?"""
import pickle, math
from fractions import Fraction
from functools import reduce
import networkx as nx
from subgraph_lp import Types
D = pickle.load(open('../data/exact_region_order7.pkl', 'rb'))
var, free, z0, V = D['var'], D['free'], D['z0'], D['V']
idx = {v: q for q, v in enumerate(var)}
T = Types(1, 2, 14, 7)
def gid(edges, m):
    G = nx.Graph(); G.add_nodes_from(range(m)); G.add_edges_from(edges)
    return idx[(m, T.find(G))]
qP = gid([(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)], 6)
qZ = gid([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4),(5,1),(5,3),(6,2),(6,4),(5,6)], 7)
den = reduce(lambda a, b: a * b // math.gcd(a, b), [x.denominator for row in V for x in row] + [x.denominator for x in z0], 1)
print('free variables:', free, ' common denominator of the parametrisation:', den)
# t = (t1, t2) are themselves counts (integers). Enumerate residues mod den.
ok = []
for a in range(den):
    for b in range(den):
        if all((z0[q] + V[q][0] * a + V[q][1] * b).denominator == 1 for q in range(len(var))):
            ok.append((a, b))
print(f'admissible residues (t1, t2) mod {den}: {len(ok)} of {den*den}')
# express P and S in terms of t
print('P =', z0[qP], '+', V[qP][0], '* t1 +', V[qP][1], '* t2')
print('S/2 = z(Z2) =', z0[qZ], '+', V[qZ][0], '* t1 +', V[qZ][1], '* t2')
resP = sorted({int((z0[qP] + V[qP][0] * a + V[qP][1] * b)) % 1000000 for a, b in ok} if ok else [])
print('P values mod ... (first residues):', [(z0[qP] + V[qP][0] * a + V[qP][1] * b) for a, b in ok[:10]])
