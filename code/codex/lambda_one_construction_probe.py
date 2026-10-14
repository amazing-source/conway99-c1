"""An asymmetric lambda=1 control and a limited SRG switching obstruction.

Run with standard Python, with no third-party dependencies:
    python code/codex/lambda_one_construction_probe.py

The constructed graph is NOT strongly regular. It is the line graph of an
explicit triangle-free cubic graph. An edge uv and an edge uw in that graph
have just the third edge at u as their common neighbour in the line graph.
Thus the line graph is 4-regular, locally 2K2, and has lambda=1.

Every automorphism preserves the number of closed walks of each length at
each vertex. Here the vectors for lengths 1 through 9 distinguish all 30
vertices, proving that the automorphism group is trivial.

The separate switching check concerns ONLY ordinary one-cell Godsil--McKay
switching. Let X have even size s, induce a d-regular graph, and have h outside
vertices with s/2 neighbours in X and t with s neighbours in X. For a
SRG(v,k,1,2), counting edges across X and then pairs in X with a common
neighbour outside X gives

    h + 2t = 2(k-d),
    h*C(s/2,2) + t*C(s,2) = s(s-1) - s*d*d/2.

Consequently s*t = 4(s-1) - 2*d*d - (s-2)(k-d).
The integer bounds below leave only s=2 at (v,k)=(99,14) and (243,22).
Switching a two-vertex cell just exchanges its two vertex labels. Odd cells
have no half-neighbours and do not change the graph. This says nothing about
multi-cell switching or other trades, and is not a nonexistence proof for
asymmetric SRGs.

Method reference: Abiad, Brouwer, Haemers (2014), Proposition 1,
https://arxiv.org/abs/1406.4170 . The parameter-specific count is derived here;
no claim of novelty is made for it or for the line-graph construction.
"""

import argparse
from collections import Counter
import hashlib
import json
from math import comb
from pathlib import Path


# Found by a seeded cubic configuration-model search (seed 20261014, trial 86).
# Keeping the actual edges makes reproduction independent of RNG versions.
BASE_EDGES = (
    (0, 7), (0, 14), (0, 16), (1, 14), (1, 18), (1, 19),
    (2, 6), (2, 8), (2, 17), (3, 8), (3, 15), (3, 16),
    (4, 11), (4, 18), (4, 19), (5, 11), (5, 13), (5, 16),
    (6, 10), (6, 18), (7, 10), (7, 15), (8, 14), (9, 11),
    (9, 12), (9, 13), (10, 13), (12, 15), (12, 17), (17, 19),
)


def adjacency(n, edges):
    result = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n and v not in result[u]
        result[u].add(v)
        result[v].add(u)
    return result


def connected(adj):
    seen, pending = {0}, [0]
    while pending:
        for w in adj[pending.pop()]:
            if w not in seen:
                seen.add(w)
                pending.append(w)
    return len(seen) == len(adj)


def closed_walk_signatures(adj, max_length):
    signatures = []
    for root in range(len(adj)):
        counts = [int(v == root) for v in range(len(adj))]
        signature = []
        for _ in range(max_length):
            counts = [sum(counts[w] for w in neighbours) for neighbours in adj]
            signature.append(counts[root])
        signatures.append(signature)
    return signatures


