"""Classify three perfect matchings on 12 points and apply the P3-closure cut.

This concerns the necessary local type of a triangle with 12 prism partners.
Two coincident matching edges must coincide in all three colors. The proof
is in the current night journal; surviving types are not C1 witnesses.
No external packages, SAT solver, or prior result files are used.
"""
from collections import Counter
from pathlib import Path
from itertools import combinations
import json


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for k in range(minimum, n + 1):
        for tail in partitions(n-k, k):
            yield (k,) + tail


def perfect_matchings(points):
    if not points:
        yield ()
        return
    x = points[0]
    for i in range(1, len(points)):
        y = points[i]
        for rest in perfect_matchings(points[1:i]+points[i+1:]):
            yield ((x,y),) + rest


def as_permutation(edges, n):
    p = [-1] * n
    for x,y in edges:
        p[x],p[y] = y,x
    assert all(p[p[i]] == i and p[i] != i for i in range(n))
    return tuple(p)


def relabel(p, g):
    result = [0] * len(p)
    for i in range(len(p)):
        result[g[i]] = g[p[i]]
    return tuple(result)


def standard_pair(parts):
    n = 2 * sum(parts)
    a = tuple(i ^ 1 for i in range(n))
    b = list(a)
    cycles = []
    offset = 0
    for part in parts:
        cycle = list(range(offset, offset + 2*part))
        for i in range(1, 2*part, 2):
            x,y = cycle[i], cycle[(i+1) % (2*part)]
            b[x],b[y] = y,x
        cycles.append(cycle)
        offset += 2*part
    generators = []
    for cycle in cycles:
        length = len(cycle)
        for local in ([((i+2) % length) for i in range(length)],
                      [((1-i) % length) for i in range(length)]):
            g = list(range(n))
            for i,j in enumerate(local):
                g[cycle[i]] = cycle[j]
            if g != list(range(n)):
                generators.append(tuple(g))
    for first,second in zip(cycles, cycles[1:]):
        if len(first) == len(second):
            g = list(range(n))
            for x,y in zip(first,second):
                g[x],g[y] = y,x
            generators.append(tuple(g))
    b = tuple(b)
    for g in generators:
        assert relabel(a,g) == a and relabel(b,g) == b
    return a,b,generators


