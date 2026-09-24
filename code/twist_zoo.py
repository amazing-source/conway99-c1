"""Collect several twisted local-axiom graphs (t, n range, a few solutions per n with blocking clauses) and record
|Aut|, number of vertices x whose point reflection sigma_x (defined on the ball of radius 2) extends to an
automorphism, trail-cycle types and non-coherent tau counts. Tests idea N6 ('rigidity forces point reflections').
Usage: python twist_zoo.py t nmin nmax per_n conflicts
"""
import sys, json, time
import numpy as np, networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
from pysat.solvers import Glucose4
import twist_search as ts
import rooted


def analyse(A):
    G = nx.from_numpy_array(np.array(A))
    n = len(A)
    auts = []
    for m in GraphMatcher(G, G).isomorphisms_iter():
        auts.append(m)
        if len(auts) > 5000:
            break
    hits = 0
    for x in range(n):
        R = rooted.Rooted(np.array(A), x)
        sig = {x: x}
        for a in R.L:
            sig[a] = R.mate[a]
        for u in R.X:
            a, b = tuple(R.label[u])
            sig[u] = R.vertex_of[frozenset((R.mate[a], R.mate[b]))]
        hits += any(all(m[v] == sig[v] for v in sig) for m in auts)
    tw = sum(1 for x in range(n) if not rooted.Rooted(np.array(A), x).is_mate_system())
    return len(auts), hits, tw, nx.diameter(G)


def main():
    t, nmin, nmax, per_n, conf = map(int, sys.argv[1:6])
    out = []
    for n in range(nmin, nmax + 1):
        cnf, pool, E = ts.build(t, n, twisted=True)
        S = Glucose4(bootstrap_with=cnf.clauses)
        for k in range(per_n):
            S.conf_budget(conf)
            ok = S.solve_limited()
            if not ok:
                print(f't={t} n={n} sol#{k}: {ok}', flush=True)
                break
            A = ts.decode(S.get_model(), pool, n, E)
            naut, hits, tw, diam = analyse(A)
            print(f't={t} n={n} sol#{k}: |Aut|={naut if naut <= 5000 else ">5000"} sigma-extending vertices={hits}/{n} '
                  f'twisted vertices={tw} diam={diam}', flush=True)
            out.append({'t': t, 'n': n, 'aut': naut, 'hits': hits, 'tw': tw, 'A': A})
            # block this exact edge set
            S.add_clause([-E(u, v) if A[u][v] else E(u, v) for u in range(n) for v in range(u + 1, n)])
        S.delete()
    json.dump(out, open(f'../data/zoo_t{t}_{nmin}_{nmax}.json', 'w'))


if __name__ == '__main__':
    main()
