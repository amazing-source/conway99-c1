"""Finite necessary component templates when all seven root lines have c>=4.

The enumeration covers all 2^21 labelled simple graphs, uses only degree-
preserving permutations to remove duplicates, and retains every splitting
of a degree-four vertex into two component pairs. No external graph atlas.
This is a quotient of a hypothetical SRG, not an enumeration of SRGs.
"""

import argparse
from collections import Counter, defaultdict
from itertools import combinations, permutations, product
import json
from pathlib import Path
import time

EDGES = tuple(combinations(range(7), 2))
EDGE_INDEX = {e: i for i, e in enumerate(EDGES)}


def relabel(mask, permutation):
    result = 0
    for k, (a, b) in enumerate(EDGES):
        if mask & (1 << k):
            p = tuple(sorted((permutation[a], permutation[b])))
            result |= 1 << EDGE_INDEX[p]
    return result


def graph_representatives():
    """Exact cover: every graph has a labelling with nondecreasing degrees."""
    seen, representatives = set(), []
    degree, previous = [0] * 7, 0
    ordered_masks = 0
    for index in range(1 << 21):
        mask = index ^ (index >> 1)
        if index:
            changed = mask ^ previous
            k = changed.bit_length() - 1
            increment = 1 if mask & changed else -1
            a, b = EDGES[k]
            degree[a] += increment
            degree[b] += increment
        previous = mask
        if any(d not in (0, 2, 3, 4) for d in degree):
            continue
        if degree != sorted(degree):
            continue
        ordered_masks += 1
        if mask in seen:
            continue
        groups = [[i for i, d in enumerate(degree) if d == value]
                  for value in sorted(set(degree))]
        orbit = set()
        for images in product(*(permutations(group) for group in groups)):
            permutation = list(range(7))
            for group, target in zip(groups, images):
                for a, b in zip(group, target):
                    permutation[a] = b
            orbit.add(relabel(mask, permutation))
        seen.update(orbit)
        representatives.append(min(orbit))
    return sorted(representatives), ordered_masks


def splittings(neighbours):
    if not neighbours:
        return [()]
    if len(neighbours) < 4:
        return [(tuple(neighbours),)]
    a, *rest = neighbours
    return [((a, b), tuple(x for x in rest if x != b)) for b in rest]


def graph_automorphisms(mask):
    degree = [sum(bool(mask & (1 << k)) for k, e in enumerate(EDGES) if i in e)
              for i in range(7)]
    groups = [[i for i, d in enumerate(degree) if d == value]
              for value in sorted(set(degree))]
    result = []
    for images in product(*(permutations(group) for group in groups)):
        permutation = list(range(7))
        for group, target in zip(groups, images):
            for a, b in zip(group, target):
                permutation[a] = b
        if relabel(mask, permutation) == mask:
            result.append(permutation)
    return result


def canonical_groups(groups, automorphisms):
    encodings = []
    for permutation in automorphisms:
        image = [()] * 7
        for i, parts in enumerate(groups):
            image[permutation[i]] = tuple(sorted(tuple(sorted(permutation[a] for a in part))
                                                for part in parts))
        encodings.append(tuple(image))
    return min(encodings)


def component_graph(edges, groups):
    vertices, lookup = [], {}
    for root, parts in enumerate(groups):
        for part in parts:
            node = len(vertices)
            vertices.append((root, part))
            for neighbour in part:
                lookup[root, neighbour] = node
    links = [(lookup[a, b], lookup[b, a]) for a, b in edges]
    return vertices, links


def components_and_nullity(vertex_count, links, omit=None):
    adjacency = [[] for _ in range(vertex_count)]
    for i, (a, b) in enumerate(links):
        if i != omit:
            adjacency[a].append(b)
            adjacency[b].append(a)
    colours, groups = {}, []
    for start in range(vertex_count):
        if start in colours:
            continue
        colours[start] = 0
        pending, nodes, bipartite = [start], [], True
        while pending:
            a = pending.pop()
            nodes.append(a)
            for b in adjacency[a]:
                if b not in colours:
                    colours[b] = 1 - colours[a]
                    pending.append(b)
                elif colours[b] == colours[a]:
                    bipartite = False
        groups.append((sorted(nodes), bipartite))
    nullity = len(links) - int(omit is not None) - vertex_count
    nullity += sum(bipartite for _, bipartite in groups)
    return groups, nullity


