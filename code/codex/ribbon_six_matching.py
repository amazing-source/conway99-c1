"""Exact local triangle classification and arithmetic certificate, note 240.

This checks our new part of the matching dichotomy. The exclusion of chord
stars is a separate input: note 239 plus LAB's message 476 / commit 589ea52.
No attempt to recheck the peer's star certificates is made here.
Only the Python standard library is used.
"""
from itertools import combinations
import json
from pathlib import Path

from ribbon_six_star import ribbon, deficit, local_ok


def triangle_support(twist, triangle):
    a = ribbon(twist)
    for u, v in combinations(triangle, 2):
        assert not a[u][v]
        a[u][v] = a[v][u] = 1
    return a


def all_masks(a):
    """All subsets satisfying pair deficits, degree <=14 and bA<=2-b."""
    d = deficit(a)
    compatible = [{v for v in range(u+1, 18) if d[u][v] > 0}
                  for u in range(18)]
    masks = []

    def visit(chosen, remaining):
        mask = [int(u in chosen) for u in range(18)]
        counts = [sum(a[u][v] for v in chosen) for u in range(18)]
        if any(counts[u] > 2-mask[u] for u in range(18)):
            return
        masks.append(mask)
        if len(chosen) == 14:
            return
        for u in sorted(remaining):
            visit(chosen+[u], remaining & compatible[u])

    visit([], set(range(18)))
    return masks


def check():
    possible = []
    for twist in (0, 1):
        base = ribbon(twist)
        triangles = []
        for tri in combinations(range(18), 3):
            if any(base[u][v] for u, v in combinations(tri, 2)):
                continue
            if local_ok(triangle_support(twist, tri)):
                triangles.append(tri)
        expected = [(12, 14, 16), (13, 15, 17)]
        if twist:
            expected = [(0, 4, 8), (1, 5, 9), (2, 6, 10), (3, 7, 11)]+expected
        assert triangles == expected
        possible.append({"twist": twist, "locally_possible_triangles": triangles})

    path = Path(__file__).resolve().parents[2]/"data/codex_ribbon6_triangle_certificate.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["twist"] == 1 and report["triangle"] == [0, 4, 8]
    a = triangle_support(1, (0, 4, 8))
    masks = all_masks(a)
    assert len(masks) == len({tuple(b) for b in masks}) == 288
    assert sorted(masks) == sorted(report["masks"])
    pairs = list(combinations(range(18), 2))
    d = deficit(a)
    rhs = [81]+[14-sum(row) for row in a]+[d[u][v] for u, v in pairs]
    y = report["certificate"]["row_multipliers"]
    assert len(y) == len(rhs) and all(type(v) is int for v in y)
    coeffs = []
    for b in masks:
        column = [1]+b+[b[u]*b[v] for u, v in pairs]
        coeffs.append(sum(s*t for s, t in zip(y, column)))
    target = sum(s*t for s, t in zip(y, rhs))
    assert min(coeffs) >= 0 and target == -3
    assert report["certificate"]["box_lower_bound"] == 0
    assert report["certificate"]["target"] == target
    print(json.dumps({"classification": possible, "certificate_masks": len(masks),
                      "nonzero_rows": sum(v != 0 for v in y),
                      "minimum_mask_coefficient": min(coeffs), "target": target,
                      "status": "exact check passed; star exclusion is cited peer input"}))


if __name__ == "__main__":
    check()