def normalize_pair(a,b,c):
    """Return the standard alternating-cycle pair and the transported third."""
    unseen = set(range(len(a)))
    cycles = []
    while unseen:
        start = min(unseen)
        cycle = []
        x = start
        while True:
            cycle.extend((x,a[x]))
            unseen.remove(x)
            unseen.remove(a[x])
            x = b[a[x]]
            if x == start:
                break
        cycles.append(cycle)
    cycles.sort(key=lambda cycle: (len(cycle), cycle[0]))
    parts = tuple(len(cycle)//2 for cycle in cycles)
    g = [0] * len(a)
    for new,old in enumerate(x for cycle in cycles for x in cycle):
        g[old] = new
    aa,bb,_ = standard_pair(parts)
    assert relabel(a,g) == aa and relabel(b,g) == bb
    return parts,relabel(c,g)


def no_double_edge(a,b,c):
    return all(len({a[i],b[i],c[i]}) != 2 for i in range(len(a)))


def no_double_clauses(n=12):
    """Binary CNF cut after fixing color A to (0,1),(2,3),... .

    The first choose(n,2) variables are the unordered edges of B in
    lexicographic order; the next block is C. Perfect-matching constraints
    belong to the calling solver and are not included in this cut.
    """
    pairs = list(combinations(range(n),2))
    width = len(pairs)
    clauses = []
    for k,(i,j) in enumerate(pairs,1):
        b,c = k,k+width
        if (i ^ 1) == j:
            clauses.extend(([-b,c],[b,-c]))
        else:
            clauses.append([-b,-c])
    return pairs,clauses


def classify(n=12):
    assert n % 2 == 0
    matchings = sorted(as_permutation(e,n) for e in perfect_matchings(tuple(range(n))))
    lookup = {}
    representatives = []
    by_partition = []
    for parts in partitions(n//2):
        a,b,generators = standard_pair(parts)
        orbit_lookup = {}
        first_id = len(representatives)
        for c in matchings:
            if c in orbit_lookup:
                continue
            orbit_id = len(representatives)
            queue = [c]
            orbit_lookup[c] = orbit_id
            orbit_size = 0
            while queue:
                current = queue.pop()
                orbit_size += 1
                for g in generators:
                    changed = relabel(current,g)
                    if changed not in orbit_lookup:
                        orbit_lookup[changed] = orbit_id
                        queue.append(changed)
            representatives.append(dict(parts=parts,a=a,b=b,c=c,
                                        orbit_size=orbit_size,
                                        survives=no_double_edge(a,b,c)))
        assert len(orbit_lookup) == len(matchings)
        lookup[parts] = orbit_lookup
        by_partition.append(dict(parts=parts, labeled_thirds=len(matchings),
                                 ordered_color_orbits=len(representatives)-first_id,
                                 surviving_ordered_color_orbits=sum(
                                     r['survives'] for r in representatives[first_id:])))

    # The pair stabilizer orbits above quotient S_n. Adjacent color swaps
    # generate S_3; use them to quotient the remaining global color labels.
    parent = list(range(len(representatives)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def union(i,j):
        i,j = find(i),find(j)
        if i != j:
            parent[max(i,j)] = min(i,j)
    for i,r in enumerate(representatives):
        a,b,c = r['a'],r['b'],r['c']
        for aa,bb,cc in ((b,a,c),(a,c,b)):
            parts,third = normalize_pair(aa,bb,cc)
            j = lookup[parts][third]
            assert r['survives'] == representatives[j]['survives']
            union(i,j)
    roots = sorted({find(i) for i in range(len(representatives))})
    survivors = [i for i in roots if representatives[i]['survives']]
    pairs,clauses = no_double_clauses(n)
    for r in representatives:
        values = [False] + [r[color][i] == j
                            for color in ('b','c') for i,j in pairs]
        cnf_accepts = all(any(values[abs(v)] == (v > 0) for v in clause)
                          for clause in clauses)
        assert cnf_accepts == r['survives']
    triples = Counter(sum(r['a'][i] == r['b'][i] == r['c'][i]
                          for i in range(n))//2
                      for r in (representatives[i] for i in survivors))
    return dict(order=n, perfect_matchings=len(matchings),
                pair_partitions=len(by_partition),
                ordered_color_orbits=len(representatives),
                all_color_orbits=len(roots),
                surviving_ordered_color_orbits=sum(r['survives'] for r in representatives),
                surviving_all_color_orbits=len(survivors),
                excluded_all_color_orbits=len(roots)-len(survivors),
                solver_cut=dict(variables=2*len(pairs), binary_clauses=len(clauses),
                                first_matching='(0,1),(2,3),... fixed',
                                other_constraints='Perfect matchings required separately'),
                surviving_by_isolated_triple_edges=dict(sorted(triples.items())),
                by_pair_partition=by_partition,
                survivors=[{key:representatives[i][key] for key in ('a','b','c')}
                           for i in survivors],
                scope='Necessary local types only; survivors are not completed graphs')


def closure_nine_vertices():
    # A and B are the two triangle rows. Ci completes the edge Ai-Bi.
    # C0-C1-C2 is the forbidden induced path. No additional S-edges are possible.
    edges = {(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),
             (0,3),(1,4),(2,5),(0,6),(3,6),(1,7),(4,7),
             (2,8),(5,8),(6,7),(7,8)}
    degree = [sum(i in e for e in edges) for i in range(9)]
    f_on_s = [4-d for d in degree]
    assert degree == [4,4,4,4,4,4,3,4,3]
    assert f_on_s == [0,0,0,0,0,0,1,0,1]
    # f=(3I-A)1_S+1, using A^2+A=12I+2J.
    norm = 21*9 - 7*(2*len(edges)) + 2*9**2 - 22*9 + 99
    assert norm == 14
    return dict(vertices=9, edges=len(edges), degrees=degree,
                f_on_s=f_on_s, f_norm_squared=norm,
                f_outside_s='1 - number of neighbors in S',
                contradiction='The two positive path endpoints already share the zero-valued center; a norm-14 vector forces their two common neighbors inside its negative support.')


if __name__ == '__main__':
    report = dict(forbidden_prism_closure=closure_nine_vertices(), classification=classify())
    out = Path('data/codex_night_20261014/prism_closure_types.json')
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    pairs,clauses = no_double_clauses()
    cnf = ['c Necessary cut for a Conway triangle with 12 prism partners.',
           'c A=(0,1),(2,3),...,(10,11). B and C must be perfect matchings.',
           'c Perfect-matching constraints are NOT included in this file.']
    for color_index,color in enumerate(('B','C')):
        for k,(i,j) in enumerate(pairs,1):
            cnf.append(f'c var {color_index*len(pairs)+k} {color} {i} {j}')
    cnf.append(f'p cnf {2*len(pairs)} {len(clauses)}')
    cnf.extend(' '.join(map(str,c))+' 0' for c in clauses)
    out.with_name('prism12_no_double_cut.cnf').write_text('\n'.join(cnf)+'\n',encoding='utf-8')
    summary = {k:v for k,v in report['classification'].items()
               if k not in ('survivors','by_pair_partition')}
    print(json.dumps(summary,indent=2))