def parity_chains(vertex_count, links):
    """Degree-two nodes impose v_edge1=-v_edge2 on Gram vectors."""
    incident = [[] for _ in range(vertex_count)]
    for edge, (a, b) in enumerate(links):
        incident[a].append(edge)
        incident[b].append(edge)
    relations = [[] for _ in links]
    for items in incident:
        if len(items) == 2:
            a, b = items
            relations[a].append(b)
            relations[b].append(a)
    classes, signs = {}, {}
    bad_cycle = False
    for start in range(len(links)):
        if start in classes:
            continue
        classes[start], signs[start] = start, 1
        pending = [start]
        while pending:
            a = pending.pop()
            for b in relations[a]:
                if b not in classes:
                    classes[b], signs[b] = start, -signs[a]
                    pending.append(b)
                elif signs[b] == signs[a]:
                    bad_cycle = True
    return incident, classes, signs, bad_cycle


def analyze_template(edges, groups):
    vertices, links = component_graph(edges, groups)
    components, nullity = components_and_nullity(len(vertices), links)
    forced_zero = [i for i in range(len(links))
                   if components_and_nullity(len(vertices), links, i)[1] == nullity]
    result = {"kernel_dimension": nullity,
              "bipartite_component_count": sum(b for _, b in components)}
    if forced_zero:
        return {**result, "reject": "unsigned_incidence_forces_zero_edge",
                "witness_edges": [edges[i] for i in forced_zero]}
    incident, classes, signs, bad = parity_chains(len(vertices), links)
    assert not bad
    for root in range(7):
        nodes = [i for i, (r, _) in enumerate(vertices) if r == root]
        if len(nodes) == 2:
            a, b = incident[nodes[0]][0], incident[nodes[1]][0]
            if classes[a] == classes[b]:
                return {**result, "reject": "equal_and_orthogonal_vectors",
                        "witness_root": root, "witness_edges": [edges[a], edges[b]]}
    for node, items in enumerate(incident):
        if len(items) == 3 and len({classes[e] for e in items}) < 3:
            return {**result, "reject": "repeated_direction_at_trivalent_node",
                    "witness_node": node, "witness_edges": [edges[e] for e in items]}
    return {**result, "reject": None,
            "component_graph_nodes": vertices, "component_graph_edges": links,
            "edge_direction_classes": [classes[i] for i in range(len(links))],
            "edge_direction_signs": [signs[i] for i in range(len(links))]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    representatives, ordered_count = graph_representatives()
    print(json.dumps({"nongrid_graph_representatives": len(representatives),
                      "degree_ordered_labelled_graphs": ordered_count}), flush=True)
    counts, nullities, surviving_graphs = Counter(), Counter(), set()
    survivors, canonical_seen, automorphisms = [], set(), {}
    for graph_number, mask in enumerate(representatives):
        edges = [e for i, e in enumerate(EDGES) if mask & (1 << i)]
        neighbours = [[b if a == i else a for a, b in edges if i in (a, b)] for i in range(7)]
        for choices in product(*(splittings(items) for items in neighbours)):
            result = analyze_template(edges, choices)
            counts["all_component_templates"] += 1
            nullities[result["kernel_dimension"]] += 1
            if result["reject"]:
                counts[result["reject"]] += 1
            else:
                counts["surviving_templates"] += 1
                surviving_graphs.add(mask)
                if mask not in automorphisms:
                    automorphisms[mask] = graph_automorphisms(mask)
                key = (mask, canonical_groups(choices, automorphisms[mask]))
                if key in canonical_seen:
                    continue
                canonical_seen.add(key)
                c_values = [6 if len(items) == 0 else 5 if len(items) == 2 else 4 for items in neighbours]
                survivors.append({"graph_mask": mask, "nongrid_edges": edges,
                                  "component_count_by_root_line": c_values,
                                  "nontrivial_component_groups": choices, **result})
    output = {"scope": "Necessary root component templates under c>=4 on all seven lines; not graph completions.",
              "enumerated_labelled_graph_masks": 1 << 21,
              "degree_ordered_labelled_graphs": ordered_count,
              "nongrid_graph_representatives": len(representatives),
              "surviving_graph_representatives": len(surviving_graphs),
              "counts": dict(counts), "kernel_dimension_histogram_all_templates": dict(sorted(nullities.items())),
              "surviving_component_templates_up_to_root_permutation": len(survivors),
              "elapsed_seconds": time.monotonic() - started,
              "survivors": survivors}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in output.items() if k != "survivors"}), flush=True)


if __name__ == "__main__":
    main()
