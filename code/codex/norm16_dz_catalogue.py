"""Exact local D--Z catalogue, quotienting only automorphisms of Z.

Uses saved core attachments, degree identities and all common-neighbour
upper bounds on core+D+Z. Counts are NOT counts of SRG completions.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import time

import networkx as nx

ROOT = Path(__file__).resolve().parents[2]


def catalogue(attachment, forest, seconds=30, limit=0):
    if forest['edges_D']:
        raise ValueError('First catalogue pilot: D independent only.')
    az = forest['adjacency_Z']
    graph = nx.Graph()
    graph.add_nodes_from(range(11))
    graph.add_edges_from((i, j) for i in range(11) for j in range(i+1, 11) if az[i][j])
    autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
    zrows = [sum(1 << j for j, value in enumerate(row) if value) for row in az]
    pairs = list(combinations(range(11), 2))
    pair_masks = [(1 << i) | (1 << j) for i, j in pairs]
    masks = [sum(1 << z for z in row) for row in combinations(range(11), 4)]
    masks = [m for m in masks
             if sum(sum(az[z]) for z in range(11) if m >> z & 1) <= 6
             and all((m & zrows[z]).bit_count() <= 2-(m >> z & 1)
                     for z in range(11))]
    nmask = len(masks)
    index = {m: i for i, m in enumerate(masks)}
    mask_vertices = [[z for z in range(11) if m >> z & 1] for m in masks]
    row_pairs = [[k for k, pair in enumerate(pair_masks) if m & pair == pair] for m in masks]
    pair_contains = [sum(1 << j for j, m in enumerate(masks) if m & p == p) for p in pair_masks]
    col_contains = [sum(1 << j for j, m in enumerate(masks) if m >> z & 1) for z in range(11)]
    compatible = [[sum(1 << j for j, m2 in enumerate(masks) if (m & m2).bit_count() <= cap)
                   for m in masks] for cap in range(3)]
    images = [[index[sum(1 << auto[z] for z in vertices)] for vertices in mask_vertices]
              for auto in autos]
    core_sets = [set(row[:2]) | {8+q for q in row[2:]} for row in attachment]
    cap_d = [[2-len(u & v) for v in core_sets] for u in core_sets]
    cap_z = [2-az[i][j]-(zrows[i] & zrows[j]).bit_count() for i, j in pairs]
    degrees = [2+sum(row) for row in az]
    initial = (1 << nmask)-1
    for k, cap in enumerate(cap_z):
        if cap == 0:
            initial &= ~pair_contains[k]
    nodes = count = 0
    examples = []
    start = time.monotonic()
    stopped = False

    def visit(domains, left, columns, pair_left, group, chosen):
        nonlocal nodes, count, stopped
        nodes += 1
        if nodes & 1023 == 0 and time.monotonic()-start > seconds:
            stopped = True
            return
        if not left:
            assert not any(columns)
            count += 1
            if len(examples) < 3:
                examples.append(chosen[:])
            if limit and count >= limit:
                stopped = True
            return
        # The choice of labelled D row is invariant under Z automorphisms.
        d = min(left, key=lambda i: (domains[i].bit_count(), i))
        domain = domains[d]
        if not domain:
            return
        new_left = [i for i in left if i != d]
        while domain and not stopped:
            low = domain & -domain
            j = low.bit_length()-1
            domain -= low
            m = masks[j]
            stabilizer = []
            canonical = True
            for auto in group:
                target = images[auto][j]
                if masks[target] < m:
                    canonical = False
                    break
                if target == j:
                    stabilizer.append(auto)
            if not canonical:
                continue
            new_columns = columns[:]
            for z in mask_vertices[j]:
                new_columns[z] -= 1
            if any(c < 0 or c > len(new_left) for c in new_columns):
                continue
            new_pairs = pair_left[:]
            forbidden = 0
            for k in row_pairs[j]:
                new_pairs[k] -= 1
                if new_pairs[k] == 0:
                    forbidden |= pair_contains[k]
            assert min(new_pairs) >= 0
            required = (1 << nmask)-1
            for z, c in enumerate(new_columns):
                if c == 0:
                    forbidden |= col_contains[z]
                elif c == len(new_left):
                    required &= col_contains[z]
            nd = domains[:]
            for i in new_left:
                nd[i] &= compatible[cap_d[d][i]][j] & ~forbidden & required
            if any(not nd[i] for i in new_left):
                continue
            # Column capacities after all current pair restrictions.
            good = True
            for z, need in enumerate(new_columns):
                upper = sum(bool(nd[i] & col_contains[z]) for i in new_left)
                lower = sum(not (nd[i] & ~col_contains[z]) for i in new_left)
                if not lower <= need <= upper:
                    good = False
                    break
            if not good:
                continue
            chosen[d] = m
            visit(nd, new_left, new_columns, new_pairs, stabilizer, chosen)
            chosen[d] = -1

    visit([initial]*8, list(range(8)), degrees, cap_z, list(range(len(autos))), [-1]*8)
    return {'status': 'STOPPED' if stopped else 'EXHAUSTED', 'count_mod_Aut_Z': count,
            'nodes': nodes, 'seconds_search': time.monotonic()-start,
            'row_domain_size': nmask, 'Aut_Z': len(autos), 'example_row_masks': examples,
            'scope': __doc__}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=int, default=0)
    parser.add_argument('--orbit', type=int, default=0)
    parser.add_argument('--forest', type=int, default=2)
    parser.add_argument('--seconds', type=float, default=20)
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--write-instance', help='Only write the compact input for the C++ counter')
    args = parser.parse_args()
    cases = json.loads((ROOT/'data/codex_norm16_attachments_rank.json').read_text())['cases']
    forests = json.loads((ROOT/'data/codex_norm16_far_forest.json').read_text())['forests']
    attachment = cases[args.case]['orbits'][args.orbit]['representative']
    forest = next(f for f in forests if f['id'] == args.forest)
    if args.write_instance:
        if forest['edges_D']:
            raise ValueError('The current counter is for D independent.')
        az = forest['adjacency_Z']
        graph = nx.Graph()
        graph.add_nodes_from(range(11))
        graph.add_edges_from((i, j) for i in range(11) for j in range(i+1, 11) if az[i][j])
        autos = list(nx.algorithms.isomorphism.GraphMatcher(graph, graph).isomorphisms_iter())
        lines = [' '.join(str(sum(1 << j for j, v in enumerate(row) if v)) for row in az),
                 ' '.join(str(sum(1 << p for p in row[:2])+sum(1 << (8+q) for q in row[2:]))
                          for row in attachment), str(len(autos))]
        lines += [' '.join(str(auto[z]) for z in range(11)) for auto in autos]
        (ROOT/args.write_instance).write_text('\n'.join(lines)+'\n', encoding='ascii')
        print(json.dumps({'file': args.write_instance, 'Aut_Z': len(autos)}))
        raise SystemExit(0)
    result = catalogue(attachment, forest, args.seconds, args.limit)
    result.update({'case': args.case, 'orbit': args.orbit, 'forest': args.forest})
    target = ROOT/f'data/codex_norm16_dz_count_{args.case}_{args.orbit}_{args.forest}.json'
    target.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)
