"""Enumerate class-level twist patterns W (label a twists class j) with exactly k twisting labels, allowed by the
hand-proved rules R0, L12, L13a, up to the symmetry group of the rooted structure (S7 on classes x sign flips).
Canonical form via networkx graph isomorphism on a small coloured graph (labels, classes, mate edges, W edges).
Usage: python wpatterns.py k
"""
import sys, itertools
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher, categorical_node_match
from pysat.solvers import Cadical153
import l12_closure as lc

CL = range(7)
LABELS = lc.LABELS


def patterns(k):
    pool, cnf, W = lc.base()
    from pysat.card import CardEnc, EncType
    T = {}
    for a in LABELS:
        t = pool.id(('T', a))
        T[a] = t
        ws = [W(a, j) for j in CL if j != a[0]]
        cnf.append([-t] + ws)
        for w in ws:
            cnf.append([t, -w])
    cnf.extend(CardEnc.equals(list(T.values()), k, vpool=pool, encoding=EncType.seqcounter).clauses)
    S = Cadical153(bootstrap_with=cnf)
    out = []
    while S.solve():
        m = set(l for l in S.get_model() if l > 0)
        pat = frozenset((a, j) for a in LABELS for j in CL if j != a[0] and W(a, j) in m)
        out.append(pat)
        S.add_clause([-W(a, j) for (a, j) in pat] + [W(a, j) for a in LABELS for j in CL if j != a[0] and (a, j) not in pat])
    return out


def graph_of(pat):
    G = nx.Graph()
    for c in CL:
        G.add_node(('C', c), kind='class')
    for a in LABELS:
        G.add_node(('L', a), kind='label')
        G.add_edge(('L', a), ('C', a[0]), kind='member')
    for (a, j) in pat:
        G.add_edge(('L', a), ('C', j), kind='twist')
    return G


def classes_up_to_symmetry(pats):
    reps = []
    for p in pats:
        G = graph_of(p)
        if any(nx.is_isomorphic(G, graph_of(r), node_match=categorical_node_match('kind', None),
                                edge_match=lambda e1, e2: e1['kind'] == e2['kind']) for r in reps):
            continue
        reps.append(p)
    return reps


if __name__ == '__main__':
    k = int(sys.argv[1])
    pats = patterns(k)
    reps = classes_up_to_symmetry(pats)
    print(f'k = {k}: {len(pats)} labelled W-patterns allowed by R0+L12+L13a, {len(reps)} up to symmetry')
    for r in reps:
        d = {}
        for (a, j) in sorted(r):
            d.setdefault(a, []).append(j)
        print('   ', d)
