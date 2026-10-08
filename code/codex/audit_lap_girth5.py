"""Independent small-ingredient/coverage audit of LAP's rank-37 girth-5 proof.

Does not replay all star searches or the complete GL(3,7) search.
No imports from the proof implementation: only the archived input data/logs.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path
import re

import numpy as np


def matchings(points):
    if not points:
        yield ()
        return
    u, *rest = points
    for v in rest:
        for pairs in matchings([w for w in rest if w != v]):
            yield ((u, v),)+pairs


def matching_map(pairs, n):
    p = [0]*n
    for u, v in pairs:
        p[u], p[v] = v, u
    return tuple(p)


def graph(key):
    n = len(key[0])
    rows = [0]*(3*n)
    def edge(u, v):
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    for layer in range(3):
        for i, j in enumerate(key[layer]):
            edge(layer*n+i, layer*n+j)
    for i in range(n):
        edge(i, n+i)
        edge(i, 2*n+i)
        edge(n+i, 2*n+key[3][i])
    return rows


def girth5(rows):
    return all((rows[u] & rows[v]).bit_count() <= (0 if rows[u] >> v & 1 else 1)
               for u, v in combinations(range(len(rows)), 2))


def enumerate_normal(n):
    fixed = tuple(i ^ 1 for i in range(n))
    mates = [matching_map(p, n) for p in matchings(list(range(n)))]
    out = set()
    for p, q, r in product(mates, mates, list(permutations(range(n)))):
        key = (fixed, p, q, r)
        if girth5(graph(key)):
            out.add(key)
    return out


def orbit(key):
    rows = graph(key)
    n = len(key[0])
    fixed = tuple(i ^ 1 for i in range(n))
    neighbors = [[j for j in range(3*n) if rows[i] >> j & 1] for i in range(3*n)]
    out = set()
    autos = {}
    for order in permutations(range(3)):
        for first in permutations(range(order[0]*n, (order[0]+1)*n)):
            if any(not (rows[first[i]] >> first[i ^ 1] & 1) for i in range(n)):
                continue
            old = list(first)
            for layer in order[1:]:
                old.extend(next(w for w in neighbors[v] if w//n == layer) for v in first)
            renumber = {v: i for i, v in enumerate(old)}
            mates = [tuple(renumber[next(w for w in neighbors[v] if w//n == v//n)] % n
                           for v in old[layer*n:(layer+1)*n]) for layer in range(3)]
            cross = tuple(renumber[next(w for w in neighbors[v] if w//n == order[2])] % n
                          for v in old[n:2*n])
            mapped = tuple(mates)+(cross,)
            assert mapped[0] == fixed
            out.add(mapped)
            if mapped == key:
                autos.setdefault(order, [renumber[i] for i in range(3*n)])
    return out, autos


def kernel7(matrix):
    a = np.array(matrix, dtype=np.int64) % 7
    rank = 0
    pivots = []
    for col in range(a.shape[1]):
        available = np.flatnonzero(a[rank:, col])
        if not len(available):
            continue
        pivot = rank+int(available[0])
        a[[rank, pivot]] = a[[pivot, rank]]
        a[rank] = a[rank]*pow(int(a[rank, col]), -1, 7) % 7
        for i in range(a.shape[0]):
            if i != rank:
                a[i] = (a[i]-a[i, col]*a[rank]) % 7
        pivots.append(col)
        rank += 1
    basis = []
    for col in sorted(set(range(a.shape[1]))-set(pivots)):
        v = np.zeros(a.shape[1], dtype=np.int64)
        v[col] = 1
        v[pivots] = -a[:rank, col] % 7
        basis.append(v)
    return basis


def torsion_obstruction(key):
    rows = graph(key)
    a = np.array([[(rows[u] >> v) & 1 for v in range(18)] for u in range(18)], dtype=np.int64)
    h = 3*np.eye(18, dtype=np.int64)-a
    basis = kernel7(np.vstack([h, np.ones(18, dtype=np.int64)]))
    t = len(basis)
    if not t:
        return {'torsion': 0}
    triples = []
    for s in combinations(range(18), 3):
        if len({v//6 for v in s}) == 1:
            continue
        if any(u//6 == v//6 and a[u, v] for u, v in combinations(s, 2)):
            continue
        if sum(a[u, v] for u, v in combinations(s, 2)) > 1:
            continue
        if np.any(a[:, s].sum(axis=1) > 2):
            continue
        triples.append(s)
    masks = np.zeros((len(triples), 18), dtype=np.int64)
    for i, s in enumerate(triples):
        masks[i, list(s)] = 1
    layer = np.arange(18)//6
    k = 12*np.eye(18, dtype=np.int64)-a-a@a+2-(layer[:, None] == layer[None, :])
    minimum, count = 153, 0
    for coef in product(range(7), repeat=t):
        if not any(coef) or next(x for x in coef if x) != 1:
            continue
        phi = np.array(coef) @ np.array(basis) % 7
        balanced = masks[(masks @ phi) % 7 == 0]
        counts = balanced.T @ balanced
        bad = sum(counts[u, v] < k[u, v] for u, v in combinations(range(18), 2))
        assert bad > 0
        minimum = min(minimum, bad)
        count += 1
    return {'torsion': t, 'triples': len(triples), 'projective_vectors': count,
            'minimum_deficient_pairs': int(minimum)}


def audit_logs(source, types):
    free = [i for i, t in enumerate(types) if t['torsion'] == 0]
    one = [i for i, t in enumerate(types) if t['torsion'] == 1]
    pattern = re.compile(r'^(?:(00|01u|10u|11) )?(\d+) (\d+) rho=(\d+) u=(\d+) c0=(\d+)(?: lam=(\d+))?.*?items (\d+).*?nodes (\d+) solutions (\d+) timeout (\d+)')
    results = {}
    for case, filename in [('00', 'sweep66.log'), ('01u', 'sweep_01u.log'), ('10u', 'sweep_10u.log'), ('11', 'sweep_11.log')]:
        found = {}
        for line in (source/filename).read_text().splitlines():
            m = pattern.search(line)
            assert m, line
            tag, i, j, rho, u, c0, lam, items, nodes, solutions, timeout = m.groups()
            assert tag in (None, case)
            key = tuple(map(int, (i, j, rho, u, c0, lam or '1')))
            assert key not in found
            assert int(solutions) == int(timeout) == 0
            assert int(items) < (40000 if case == '00' else 400000)
            assert int(nodes) < 20000000000
            found[key] = int(nodes)
        if case == '00':
            expected = set(product(free, free, range(6), [0], [1, 3], [1]))
        elif case == '01u':
            expected = set(product(free, one, range(6), [0], [1], [1]))
        elif case == '10u':
            expected = set(product(one, free, range(6), [0], [1], [1]))
        else:
            expected = set(product(one, one, range(6), [0], [1, 3], range(1, 7)))
        assert set(found) == expected
        results[case] = {'runs': len(found), 'reported_nodes': sum(found.values()),
                         'max_reported_nodes': max(found.values()), 'complete_parameter_grid': True}
    return results


def high_torsion_input(key, u):
    rows = graph(key)
    component = np.array([[(rows[i] >> j) & 1 for j in range(18)] for i in range(18)], dtype=np.int64)
    a = np.zeros((36, 36), dtype=np.int64)
    a[:18, :18] = a[18:, 18:] = component
    layer = np.tile(np.arange(18)//6, 2)
    same_layer = layer[:, None] == layer[None, :]
    k = 12*np.eye(36, dtype=np.int64)-a-a@a+2-same_layer
    basis = np.array(kernel7(np.vstack([3*np.eye(18, dtype=np.int64)-component,
                                       np.ones(18, dtype=np.int64)])))
    domains = []
    for ell in range(3):
        domains.append([p for p in combinations(np.flatnonzero(layer == ell), 2)
                        if not a[p[0], p[1]] and (ell != layer[u] or u in p)])
    incidence = []
    for parts in product(*domains):
        support = tuple(v for p in parts for v in p)
        if sum(v < 18 for v in support) != 3:
            continue
        n = np.zeros(36, dtype=np.int64)
        n[list(support)] = 1
        if np.any(a @ n > 2-n):
            continue
        if any(k[i, j] == 0 for i, j in combinations(support, 2)):
            continue
        incidence.append(n)
    incidence = np.array(incidence)
    sig1 = incidence[:, :18] @ basis.T % 7
    sig2 = incidence[:, 18:] @ basis.T % 7
    # Matrix codes in the archive use the basis obtained from ker(H), then
    # subtracting each vector's mean and keeping independent vectors in order.
    # Reconstruct that coordinate convention using our own linear algebra.
    h = 3*np.eye(18, dtype=np.int64)-component
    reference = []
    for v in kernel7(h):
        w = (v-2*int(v.sum())) % 7
        if np.any(w) and not kernel7(np.array(reference+[w]).T):
            reference.append(w)
    coordinates = {tuple(np.array(coef) @ basis % 7): coef for coef in product(range(7), repeat=3)}
    change = np.array([coordinates[tuple(v)] for v in reference])
    assert np.array_equal(change @ basis % 7, reference)
    assert not kernel7(change)
    sig1 = sig1 @ change.T % 7
    sig2 = sig2 @ change.T % 7
    return incidence, sig1, sig2, k[:, u]


def independent_cover(incidence, demand, u):
    supports = [tuple(np.flatnonzero(row)) for row in incidence]
    masks = [sum(1 << int(v) for v in support) for support in supports]
    incompatible = [set(j for j, mj in enumerate(masks) if (mi & mj).bit_count() > 2)
                    for mi in masks]
    remaining = [int(x) for x in demand]
    remaining[u] = 0
    nodes = 0
    def dfs(pool, chosen):
        nonlocal nodes
        nodes += 1
        if len(chosen) == 10:
            return chosen if not any(remaining) else None
        columns = [i for i, d in enumerate(remaining) if d]
        choices = [(v, [j for j in pool if v in supports[j]]) for v in columns]
        if any(len(options) < remaining[v] for v, options in choices):
            return None
        if not choices:
            return None
        _, choices_at_pivot = min(choices, key=lambda item: len(item[1]))
        for j in choices_at_pivot:
            for v in supports[j]:
                if v != u:
                    remaining[v] -= 1
            next_pool = [i for i in pool if i != j and i not in incompatible[j]
                         and all(v == u or remaining[v] > 0 for v in supports[i])]
            answer = dfs(next_pool, chosen+[j])
            for v in supports[j]:
                if v != u:
                    remaining[v] += 1
            if answer is not None:
                return answer
        return None
    selected = dfs(list(range(len(supports))), [])
    if selected is not None:
        assert len(selected) == len(set(selected)) == 10
        assert np.array_equal(incidence[selected].sum(axis=0), demand)
        assert all((masks[i] & masks[j]).bit_count() <= 2 for i, j in combinations(selected, 2))
    return selected, nodes


def audit_last_gl_step(source, key):
    # high_torsion_input explicitly translates our basis to the archive convention.
    incidence, sig1, sig2, demand = high_torsion_input(key, 6)
    good1 = [int(x) for x in (source/'good_after_1.txt').read_text().split()]
    outcomes = []
    for code in good1:
        m = np.array([(code//(7**i)) % 7 for i in range(9)], dtype=np.int64).reshape((3, 3))
        selected = np.all((sig1+sig2 @ m.T) % 7 == 0, axis=1)
        family, nodes = independent_cover(incidence[selected], demand, 6)
        outcomes.append({'matrix_code': code, 'balanced_candidates': int(selected.sum()),
                         'nodes': nodes, 'family_found': family is not None})
    assert not any(r['family_found'] for r in outcomes)
    # A real combinatorial family at u=1 must be found for a retained matrix.
    positive_incidence, s1, s2, positive_demand = high_torsion_input(key, 1)
    good0 = [int(x) for x in (source/'good_u0.txt').read_text().split()]
    rebuilt_good1 = []
    total_nodes = 0
    for matrix_code in good0:
        mm = np.array([(matrix_code//(7**i)) % 7 for i in range(9)], dtype=np.int64).reshape((3, 3))
        keep = np.all((s1+s2 @ mm.T) % 7 == 0, axis=1)
        witness, used = independent_cover(positive_incidence[keep], positive_demand, 1)
        total_nodes += used
        if witness is not None:
            rebuilt_good1.append(matrix_code)
    assert rebuilt_good1 == good1
    code = good1[0]
    m = np.array([(code//(7**i)) % 7 for i in range(9)], dtype=np.int64).reshape((3, 3))
    selected = np.all((s1+s2 @ m.T) % 7 == 0, axis=1)
    family, nodes = independent_cover(positive_incidence[selected], positive_demand, 1)
    assert family is not None
    return {'input_candidates': len(incidence), 'outcomes': outcomes,
            'intermediate_step': {'vertex': 1, 'input_matrices': len(good0),
                                  'surviving_matrices': rebuilt_good1, 'total_nodes': total_nodes,
                                  'matches_archived_list_exactly': True},
            'positive_control': {'vertex': 1, 'matrix_code': code, 'nodes': nodes,
                                 'shadows': [np.flatnonzero(row).tolist()
                                             for row in positive_incidence[selected][family]]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    types = json.loads((args.source/'comp66_types.json').read_text())
    keys = [tuple(tuple(x) for x in t['key']) for t in types]
    report = {'scope': 'independent finite ingredients and archived coverage, not full search replay',
              'upstream_commit': '15a3cfe3f6ccaa68c5e862d745a3a60558f60626',
              'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in sorted(args.source.iterdir()) if p.is_file() and p.suffix in ('.py', '.c', '.json', '.log', '.out', '.txt', '.md')},
              'small_components': {str(n): len(enumerate_normal(n)) for n in (2, 4)}}
    assert report['small_components'] == {'2': 0, '4': 0}
    all_normal = enumerate_normal(6)
    covered = set()
    component_reports = []
    for i, key in enumerate(keys):
        images, autos = orbit(key)
        assert not covered.intersection(images)
        assert len(images) == types[i]['mult']
        covered.update(images)
        item = torsion_obstruction(key)
        assert item['torsion'] == types[i]['torsion']
        item.update(type=i, normal_forms=len(images))
        if item['torsion'] == 3:
            assert len(autos) == 6
            item['layer_automorphisms'] = [{'order': list(order), 'permutation': p} for order, p in autos.items()]
        component_reports.append(item)
    assert covered == all_normal and len(all_normal) == 288
    report['components'] = component_reports
    report['labelled_normal_forms'] = len(all_normal)
    report['archived_star_search_logs'] = audit_logs(args.source, types)
    good0 = [int(x) for x in (args.source/'good_u0.txt').read_text().split()]
    good1 = [int(x) for x in (args.source/'good_after_1.txt').read_text().split()]
    assert len(good0) == len(set(good0)) == 25588
    assert len(good1) == len(set(good1)) == 44 and set(good1) <= set(good0)
    for code in good0:
        m = np.array([(code//(7**i)) % 7 for i in range(9)], dtype=np.int64).reshape((3, 3))
        assert not kernel7(m)
    report['gl3_archived_lists'] = {'u0': len(good0), 'u1': len(good1),
                                   'all_listed_matrices_invertible': True,
                                   'entire_gl3_search_replayed': False}
    report['gl3_last_step_independent'] = audit_last_gl_step(args.source, keys[5])
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('source_sha256', 'gl3_last_step_independent')}))
    print('GL3 steps independently reproduced: 25588 -> 44 -> 0; positive family at u=1 verified')


if __name__ == '__main__':
    main()
