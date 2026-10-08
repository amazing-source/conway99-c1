"""Exact checks for note210: local relations and admissible component triples.

Enumerate the 700 normalized systems containing a K3,3 block component,
and reconstruct all 288 labelled girth-five-or-more near components.
No design solver is used here.
"""
import argparse
from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path

from local_component_space import component_vector
from grid_kernel_rank_obstruction import rank_pivots
from grid_vertex_relations import PAIRS, ball_image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/codex_component66_local_audit.json"


def graph_components(adj):
    done, result = set(), []
    for start in range(len(adj)):
        if start in done:
            continue
        colors = {start: 1}
        queue = [start]
        bipartite = True
        for i in queue:
            for j in adj[i]:
                if j not in colors:
                    colors[j] = -colors[i]
                    queue.append(j)
                elif colors[j] == colors[i]:
                    bipartite = False
        done.update(colors)
        result.append((colors, bipartite))
    return result


def splits(six):
    # Unordered 3+3 partitions, with a deterministic first block.
    for tail in combinations(six[1:], 2):
        first = {six[0], *tail}
        yield first, set(six)-first


def local_audit():
    systems = 0
    shapes = Counter()
    for omitted in range(7):
        rest = [i for i in range(7) if i != omitted]
        for left, right in splits(rest):
            for missing_split in splits(rest):
                blocks = []
                for i in range(7):
                    if i == omitted:
                        blocks.append(missing_split)
                    else:
                        first = right if i in left else left
                        blocks.append((first, set(range(7))-{i}-first))
                adj = [set() for _ in range(14)]
                incidence = [[0]*21 for _ in range(14)]
                for e, (i, j) in enumerate(PAIRS):
                    a = 2*i+int(j not in blocks[i][0])
                    b = 2*j+int(i not in blocks[j][0])
                    adj[a].add(b)
                    adj[b].add(a)
                    incidence[a][e] = incidence[b][e] = 1
                assert all(len(row) == 3 for row in adj)
                components = graph_components(adj)
                bip = [colors for colors, flag in components if flag]
                assert len(bip) == 1 and len(bip[0]) == 6
                assert rank_pivots(incidence)[0] == 13
                shapes[tuple(sorted(len(colors) for colors, _ in components))] += 1
                # Build the unique local coefficient relation as an
                # exact integer (A+4I)y identity in the 99 coordinates.
                x = [bip[0].get(i, 0) for i in range(14)]
                coeff = [x[2*i]-x[2*i+1] for i in range(7)]
                z = [-x[2*i]-x[2*i+1] for i in range(7)]
                assert sum(z) == 0
                hs = []
                for i in range(7):
                    a = component_vector(i, blocks[i][0])
                    b = component_vector(i, blocks[i][1])
                    h = [u-v for u, v in zip(a, b)]
                    assert sum(h) == 0 and sum(v*v for v in h) == 36
                    hs.append(h)
                combined = [sum(coeff[i]*hs[i][j] for i in range(7)) for j in range(99)]
                assert combined == ball_image(0, z)
                systems += 1
    assert systems == 700
    return {"normalized_K33_systems": systems, "bipartite_components_in_each": 1,
            "component_order_histogram": {str(k): v for k, v in sorted(shapes.items())},
            "integer_relations_checked": systems, "component_difference_norm": 36}


def matchings(labels):
    if not labels:
        yield {}
        return
    i = labels[0]
    for j in labels[1:]:
        if j == i ^ 1:
            continue
        for rest in matchings([a for a in labels if a not in (i, j)]):
            yield {**rest, i: j, j: i}


def triple_audit():
    labels = list(range(6))
    mates = list(matchings(labels))
    checked = 0
    histogram = Counter()
    for mb in mates:
        for mc in mates:
            for sigma in permutations(labels):
                if any(sigma[i] in (i, i ^ 1, mb[i], mc[i]) for i in labels):
                    continue
                if any(mc[sigma[i]] == sigma[mb[i]] for i in labels):
                    continue
                adj = [set() for _ in range(18)]

                def edge(i, j):
                    adj[i].add(j)
                    adj[j].add(i)

                for i in labels:
                    edge(i, i ^ 1)
                    edge(6+i, 6+mb[i])
                    edge(12+i, 12+mc[i])
                    edge(i, 6+i)
                    edge(i, 12+i)
                    edge(6+i, 12+sigma[i])
                assert all(len(row) == 3 for row in adj)
                assert len(graph_components(adj)) == 1
                assert all(len(adj[i] & adj[j]) <= (0 if j in adj[i] else 1)
                           for i, j in combinations(range(18), 2))
                k = [[12*int(i == j)-int(j in adj[i])+2-len(adj[i] & adj[j])-int(i//6 == j//6)
                      for j in range(18)] for i in range(18)]
                assert all(k[i][i] == 10 and sum(k[i])-10 == 20 for i in range(18))
                old = []
                for triple in combinations(range(18), 3):
                    if any(sum(i//6 == layer for i in triple) > 2 for layer in range(3)):
                        continue
                    if any(k[i][j] < 1 for i, j in combinations(triple, 2)):
                        continue
                    if sum(j in adj[i] for i, j in combinations(triple, 2)) > 1:
                        continue
                    old.append(frozenset(triple))
                rejected = {t for t in old if any(len(adj[i] & t) > 2-int(i in t) for i in range(18))}
                neighborhoods = {frozenset(row) for row in adj}
                assert len(old) == 630 and len(neighborhoods) == 18
                assert rejected == neighborhoods
                histogram[(len(old), len(old)-len(rejected))] += 1
                checked += 1
    assert checked == 288
    return {"labelled_components_checked": checked,
            "candidate_count_histogram_before_after": {str(k): v for k, v in sorted(histogram.items())},
            "rejected_candidates": "exactly the 18 distinct cubic neighborhoods in every component"}


def audit():
    return {"local_relations": local_audit(), "integer_shadow_filter": triple_audit(),
            "scope": "finite verifications supporting the hand proofs of note210; no complete designs solved"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.verify_only:
        assert json.loads(OUT.read_text(encoding="utf-8")) == result
    else:
        OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
