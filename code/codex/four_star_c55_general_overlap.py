"""Small active-component reductions for c55 without assuming G1.

Only own finite two-star patterns are generated. No producer seeds read.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path
import sys

import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_star_profile_join import boundary, residual, upper_entry
from three_star_ambient_upper import psd_or_witness
from three_star_column_domains import k8


TWO_LABELS = tuple((a, x) for a in (0, 1) for x in range(2, 14))
MATCHINGS = ((1, 0, 3, 2), (2, 3, 0, 1), (3, 2, 1, 0))
CORE = ((0, 2), (0, 3), (1, 2), (1, 3),
        (0, 4), (0, 5), (1, 4), (1, 5),
        (2, 6), (2, 7), (3, 6), (3, 7))


def two_star_catalogue():
    index = {p: i for i, p in enumerate(TWO_LABELS)}
    accepted = []
    for ta, tb, sigma in product(MATCHINGS, MATCHINGS, permutations(range(4))):
        adjacency = [set((x ^ 1, ta[x], tb[x], sigma[x])) for x in range(4)]
        for x in range(4):
            adjacency[sigma[x]].add(x)
        seen, pending = {0}, [0]
        while pending:
            for x in adjacency[pending.pop()]-seen:
                seen.add(x)
                pending.append(x)
        if len(seen) != 4:
            continue
        gamma = [[0]*24 for _ in range(24)]
        for a, tau in ((0, ta), (1, tb)):
            for x in range(2, 14):
                y = tau[x-2]+2 if x < 6 else x ^ 1
                gamma[index[a, x]][index[a, y]] = 1
        for x in range(2, 14):
            y = sigma[x-2]+2 if x < 6 else x
            gamma[index[0, x]][index[1, y]] = gamma[index[1, y]][index[0, x]] = 1
        r = residual(boundary(gamma, TWO_LABELS))
        if any(v < 0 for row in r for v in row) or any(v for row in r[:3] for v in row):
            continue
        overlap = [index[p] for p in CORE[:4]]
        count = sum(gamma[i][j] for i, j in combinations(overlap, 2))
        accepted.append(dict(ta=ta, tb=tb, sigma=sigma, overlap_edges=count, gamma=gamma))
    return accepted


def investigate(overlap_edges=3):
    catalogue = two_star_catalogue()
    cases = [row for row in catalogue if row['overlap_edges'] == overlap_edges]
    remap = {0: 2, 1: 3, 2: 0, 3: 1, 4: 6, 5: 7, 6: 4, 7: 5,
             **{i: i for i in range(8, 14)}}
    left_index = {p: i for i, p in enumerate(TWO_LABELS)}
    right_index = {tuple(sorted(remap[x] for x in p)): i for i, p in enumerate(TWO_LABELS)}
    counts = Counter()
    witnesses = []
    core_k = sp.Matrix(12, 12, lambda i, j: k8(CORE[i], CORE[j]))
    relation_left = sp.Matrix([1]*8+[0]*4)
    relation_right = sp.Matrix([1]*4+[0]*4+[1]*4)
    for li, left in enumerate(cases):
        for ri, right in enumerate(cases):
            gamma = [[0]*12 for _ in range(12)]
            consistent = True
            for i, j in combinations(range(12), 2):
                p, q = CORE[i], CORE[j]
                values = []
                if p in left_index and q in left_index:
                    values.append(left['gamma'][left_index[p]][left_index[q]])
                if p in right_index and q in right_index:
                    values.append(right['gamma'][right_index[p]][right_index[q]])
                if len(set(values)) > 1:
                    consistent = False
                    break
                if values:
                    gamma[i][j] = gamma[j][i] = values[0]
            if not consistent:
                continue
            counts['compatible_line_pairs'] += 1
            # The quotient kernel forces e(LA,RB)=4-4*t=2*e(O)-4.
            cross_count = 2*overlap_edges-4
            for cross_edges in combinations(list(product(range(4, 8), range(8, 12))), cross_count):
                current = [row[:] for row in gamma]
                for i, j in cross_edges:
                    current[i][j] = current[j][i] = 1
                m8 = 24*sp.eye(12)-8*sp.Matrix(current)-core_k
                if any(m8*relation_left) or any(m8*relation_right):
                    continue
                counts['core_kernel_compatible'] += 1
                r = residual(boundary(current, CORE))
                if any(v < 0 for row in r for v in row):
                    continue
                counts['core_capacity_compatible'] += 1
                t = psd_or_witness(m8)
                record = dict(left_index=li, right_index=ri, cross_edges=cross_edges,
                              T=t)
                if t['psd']:
                    counts['T_psd'] += 1
                    n15 = sp.Matrix(12, 12, lambda i, j:
                                    upper_entry(CORE[i], CORE[j], current[i][j], i == j))
                    u = psd_or_witness(n15)
                    record['U'] = u
                    if u['psd']:
                        counts['T_U_psd'] += 1
                        record['rank_T'] = m8.rank()
                witnesses.append(record)
    return dict(status='EXACT_ACTIVE_CORE_CATALOGUE_WITHOUT_G1',
                overlap_edges=overlap_edges, labels=CORE,
                total_single_line_patterns=len(catalogue),
                single_line_overlap_histogram=dict(Counter(r['overlap_edges'] for r in catalogue)),
                selected_line_patterns=[{k: v for k, v in r.items() if k != 'gamma'} for r in cases],
                counts=dict(counts), certificates=witnesses,
                scope='Necessary 12-label core tests only; no completion of the whole44-label border asserted.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--overlap-edges', type=int, choices=(2, 3), default=3)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    result = investigate(a.overlap_edges)
    path = Path(a.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in ('selected_line_patterns', 'certificates', 'labels')}))
