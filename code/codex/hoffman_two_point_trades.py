"""Explore exact two-point incidence trades, then test new designs globally.

A selection of a-only and b-only blocks may swap a and b iff its residual
incidence sums agree at all other points. This preserves every pair count.
The empty selection and the full point relabelling are omitted. No graph
automorphism or Seidel-rank condition is imposed.
"""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/codex_hoffman_trades'
sys.path.insert(0, str(ROOT.parent / 'c1-audit-deps'))
import igraph as ig


def design_key(blocks):
    graph = ig.Graph(n=99, edges=[(x, 22+i) for i, b in enumerate(blocks) for x in b])
    colors = [0]*22 + [1]*77
    perm = graph.canonical_permutation(color=colors)
    edges = tuple(sorted(tuple(sorted(e)) for e in graph.permute_vertices(perm).get_edgelist()))
    return hashlib.sha256(repr(edges).encode()).hexdigest(), graph.count_automorphisms(color=colors)


def verify(blocks):
    assert len(blocks) == len(set(blocks)) == 77
    assert Counter(x for b in blocks for x in b) == Counter({x: 14 for x in range(22)})
    assert Counter(p for b in blocks for p in combinations(b, 2)) == Counter({p: 2 for p in combinations(range(22), 2)})
    assert all(len(set(b) & set(c)) <= 2 for b, c in combinations(blocks, 2))


def subset_sums(values):
    sums = [0]*(1 << len(values))
    for mask in range(1, len(sums)):
        bit = mask & -mask
        sums[mask] = sums[mask ^ bit] + values[bit.bit_length()-1]
    return sums


def trades(blocks, a, b):
    left = [i for i, block in enumerate(blocks) if a in block and b not in block]
    right = [i for i, block in enumerate(blocks) if b in block and a not in block]
    assert len(left) == len(right) == 12
    # Each residual point occurs at most twice; radix 3 encodes vectors without carry.
    weights = [3**x for x in range(22)]
    ls = subset_sums([sum(weights[x] for x in blocks[i] if x != a) for i in left])
    rs = subset_sums([sum(weights[x] for x in blocks[i] if x != b) for i in right])
    by_sum = defaultdict(list)
    for mask, signature in enumerate(rs):
        by_sum[signature].append(mask)
    for lm, signature in enumerate(ls):
        if lm == 0 or lm == len(ls)-1:
            continue
        for rm in by_sum.get(signature, []):
            selected = [i for bit, i in enumerate(left) if lm >> bit & 1]
            selected += [i for bit, i in enumerate(right) if rm >> bit & 1]
            changed = list(blocks)
            for i in selected:
                changed[i] = tuple(sorted(b if x == a else a if x == b else x for x in blocks[i]))
            changed = tuple(sorted(changed))
            if len(set(changed)) != 77:
                yield None, selected
                continue
            if any(len(set(x) & set(y)) > 2 for x, y in combinations(changed, 2)):
                yield None, selected
                continue
            yield changed, selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', type=int, default=1)
    parser.add_argument('--generations', type=int, default=1)
    parser.add_argument('--max-designs', type=int, default=200)
    args = parser.parse_args()
    start = time.monotonic()
    source = json.loads((OUT / 'cyclic_designs22.json').read_text())['designs']
    seen = set()
    frontier = []
    for i, item in enumerate(source[:args.seeds]):
        blocks = tuple(tuple(b) for b in item['blocks'])
        key, order = design_key(blocks)
        seen.add(key)
        frontier.append(dict(blocks=blocks, key=key, aut=order, seed=i, generation=0))
    found = []
    seed_records = list(frontier)
    totals = Counter()
    for generation in range(1, args.generations+1):
        next_frontier = []
        for parent in frontier:
            # Cyclic seeds: translation makes a=0 covering. Mutants have no imposed symmetry.
            pairs = [(0, b) for b in range(1, 22)] if parent['generation'] == 0 else combinations(range(22), 2)
            for a, b in pairs:
                totals['point_pairs'] += 1
                for blocks, selected in trades(parent['blocks'], a, b):
                    totals['nontrivial_labelled_selections'] += 1
                    if blocks is None:
                        totals['intersection_rejections'] += 1
                        continue
                    key, order = design_key(blocks)
                    if key in seen:
                        totals['known_design_class'] += 1
                        continue
                    verify(blocks)
                    seen.add(key)
                    item = dict(blocks=blocks, key=key, aut=int(order), seed=parent['seed'],
                                generation=generation, parent=parent['key'], pair=[a,b],
                                switched_block_indices=selected, volume=len(selected))
                    found.append(item)
                    next_frontier.append(item)
                    print(json.dumps({k: v for k, v in item.items() if k != 'blocks'}), flush=True)
                    if len(found) >= args.max_designs:
                        break
                if len(found) >= args.max_designs:
                    break
            if len(found) >= args.max_designs:
                break
        frontier = next_frontier
        if not frontier or len(found) >= args.max_designs:
            break
    result = dict(arguments=vars(args), counts=dict(totals), seeds=seed_records, new_designs=found,
                  elapsed_seconds=time.monotonic()-start,
                  status='CAPPED' if len(found) >= args.max_designs else 'EXHAUSTED_REQUESTED_NEIGHBOURHOOD',
                  scope='Two-point trades from specified seeds; not a global design census or SRG construction')
    (OUT / 'two_point_trades.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('new_designs','seeds')}), flush=True)
    print('New isomorphism classes:', len(found), 'automorphism orders:', dict(Counter(x['aut'] for x in found)))


if __name__ == '__main__':
    main()