def one_cell_candidates(v, k):
    candidates = []
    for s in range(2, v + 1, 2):
        for d in range(min(k, s - 1) + 1):
            numerator = 4 * (s - 1) - 2 * d * d - (s - 2) * (k - d)
            if numerator % s:
                continue
            t = numerator // s
            h = 2 * (k - d - t)
            if t < 0 or h < 0 or t + h > v - s:
                continue
            # Check the original two counting equations as well.
            assert h * (s // 2) + t * s == s * (k - d)
            assert 2 * (h * comb(s // 2, 2) + t * comb(s, 2)) == (
                2 * s * (s - 1) - s * d * d
            )
            candidates.append({"s": s, "d": d, "t": t, "h": h})
    return candidates


def write_edges(path, edges):
    raw = "".join(f"{u} {v}\n" for u, v in edges).encode("ascii")
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parents[2]
        / "data/codex_lambda_one_construction_20261014",
    )
    args = parser.parse_args()
    base = adjacency(20, BASE_EDGES)
    assert connected(base) and all(len(row) == 3 for row in base)
    assert all(not (base[u] & base[v]) for u, v in BASE_EDGES)
    graph_edges = [
        (i, j) for i in range(30) for j in range(i + 1, 30)
        if set(BASE_EDGES[i]) & set(BASE_EDGES[j])
    ]
    graph = adjacency(30, graph_edges)
    assert connected(graph) and all(len(row) == 4 for row in graph)
    edge_counts, nonedge_counts = Counter(), Counter()
    for u in range(30):
        for v in range(u + 1, 30):
            target = edge_counts if v in graph[u] else nonedge_counts
            target[len(graph[u] & graph[v])] += 1
    assert edge_counts == {1: 60}
    assert nonedge_counts == {0: 259, 1: 112, 2: 4}
    assert all(
        len(graph[w] & graph[v]) == 1 for v in range(30) for w in graph[v]
    )  # Every 4-vertex neighbourhood is 1-regular, hence 2K2.
    signatures = closed_walk_signatures(graph, 9)
    classes = [len({tuple(row[:r]) for row in signatures}) for r in range(1, 10)]
    assert classes == [1, 1, 1, 2, 4, 12, 19, 26, 30]
    gm = {str(v): one_cell_candidates(v, k) for v, k in [(99, 14), (243, 22)]}
    for rows in gm.values():
        assert len(rows) == 2 and all(row["s"] == 2 for row in rows)
    args.output.mkdir(parents=True, exist_ok=True)
    hashes = {
        "cubic20.edges": write_edges(args.output / "cubic20.edges", BASE_EDGES),
        "line30.edges": write_edges(args.output / "line30.edges", graph_edges),
    }
    result = {
        "status": "Asymmetric regular lambda=1 graph constructed; NOT an SRG.",
        "construction": {
            "method": "Line graph of the explicit triangle-free cubic graph cubic20.edges.",
            "vertex_labels": "Vertex i of line30 is edge i of cubic20, in file order.",
            "base_order": 20, "base_degree": 3, "base_connected": True,
            "base_triangle_free": True, "order": 30, "size": len(graph_edges),
            "degree": 4, "connected": True, "neighbourhood": "2K2 at every vertex",
            "lambda": 1, "adjacent_common_neighbour_histogram": dict(edge_counts),
            "nonadjacent_common_neighbour_histogram": dict(nonedge_counts),
            "strongly_regular": False, "automorphism_group_order": 1,
        },
        "asymmetry_certificate": {
            "invariant": "Numbers (A^r)[v,v] of closed walks, r=1,...,9.",
            "proof": "All 30 vectors are distinct. Every automorphism preserves them, so fixes every vertex.",
            "distinct_vectors_by_max_length": classes,
            "vertex_signatures": signatures,
            "limitation": "For an SRG every diagonal (A^r)[v,v] is constant. This certificate cannot distinguish vertices of an SRG.",
        },
        "one_cell_godsil_mckay_obstruction": {
            "scope": "SRG(v,k,1,2), ordinary one-cell switching only.",
            "reference": "https://arxiv.org/abs/1406.4170",
            "definitions": "s=even cell size; d=induced degree; h,t=outside counts with s/2,s neighbours.",
            "cross_edges": "h+2t=2(k-d)",
            "outside_common_neighbours": "h*C(s/2,2)+t*C(s,2)=s(s-1)-s*d^2/2",
            "elimination": "s*t=4(s-1)-2*d^2-(s-2)*(k-d)",
            "enumeration_bounds": "2<=s<=v even; 0<=d<=min(k,s-1); t,h nonnegative integers; t+h<=v-s.",
            "parameters": [[99, 14, 1, 2], [243, 22, 1, 2]],
            "all_integer_candidates": gm,
            "conclusion": "Only two-vertex cells survive; their switching is a relabelling. Odd cells have no half-neighbours and do nothing.",
            "not_excluded": "Multi-cell switching, other trades, and asymmetric SRGs in general.",
            "novelty": "No novelty claim; the parameter-specific obstruction is derived by elementary counting.",
        },
        "sha256": hashes,
    }
    (args.output / "certificate.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "construction": result["construction"],
        "closed_walk_class_counts": classes,
        "gm_integer_candidates": gm,
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
