# One component of G(L) with m classes (2m labels) per layer, built directly as a graph:
#   x-layer: labels v (internal edge v - vbar), u-layer: (u,v) (internal edge = tau_u), ubar-layer: (ub,v) (tau_ub),
#   cross edges v-(u,v), v-(ub,v), (u,v)-(ub,sigma v).
# Hand-derived claim: at P = 0, girth >= 5  <=>  tau_u, tau_ub avoid mates, sigma(v) not in {v, vbar, tau_u v, tau_ub v},
#   and tau_ub(sigma w) != sigma(tau_u w) for all w.  (m = 2: impossible; m = 3: enumerate.)
import itertools, networkx as nx
def matchings(labels, mate):
    if not labels: yield {}; return
    a = labels[0]
    for b in labels[1:]:
        if b == mate[a]: continue
        rest = [c for c in labels if c not in (a, b)]
        for m in matchings(rest, mate):
            d = dict(m); d[a] = b; d[b] = a; yield d
def build(labels, mate, tu, tub, sig):
    G = nx.Graph()
    for v in labels:
        G.add_edge(('x', v), ('x', mate[v])); G.add_edge(('u', v), ('u', tu[v])); G.add_edge(('b', v), ('b', tub[v]))
        G.add_edge(('x', v), ('u', v)); G.add_edge(('x', v), ('b', v)); G.add_edge(('u', v), ('b', sig[v]))
    return G
def girth(G):
    return nx.girth(G)
for m in (2, 3):
    labels = list(range(2 * m)); mate = {i: i ^ 1 for i in labels}
    M = list(matchings(labels, mate))
    tot = agree = g5 = 0; conn = 0
    for tu in M:
        for tub in M:
            for perm in itertools.permutations(labels):
                sig = dict(zip(labels, perm))
                G = build(labels, mate, tu, tub, sig)
                if not nx.is_connected(G): continue
                if any(len(set(G[n])) != 3 for n in G): continue
                tot += 1
                real = girth(G) >= 5
                pred = (all(sig[v] not in (v, mate[v], tu[v], tub[v]) for v in labels)
                        and all(tub[sig[w]] != sig[tu[w]] for w in labels))
                agree += (real == pred); g5 += real
    print(f'm={m}: connected cubic configurations {tot}, girth>=5: {g5}, prediction agrees on {agree}/{tot}')
