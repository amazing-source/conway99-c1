"""Certify Spence graph 167, SRG(64,18,2,6), by intrinsic colour refinement.

Every automorphism preserves the cycle lengths in the graph induced on a
vertex's neighbours. It also preserves each subsequent colour consisting of
the previous colour and the multiset of neighbours' colours. A discrete final
partition therefore proves Aut(G) = 1, without an automorphism-group library.

This is colour refinement AFTER an intrinsic neighbourhood invariant, not
ordinary uncoloured 1-WL or 2-WL (which cannot split an SRG's vertices).
The scan certifies rigidity of graph 167 only; completeness of the catalogue
and existence of involutions in the other 166 are literature results.
"""

from collections import Counter
import bz2
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/codex_asymmetry_synthesis_20261014/literature_expansion"
SOURCE = DATA / "spence_64_18_2_6.txt.bz2"
SOURCE_URL = "https://www.maths.gla.ac.uk/~es/SRGs/64-18-2-6"


def load_catalogue():
    rows = [line.strip() for line in bz2.decompress(SOURCE.read_bytes()).decode("ascii").splitlines()
            if len(line.strip()) == 64 and set(line.strip()) <= {"0", "1"}]
    assert len(rows) == 167 * 64
    return [[{v for v, char in enumerate(row) if char == "1"}
             for row in rows[start:start + 64]]
            for start in range(0, len(rows), 64)]


def neighbourhood_cycles(adj, vertex):
    remaining = set(adj[vertex])
    assert all(len(adj[w] & adj[vertex]) == 2 for w in remaining)
    sizes = []
    while remaining:
        first = min(remaining)
        remaining.remove(first)
        component = {first}
        stack = [first]
        while stack:
            found = adj[stack.pop()] & remaining
            remaining -= found
            component |= found
            stack.extend(found)
        sizes.append(len(component))
    return tuple(sorted(sizes))


def compress(signatures):
    ids = {signature: index for index, signature in enumerate(sorted(set(signatures)))}
    return [ids[signature] for signature in signatures]


def refine(adj):
    local_types = [neighbourhood_cycles(adj, v) for v in range(len(adj))]
    colours = compress(local_types)
    rounds = [colours]
    while True:
        new = compress([(colours[v], tuple(sorted(colours[w] for w in adj[v])))
                        for v in range(len(adj))])
        if len(set(new)) == len(set(colours)):
            break
        rounds.append(new)
        colours = new
    return local_types, rounds


def check_srg(adj):
    assert len(adj) == 64
    for u in range(64):
        assert u not in adj[u] and len(adj[u]) == 18
        assert all(u in adj[v] for v in adj[u])
    for u, v in combinations(range(64), 2):
        assert len(adj[u] & adj[v]) == (2 if v in adj[u] else 6)


def four_vertex_counts(adj):
    histograms = {"adjacent": Counter(), "nonadjacent": Counter()}
    witnesses = {kind: {} for kind in histograms}
    for u, v in combinations(range(len(adj)), 2):
        common = adj[u] & adj[v]
        count = sum(y in adj[x] for x, y in combinations(sorted(common), 2))
        kind = "adjacent" if v in adj[u] else "nonadjacent"
        histograms[kind][count] += 1
        witnesses[kind].setdefault(count, [u, v])
    return {"histograms": {kind: dict(sorted(counts.items()))
                           for kind, counts in histograms.items()},
            "witness_pairs_zero_based": witnesses,
            "satisfies_four_vertex_condition": all(len(h) == 1 for h in histograms.values())}


def main():
    catalogue = load_catalogue()
    discrete = []
    for number, adj in enumerate(catalogue, 1):
        local_types, rounds = refine(adj)
        if len(set(rounds[-1])) == 64:
            discrete.append(number)
    assert discrete == [167]
    adj = catalogue[166]
    check_srg(adj)
    local_types, rounds = refine(adj)
    counts = [len(set(colours)) for colours in rounds]
    assert counts == [8, 57, 64]
    classes = [{"cycle_lengths": list(t),
                "vertices_zero_based": [v for v in range(64) if local_types[v] == t]}
               for t in sorted(set(local_types))]
    assert classes[0]["vertices_zero_based"] == [0]
    edges = "".join(f"{u} {v}\n" for u, v in combinations(range(64), 2) if v in adj[u])
    edge_path = DATA / "spence_64_18_2_6_g167.edges"
    edge_path.write_text(edges, encoding="ascii")
    certificate = {
        "source_url": SOURCE_URL,
        "source_sha256": sha256(bz2.decompress(SOURCE.read_bytes())).hexdigest(),
        "catalogue_size": len(catalogue),
        "graph_index_one_based": 167,
        "parameters_exactly_verified": [64, 18, 2, 6],
        "edge_count": 576,
        "edge_file": edge_path.name,
        "edge_file_sha256": sha256(edge_path.read_bytes()).hexdigest(),
        "intrinsic_initial_classes": classes,
        "refinement_class_counts": counts,
        "refinement_colours_by_zero_based_vertex": rounds,
        "certified_automorphism_group_order": 1,
        "catalogue_graphs_certified_by_this_invariant": discrete,
        "other_graphs_status": "Not certified rigid by this test; no group calculation performed.",
        "four_vertex_test": four_vertex_counts(adj),
        "proof": [
            "An automorphism preserves the isomorphism type of every induced neighbourhood.",
            "Each neighbourhood is 2-regular, so its sorted cycle lengths are intrinsic.",
            "A previous colour and the multiset of neighbours' colours are automorphism invariant.",
            "After two refinement rounds all 64 vertices have distinct colours.",
            "Every automorphism therefore fixes every vertex."
        ],
        "conway_limitation": "For lambda=1 every neighbourhood is the same matching; this initial invariant is constant and ordinary refinement cannot split it."
    }
    (DATA / "spence_g167_certificate.json").write_text(
        json.dumps(certificate, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({key: certificate[key] for key in [
        "parameters_exactly_verified", "graph_index_one_based", "refinement_class_counts",
        "certified_automorphism_group_order", "four_vertex_test"]}, indent=2))


if __name__ == "__main__":
    main()
