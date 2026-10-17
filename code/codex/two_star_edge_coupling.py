"""Exact abstract two-star couplings over a cross-layer near edge, P=0.

The catalog consists of necessary abstract far-graph patterns, not SRGs or
shadow assignments. See note209. Also verify the 33-dimensional Green
space directly on the cyclic (2,4,1) near graph.
"""
import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

from generic_star_apex_audit import cyclic_ball, inverse7, multiply
from grid_kernel_rank_obstruction import rank_pivots

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/codex_two_star_edge_coupling.json"


def partitions(total, count, minimum=1):
    if count == 0:
        if total == 0:
            yield ()
        return
    for first in range(minimum, total//count+1):
        for rest in partitions(total-first, count-1, first):
            yield (first,)+rest


def realize(paths, cycles, cross_count):
    # Edge type 0: internal to one star; 1: crossing between stars.
    choices = [[(side, first) for side in (0, 1)
                for first in ((0,) if length == 1 else (0, 1))]
               for length in paths]
    for settings in product(*choices):
        sides, edges = [], []
        for length, (side, first) in zip(paths, settings):
            start = len(sides)
            sides.append(side)
            for i in range(length-1):
                edge_type = (first+i) % 2
                side ^= edge_type
                sides.append(side)
                edges.append((start+i, start+i+1, edge_type))
        for length in cycles:
            start = len(sides)
            side = 0
            sides.append(side)
            for i in range(length-1):
                side ^= i % 2
                sides.append(side)
                edges.append((start+i, start+i+1, i % 2))
            assert side ^ ((length-1) % 2) == sides[start]
            edges.append((start+length-1, start, (length-1) % 2))
        if Counter(sides) != {0: 9, 1: 9}:
            continue
        internal = Counter(sides[i] for i, j, t in edges if t == 0)
        if internal != {0: 4, 1: 4}:
            continue
        assert sum(t for _, _, t in edges) == cross_count
        for i in range(18):
            assert sum(i in (u, v) for u, v, t in edges if t == 0) <= 1
            assert sum(i in (u, v) for u, v, t in edges if t == 1) <= 1
        return sides, edges
    raise AssertionError((paths, cycles, "not realizable with the prescribed colors"))


def patterns(c4):
    # On the 18 private vertices: edges=15+c4, hence exactly 3-c4
    # path components. Every cycle is 0 mod 4, and 4-cycles are forbidden.
    out = []
    for cycles in ((), (8,), (12,), (16,), (8, 8)):
        remaining = 18-sum(cycles)
        for paths in partitions(remaining, 3-c4):
            sides, edges = realize(paths, cycles, 7+c4)
            a = [[0]*19 for _ in range(19)]
            for i, j, _ in edges:
                a[i][j] = a[j][i] = 1
            # Last vertex is the common apex, isolated in the union.
            gram = [[(3*int(i == j)+3-a[i][j]) % 7 for j in range(19)]
                    for i in range(19)]
            q = rank_pivots(gram)[0]
            stars = [[int(i == 18 or sides[i] == side) for i in range(19)]
                     for side in (0, 1)]
            apex = [int(i == 18) for i in range(19)]
            forms = stars+[apex]
            small = multiply(multiply(forms, gram), list(map(list, zip(*forms))))
            small = [[x % 7 for x in row] for row in small]
            assert small == [[0, (2-c4) % 7, 5], [(2-c4) % 7, 0, 5], [5, 5, 6]]
            # A 19-dimensional space with this possibly degenerate Gram
            # embeds in any nondegenerate 33-space: strict room after
            # adjoining a dual to every radical direction.
            assert 38-q < 33
            out.append({"path_orders": paths, "cycle_orders": cycles,
                        "star_sides_on_private_vertices": sides,
                        "edges_with_type": edges, "green_gram_rank_mod7": q,
                        "star_sum_and_common_apex_gram_mod7": small})
    return out


def green_dimension_check():
    g = cyclic_ball()
    h = [[3*int(i == j)-g[i][j] for j in range(36)] for i in range(36)]
    hinv = inverse7([[x+1 for x in row] for row in h])
    green = [[(x-1) % 7 for x in row] for row in hinv]
    g2 = multiply(g, g)
    g3 = multiply(g2, g)
    assert all(g3[i][i] == 0 for i in range(36))
    k = [[12*int(i == j)-g[i][j]+2-g2[i][j]-int(i//12 == j//12)
          for j in range(36)] for i in range(36)]
    # V = vectors with sum zero on each of the three layers.
    basis = [[int(j == 12*layer+i)-int(j == 12*layer+11) for j in range(36)]
             for layer in range(3) for i in range(11)]
    green_v = multiply(multiply(basis, green), list(map(list, zip(*basis))))
    projector_v = [[int(i == j)-3*int(i//12 == j//12) for j in range(36)]
                   for i in range(36)]
    hkh = multiply(multiply(green, k), green)
    assert all((hkh[i][j]+projector_v[i][j]) % 7 == 0
               for i in range(36) for j in range(36))
    assert rank_pivots(k)[0] == 34 and rank_pivots(green_v)[0] == 33
    assert all(sum(k[i][12*layer:12*layer+12]) == 20
               for i in range(36) for layer in range(3))
    gk = multiply(g, k)
    cross_c4 = Counter()
    for i in range(36):
        for j in range(i+1, 36):
            if not g[i][j] or i//12 == j//12:
                continue
            c4 = sum(g[i][a]*g[a][b]*g[b][j]
                     for a in range(36) for b in range(36)
                     if len({i, j, a, b}) == 4)
            assert c4 == g3[i][j]-5
            assert k[i][j] == 1 and gk[i][j] == 12-c4
            cross_c4[c4] += 1
    return {"generic_cyclic_ball": [2, 4, 1], "rank_K_mod7": 34,
            "green_layer_balanced_dimension": 33,
            "cross_edge_four_cycle_histogram": dict(sorted(cross_c4.items())),
            "verified_identity": "H+ K H+ = -I + 3D over F7"}


def audit():
    catalog = {str(c): patterns(c) for c in range(3)}
    assert [len(catalog[str(c)]) for c in range(3)] == [38, 19, 5]
    counts = {c: dict(sorted(Counter(p["green_gram_rank_mod7"] for p in cases).items()))
              for c, cases in catalog.items()}
    return {"assumptions": "P=0; u,v a cross-layer edge in the near graph of a line T",
            "scope": "necessary abstract pair-star graphs; not shadow solutions or SRGs",
            "catalog": catalog, "gram_rank_histograms": counts,
            "green_dimension_check": green_dimension_check()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = audit()
    normalized = json.loads(json.dumps(result))
    if args.verify_only:
        assert json.loads(OUT.read_text(encoding="utf-8")) == normalized
    else:
        OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"verified": True, "pattern_counts": {c: len(v) for c, v in result["catalog"].items()},
                      "gram_rank_histograms": result["gram_rank_histograms"],
                      "green_dimension_check": result["green_dimension_check"]}))


if __name__ == "__main__":
    main()
