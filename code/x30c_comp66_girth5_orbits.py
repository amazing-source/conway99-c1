# The 288 labeled 6-label components (3 classes) with girth >= 5, up to relabelings preserving mates (order 48).
import itertools, networkx as nx
labels = list(range(6)); mate = {i: i ^ 1 for i in labels}
def matchings(ls):
    if not ls: yield {}; return
    a = ls[0]
    for b in ls[1:]:
        if b == mate[a]: continue
        rest = [c for c in ls if c not in (a, b)]
        for m in matchings(rest):
            d = dict(m); d[a] = b; d[b] = a; yield d
M = list(matchings(labels))
good = []
for tu in M:
    for tb in M:
        for perm in itertools.permutations(labels):
            s = dict(zip(labels, perm))
            if all(s[v] not in (v, mate[v], tu[v], tb[v]) for v in labels) and all(tb[s[w]] != s[tu[w]] for w in labels):
                good.append((tu, tb, s))
print('labeled:', len(good))
# relabelings g preserving mates
G = []
for p in itertools.permutations(range(3)):
    for flips in itertools.product((0, 1), repeat=3):
        g = {}
        for c in range(3):
            for e in (0, 1):
                g[2 * c + e] = 2 * p[c] + (e ^ flips[c])
        G.append(g)
def key(cfg):
    tu, tb, s = cfg
    return (tuple(tu[i] for i in labels), tuple(tb[i] for i in labels), tuple(s[i] for i in labels))
def act(g, cfg):
    tu, tb, s = cfg
    gi = {v: k for k, v in g.items()}
    conj = lambda f: {i: g[f[gi[i]]] for i in labels}
    return (conj(tu), conj(tb), conj(s))
seen = set(); orbits = []
for cfg in good:
    k = key(cfg)
    if k in seen: continue
    orb = {key(act(g, cfg)) for g in G}
    seen |= orb; orbits.append((cfg, len(orb)))
def cyc(s):
    out = []; done = set()
    for i in labels:
        if i in done: continue
        c = [i]; done.add(i); j = s[i]
        while j != i: c.append(j); done.add(j); j = s[j]
        out.append(len(c))
    return sorted(out)
for cfg, n in orbits:
    tu, tb, s = cfg
    same = sum(tu[v] == tb[v] for v in labels)
    # graph invariants
    Gr = nx.Graph()
    for v in labels:
        Gr.add_edge(('x', v), ('x', mate[v])); Gr.add_edge(('u', v), ('u', tu[v])); Gr.add_edge(('b', v), ('b', tb[v]))
        Gr.add_edge(('x', v), ('u', v)); Gr.add_edge(('x', v), ('b', v)); Gr.add_edge(('u', v), ('b', s[v]))
    c5 = sum(1 for c in nx.simple_cycles(Gr, length_bound=5) if len(c) == 5)
    print(f'orbit size {n:3d}: sigma cycles {cyc(s)}, |tau_u = tau_ub| = {same}, girth {nx.girth(Gr)}, 5-cycles {c5}, '
          f'tau_u={key(cfg)[0]} tau_ub={key(cfg)[1]} sigma={key(cfg)[2]}')
