"""Test the canonical reversal of all triangles through each point.

In an SRG with lambda=1, mu=2, every non-neighbour z of x is uniquely
identified by the unordered pair N(z) intersect N(x). Any automorphism
fixing x is therefore determined by its restriction to N(x).

Swap the two neighbours on each triangle through x. This uniquely extends
to an involutory permutation of all vertices, but need not preserve edges.
This probe tests that specific, parameter-free symmetry hypothesis; it is
not a recomputation of full automorphism groups or a Conway exclusion.
"""
from pathlib import Path
from fractions import Fraction
from math import factorial
import hashlib
import json
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/codex_asymmetry_synthesis_20261014'


def probe(name, a, source=None):
    n = len(a)
    ns = [set(map(int, np.flatnonzero(a[x]))) for x in range(n)]
    defects = []
    witnesses = []
    for x in range(n):
        neighbours = ns[x]
        mate = {}
        for y in neighbours:
            common = ns[y] & neighbours
            assert len(common) == 1
            mate[y] = next(iter(common))
        far = set(range(n)) - neighbours - {x}
        labels = {z: tuple(sorted(ns[z] & neighbours)) for z in far}
        assert all(len(pair) == 2 for pair in labels.values())
        inverse = {pair: z for z, pair in labels.items()}
        assert len(inverse) == len(far)
        p = np.arange(n)
        for y in neighbours:
            p[y] = mate[y]
        for z, pair in labels.items():
            p[z] = inverse[tuple(sorted(mate[y] for y in pair))]
        assert sorted(p.tolist()) == list(range(n))
        assert np.array_equal(p[p], np.arange(n))
        assert np.count_nonzero(p == np.arange(n)) == 1
        differences = a != a[np.ix_(p, p)]
        count = int(np.count_nonzero(differences) // 2)
        defects.append(count)
        if count == 0:
            witnesses.append(x)
    unique, counts = np.unique(defects, return_counts=True)
    result = dict(name=name, vertices=n,
                  canonical_reflection_centres=witnesses,
                  centres_count=len(witnesses),
                  changed_unordered_pairs_distribution={str(int(k)): int(v)
                                                       for k, v in zip(unique, counts)})
    if source is not None:
        result['source'] = str(source.relative_to(ROOT)).replace('\\', '/')
        result['sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    return result


def read_edges(path):
    pairs = [tuple(map(int, line.split())) for line in path.read_text().splitlines()
             if line.strip() and not line.startswith('#')]
    n = max(max(pair) for pair in pairs) + 1
    a = np.zeros((n, n), dtype=np.bool_)
    for x, y in pairs:
        a[x, y] = a[y, x] = True
    return a


def main():
    start = time.monotonic()
    a = np.array([[i != j and (i // 3 == j // 3 or i % 3 == j % 3)
                   for j in range(9)] for i in range(9)], dtype=np.bool_)
    rows = [probe('Paley9', a)]
    assert rows[0]['centres_count'] == 9
    paths = [ROOT/'data/srg243/bvls243.edges',
             ROOT/'data/srg243/twin243_switched.edges',
             ROOT/'data/srg243/family/gamma3_aut864.edges',
             ROOT/'data/srg243/family/gamma4_aut3888.edges']
    paths += [OUT/'lab_sources'/name for name in
              ['new243_tricayley_Z3x4_grids25.edges', 'new243_trade_aut108.edges',
               'new243_trade_aut162.edges', 'new243_trade_aut108_b.edges']]
    for path in paths:
        row = probe(path.stem, read_edges(path), path)
        rows.append(row)
        print(json.dumps({k: row[k] for k in
                          ['name', 'centres_count', 'changed_unordered_pairs_distribution']}),
              flush=True)
    geometry = []
    for n, k, r in [(9, 4, 1), (99, 14, 3), (243, 22, 4)]:
        # Negative-eigenspace projector:
        # P = (r I - A + (k-r) J/n)/(2r+1).
        # For triangles L,M meeting in one point: 1_L^t A 1_M = 4.
        # For L=M the same expression is 6.
        constant = Fraction(9*(k-r), n*(2*r+1))
        norm2 = Fraction(3*r-6, 2*r+1) + constant
        inner = Fraction(r-4, 2*r+1) + constant
        geometry.append(dict(vertices=n, degree=k, positive_eigenvalue=r,
                             triangle_projection_norm2=str(norm2),
                             meeting_triangle_inner_product=str(inner)))
    assert geometry[1]['triangle_projection_norm2'] == '4/7'
    assert geometry[1]['meeting_triangle_inner_product'] == '0'
    assert geometry[2]['meeting_triangle_inner_product'] == '2/27'
    report = dict(scope='Canonical triangle reversal only; no full automorphism classification.',
                  graphs=rows, triangle_projection_geometry=geometry,
                  conway_star=dict(closed_star_vertices=15, far_vertices=84,
                      local_permutations=2**7*factorial(7),
                      explanation='Each far vertex is uniquely labelled by its two neighbours '
                      'in the star. All pairs from different matching edges occur once. '
                      'Every matching automorphism therefore extends uniquely to a permutation '
                      'preserving every pair meeting the closed star. Preservation of far-far '
                      'edges remains an additional condition, not a theorem.'),
                  elapsed_seconds=time.monotonic()-start)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'point_reflections.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
