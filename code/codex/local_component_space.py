"""Verify the universal 14-dimensional local component space of note208.

All nonempty blocks on all seven lines are checked, without random systems.
The arbitrary blocks need not be simultaneously realizable in an SRG.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

from generic_star_apex_audit import determinant, multiply
from grid_kernel_rank_obstruction import rank_pivots
from grid_vertex_relations import PAIRS, ball_image, grid_vector

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/codex_local_component_space.json"


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def component_vector(i, block):
    # kappa = 1_C + |block| 1_L_i, constructed directly in 99 coordinates.
    m = len(block)
    v = [0]*99
    v[0] = v[1+2*i] = v[2+2*i] = m
    for j in block:
        v[1+2*j] = v[2+2*j] = 1
        edge = tuple(sorted((i, j)))
        start = 15+4*PAIRS.index(edge)
        v[start:start+4] = [1]*4
    return v


def audit():
    grids = [grid_vector(edge) for edge in PAIRS]
    c = [[int(i in edge) for edge in PAIRS] for i in range(7)]
    cc = multiply(c, list(map(list, zip(*c))))
    assert cc == [[5*int(i == j)+1 for j in range(7)] for i in range(7)]
    gamma = [[(dot(g, h)-81) % 7 for h in grids] for g in grids]
    assert all(gamma[i][j] == (4*int(i == j)+2*len(set(e) & set(f))-3) % 7
               for i, e in enumerate(PAIRS) for j, f in enumerate(PAIRS))
    assert rank_pivots(c)[0] == 7 and rank_pivots(gamma)[0] == 14
    assert all(x % 7 == 0 for row in multiply(gamma, list(map(list, zip(*c)))) for x in row)
    pivot_columns = rank_pivots(gamma)[2]
    minor = [[gamma[i][j] for j in pivot_columns] for i in pivot_columns]
    det7 = determinant(minor) % 7
    assert det7 in (3, 5, 6)
    assert determinant(cc) % 7 == 5

    # Seven independent relations, exact in Z before centering mod 7.
    for i in range(7):
        z = [int(j == i) for j in range(7)]
        image = ball_image(1, z)
        combination = [sum(grids[k][p] for k, e in enumerate(PAIRS) if i in e)
                       for p in range(99)]
        assert image == combination
        centered = [(x-12) % 7 for x in combination]
        assert centered == [(x-5) % 7 for x in image]

    blocks = []
    for i in range(7):
        rest = [j for j in range(7) if j != i]
        for m in range(1, 7):
            for b in combinations(rest, m):
                v = component_vector(i, b)
                expected = [sum(grids[PAIRS.index(tuple(sorted((i, j))))][p] for j in b)
                            for p in range(99)]
                assert v == expected and sum(v) == 9*m
                blocks.append((i, set(b), v))
    pairs_checked = 0
    for ix, (i, b, v) in enumerate(blocks):
        for j, b2, w in blocks[ix:]:
            m, n = len(b), len(b2)
            common = len(b & b2)
            if i == j:
                predicted = 6*common+3*m*n
            else:
                predicted = (2*common+4*(j in b)*(i in b2)
                             +2*n*(j in b)+2*m*(i in b2)+m*n)
            assert dot(v, w) == predicted
            pairs_checked += 1
    assert len(blocks) == 441 and pairs_checked == 97461

    # Two extreme partition systems and a 3+3 system from a regular
    # tournament. The latter's component graph is connected and bipartite.
    systems = {
        "one_block_per_line": [[set(range(7))-{i}] for i in range(7)],
        "six_singletons_per_line": [[{j} for j in range(7) if j != i] for i in range(7)],
        "cyclic_tournament_3_plus_3": [
            [{(i+d) % 7 for d in (1, 2, 3)}, {(i+d) % 7 for d in (4, 5, 6)}]
            for i in range(7)],
    }
    examples = {}
    for label, system in systems.items():
        incidence = [[int(i in e and next(j for j in e if j != i) in b)
                      for e in PAIRS] for i in range(7) for b in system[i]]
        rank_w = rank_pivots(incidence)[0]
        gram = multiply(multiply(incidence, gamma), list(map(list, zip(*incidence))))
        q = rank_pivots(gram)[0]
        h = rank_w-7
        # Incidence rows have precisely two 1s per column.
        assert all(sum(row[j] for row in incidence) == 2 for j in range(21))
        assert q <= h <= 14 and q >= 2*h-14
        examples[label] = {"block_count": len(incidence), "incidence_rank_mod7": rank_w,
                           "bipartite_component_count": len(incidence)-rank_w,
                           "class_dimension_upper_bound": h, "gram_rank_mod7": q}
    assert examples["one_block_per_line"]["class_dimension_upper_bound"] == 0
    assert examples["six_singletons_per_line"]["gram_rank_mod7"] == 14
    assert examples["cyclic_tournament_3_plus_3"]["class_dimension_upper_bound"] == 6
    return {"formal_edges": PAIRS, "formal_centered_gram_mod7": gamma,
            "formal_centered_gram_rank": 14, "radical_dimension": 7,
            "principal_basis": pivot_columns, "principal_determinant_mod7": det7,
            "quadratic_space": "hyperbolic dimension 14 over F7",
            "blocks_checked": len(blocks), "integer_gram_entries_checked": pairs_checked,
            "integer_ball_relations_checked": 7, "examples": examples}


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
    print(json.dumps({"verified": True, "dimension": 14,
                      "determinant_mod7": result["principal_determinant_mod7"],
                      "blocks_checked": result["blocks_checked"], "examples": result["examples"]}))


if __name__ == "__main__":
    main()
