"""Fast enumeration of k-twisting-label patterns up to symmetry: normalised generation (twisting labels occupy
classes 0..m-1, a class with two twisting labels uses both signs, a class with one uses sign 0), rules
R0 + L12 + L13a, then dedup by Weisfeiler-Lehman hash + exact isomorphism (networkx) on the coloured graph.
Usage: python wpatterns_fast.py k
"""
import itertools, sys, time
import networkx as nx
from networkx.algorithms.isomorphism import categorical_node_match
import wpatterns_direct as wd
import wpatterns as wp

C7 = list(range(7))


def gen(k):
    for a2 in range(k // 2 + 1):
        b1 = k - 2 * a2
        if a2 + b1 > 7:
            continue
        labs = [(c, s) for c in range(a2) for s in (0, 1)] + [(a2 + i, 0) for i in range(b1)]
        opts = [[frozenset(S) for r in range(2, 7) for S in itertools.combinations([c for c in C7 if c != a[0]], r)]
                for a in labs]
        for combo in itertools.product(*opts):
            pat = dict(zip(labs, combo))
            if wd.rules_ok(pat):
                yield pat


def main():
    k = int(sys.argv[1])
    t0 = time.time()
    nm = categorical_node_match('kind', None)
    em = lambda e1, e2: e1['kind'] == e2['kind']
    buckets, reps, raw = {}, [], 0
    for pat in gen(k):
        raw += 1
        G = wp.graph_of(frozenset((a, j) for a, Cs in pat.items() for j in Cs))
        h = nx.weisfeiler_lehman_graph_hash(G, node_attr='kind', edge_attr='kind', iterations=4)
        lst = buckets.setdefault(h, [])
        if any(nx.is_isomorphic(G, H, node_match=nm, edge_match=em) for H in lst):
            continue
        lst.append(G)
        reps.append(pat)
    specs = [','.join(f'{a[0]}{a[1]}:' + ''.join(str(j) for j in sorted(Cs)) for a, Cs in sorted(p.items())) for p in reps]
    open(f'../data/k{k}_patterns_fast.txt', 'w', newline='\n').write('\n'.join(specs) + '\n')
    print(f'k = {k}: {raw} normalised patterns pass the rules, {len(reps)} up to symmetry ({time.time()-t0:.0f}s)')


if __name__ == '__main__':
    main()
