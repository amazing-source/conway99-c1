"""notes/109: how far does pure slot counting (notes/108) go?  Enumerate all twisting patterns with a given
number of incomplete grids |N| (T(l) = classes twisted by label l, |T(l)| in {0} u [2,6], N = union of the
stars {class(l) c : c in T(l)}, L13: every twisted class is twisted by 0 or >= 2 labels), up to relabelling
classes and swapping the two labels of a class; then all tau/rho details; run interval propagation and, if
needed, the exactly-certified LP.  Usage: python slot_frontier.py N"""
import itertools, sys
from collections import Counter, defaultdict
import networkx as nx
from slot_calculus import LAB, CL, mate
from slot_tests import configs
from slot_lp import lp_check

pairs = list(itertools.combinations(CL, 2))

def graphs(k):
    seen = []
    for es in itertools.combinations(pairs, k):
        G = nx.Graph(); G.add_nodes_from(CL); G.add_edges_from(es)
        if any(nx.is_isomorphic(G, H) for H in seen):
            continue
        seen.append(G)
        yield es

def patterns(es):
    E = set(frozenset(e) for e in es)
    nbr = {c: [d for d in CL if frozenset((c, d)) in E] for c in CL}
    opts = []
    for l in LAB:
        o = [frozenset()]
        for r in range(2, len(nbr[l[0]]) + 1):
            o += [frozenset(s) for s in itertools.combinations(nbr[l[0]], r)]
        opts.append(o)
    out = set()
    for choice in itertools.product(*opts):
        T = dict(zip(LAB, choice))
        cover = set(frozenset((l[0], c)) for l in LAB for c in T[l])
        if cover != E:
            continue
        tw = Counter(c for l in LAB for c in T[l])
        if any(v == 1 for v in tw.values()):
            continue
        # canonical form under swapping the two labels of each class
        key = tuple(sorted(tuple(sorted((tuple(sorted(T[(c, 0)])), tuple(sorted(T[(c, 1)]))))) for c in CL))
        # (class labels are fixed by the chosen graph representative; residual graph automorphisms ignored)
        if (key, es) in out:
            continue
        out.add((key, es))
        yield {l: set(T[l]) for l in LAB if T[l]}


from slot_tests import matchings_no_mate, fpf_perms
def n_configs(T):
    tw = [l for l in LAB if T.get(l)]
    n = 1
    for l in tw:
        labs = [(c, s) for c in sorted(T[l]) for s in (0, 1)]
        n *= len(list(matchings_no_mate(labs)))
    for c in CL:
        Z = [l for l in tw if c in T[l]]
        if Z:
            n *= len(list(fpf_perms(Z)))
    return n
