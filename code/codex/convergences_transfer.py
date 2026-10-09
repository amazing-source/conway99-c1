"""Exact finite calculations for note 235; no SRG completion search.

The boundary-witness theorem comes from the user-supplied Convergences
dossier. This script computes its mandatory six-point application and
the proper intersections relevant to equal-projection twelve-point cores.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import json

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form


ROOT = Path(__file__).resolve().parents[2]


def mandatory_six():
    a = sp.zeros(6)
    for triple in ((0, 1, 2), (3, 4, 5)):
        for i, j in combinations(triple, 2):
            a[i, j] = a[j, i] = 1
    for i, j in ((0, 3), (1, 4)):
        a[i, j] = a[j, i] = 1
    a2 = a * a
    doubles = {
        (i, j): int(2 - a[i, j] - a2[i, j])
        for i, j in combinations(range(6), 2)
    }
    doubles = {pair: count for pair, count in doubles.items() if count}
    singletons = [
        int(14 - sum(a.row(i)))
        - sum(count for pair, count in doubles.items() if i in pair)
        for i in range(6)
    ]
    empty = 93 - sum(singletons) - sum(doubles.values())
    assert (empty, singletons, sum(doubles.values())) == (
        33, [9, 9, 8, 9, 9, 8], 8
    )
    f = 3 * sp.eye(6) - a + sp.ones(6) / 9
    c = sp.eye(6)
    for i in range(5):
        c[5, i] = -1
    c[5, 5] = 3
    g = c.T * f * c
    assert all(x.q == 1 for x in g)
    assert all(g[:i, :i].det() > 0 for i in range(1, 7))
    smith = [int(abs(x)) for x in smith_normal_form(g, domain=sp.ZZ).diagonal()]
    assert g.det() == 3255 and smith == [1] * 5 + [3255]
    return {
        "empty_masks": empty,
        "singleton_counts": singletons,
        "double_masks": [{"mask": list(p), "count": n} for p, n in doubles.items()],
        "coefficient_basis": [[int(x) for x in row] for row in c.tolist()],
        "gram": [[int(x) for x in row] for row in g.tolist()],
        "determinant": 3255,
        "determinant_factors": {str(p): int(e) for p, e in sp.factorint(3255).items()},
        "smith": smith,
        "orthogonal_rank": 38,
        "orthogonal_determinant": "3255 * 7^(45-r)",
    }


def strip(twist):
    a = [[0] * 12 for _ in range(12)]
    for i in range(4):
        for side in (0, 1):
            u = 4 * side + i
            v = 4 * (side ^ (twist if i == 3 else 0)) + (i + 1) % 4
            c = 8 + i
            for x, y in ((u, v), (u, c), (v, c)):
                a[x][y] = a[y][x] = 1
    assert all(sum(row) == 4 for row in a)
    return a


def collision_intersections(twist):
    a = strip(twist)
    cases = []
    hist = Counter()
    # Every proper subset; no a priori bound on the intersection size.
    for bits in range((1 << 12) - 1):
        vertices = [i for i in range(12) if bits >> i & 1]
        degrees = [sum(a[i][j] for j in vertices) for i in range(12)]
        if any(degrees[i] > 1 for i in range(12) if not bits >> i & 1):
            continue
        size = len(vertices)
        edges = sum(degrees[i] for i in vertices) // 2
        assert (size, edges) in ((0, 0), (1, 0), (2, 0), (3, 3))
        multiplicities = [
            4 - degrees[i] if bits >> i & 1 else 1 - degrees[i]
            for i in range(12)
        ]
        assert min(multiplicities) >= 0
        assert sum(multiplicities) == 12 - size
        if size == 2:
            u, v = vertices
            assert sum(a[u][j] * a[v][j] for j in range(12)) == 0
        hist[f"size_{size}_edges_{edges}"] += 1
        cases.append({"intersection": vertices, "outside_singleton_multiplicities": multiplicities})
    assert dict(hist) == {
        "size_0_edges_0": 1, "size_1_edges_0": 12,
        "size_2_edges_0": 6 if twist == 0 else 2, "size_3_edges_3": 8,
    }
    return {"dual": "Cube" if twist == 0 else "Wagner", "proper_subsets_tested": 4095,
            "histogram": dict(hist), "cases": cases}


def main():
    result = {
        "scope": "new necessary structural consequences; no rank or C1 exclusion",
        "source_zip_sha256": "e99a5ef0aedc0f59f497ecc91299835bbd8518326b954c4db2f373b63e0c5c5c",
        "mandatory_six": mandatory_six(),
        "collision_intersections": [collision_intersections(0), collision_intersections(1)],
    }
    out = ROOT / "data" / "codex_convergences_transfer.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Mandatory six-point lattice: determinant 3255, Smith (1^5,3255).")
    for item in result["collision_intersections"]:
        print(item["dual"], item["histogram"])


if __name__ == "__main__":
    main()
