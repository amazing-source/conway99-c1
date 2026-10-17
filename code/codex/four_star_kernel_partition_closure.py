"""Close retained kernel constraints using nonnegative two-star networks.

The caller supplies the old side components and a proposed retained kernel.
No adjacency matrix, producer kernel, PSD verdict or group is re-audited.
New global kernel constraints follow CONDITIONALLY on a target T being PSD.
The default examples are abstract subspaces, not four-star graphs.
"""

import argparse
from itertools import combinations
import json
from pathlib import Path

import sympy as sp


LABELS = [(a, b) for a, b in combinations(range(14), 2)
          if a < 4 and b != (a ^ 1)]
INDEX = {label: i for i, label in enumerate(LABELS)}


def column_basis(matrix):
    matrix = sp.Matrix(matrix)
    return matrix[:, list(matrix.rref()[1])]


def indicators(components):
    return sp.Matrix(44, len(components),
                     lambda i, j: int(i in components[j]))


def signatures(retained, components, original_grid_components=()):
    """Find which old components the retained potentials distinguish.

    Side components are assumed balanced for the forced star difference,
    as are the components of the accepted two-star weighted network.
    """
    K = indicators(components)
    joined = sp.Matrix.hstack(retained, -K)
    relations = joined.nullspace()
    H = (column_basis(sp.Matrix.hstack(*[v[retained.cols:, :] for v in relations]))
         if relations else sp.zeros(len(components), 0))
    groups = {}
    for i in range(K.cols):
        groups.setdefault(tuple(H.row(i)), []).append(i)
    grouped = list(groups.values())
    separate = []
    for i, j in combinations(range(K.cols), 2):
        for k in range(H.cols):
            difference = H[i, k] - H[j, k]
            if difference:
                separate.append(dict(parts=[i, j], potential_column=k,
                                     difference=str(difference)))
                break
    singleton_indices = [group[0] for group in grouped if len(group) == 1]
    forced_grids = sorted(set(singleton_indices) & set(original_grid_components))
    new = sp.Matrix.hstack(*[sum((K[:, i] for i in group), sp.zeros(44, 1))
                              for group in grouped])
    return dict(
        retained_component_potential_dimension=H.cols,
        potential_coefficients=[[str(x) for x in H.row(i)] for i in range(H.rows)],
        indistinguishable_old_component_groups=grouped,
        target_components_at_least=len(grouped),
        forced_original_grid_components=forced_grids,
        forced_prisms_at_least=2 * len(forced_grids),
        separated_old_component_pairs=separate,
        new_kernel_columns=new,
    )


def close_retained_kernel(retained, sides):
    """Return all constraints forced by iterating the side network closure.

    Each side is a dict with name, components (lists of LABELS indices),
    and original_grid_components (indices of isolated four-label grids).
    Components and the original grid declarations are producer hypotheses.
    The target may split old components or merge indistinguishable ones.
    It is NOT required to retain the old graph, its symmetry or its PSD rank.
    """
    retained = sp.Matrix(retained)
    if retained.rows != 44:
        raise ValueError("Expected44 coordinate rows in LABELS order.")
    original_dimension = retained.rank()
    stars = sp.Matrix(44, 4, lambda i, c: int(c in LABELS[i]))
    retained = column_basis(sp.Matrix.hstack(retained, stars))
    after_forced_stars = retained.cols
    rounds = []
    while True:
        before = retained.cols
        views = []
        additions = []
        for side in sides:
            result = signatures(retained, side["components"],
                                side.get("original_grid_components", ()))
            additions.append(result.pop("new_kernel_columns"))
            views.append(dict(name=side["name"], **result))
        enlarged = column_basis(sp.Matrix.hstack(retained, *additions))
        rounds.append(dict(before=before, after=enlarged.cols, sides=views))
        retained = enlarged
        if retained.cols == before:
            break
    return dict(
        input_dimension=original_dimension,
        dimension_after_forced_stars=after_forced_stars,
        closed_dimension=retained.cols,
        forced_added_dimensions=retained.cols-original_dimension,
        final_sides=rounds[-1]["sides"],
        rounds=rounds,
        closed_basis=retained,
        scope="Kernel closure requires nonnegative two-star networks, C1 and T PSD; the forced-grid/prism conclusions also use the C1-prime mate-label capacities. Old components are supplied; no producer graph is read.",
    )


def release_component_merge(full_kernel, sides, side_index, first, second):
    """Retain an old non-grid kernel except one chosen component difference.

    Complete the supplied side-component basis by columns of full_kernel.
    Keep that mixed complement, all forced stars, and all other components;
    replace the two selected component indicators by their SUM.
    The choice of mixed complement is explicit, not an exhaustive choice of
    all discarded functionals. No candidate graph or PSD state is constructed.
    """
    full = column_basis(full_kernel)
    odd = sp.Matrix(44, 2, lambda i, c:
                    int(2*c in LABELS[i])-int(2*c+1 in LABELS[i]))
    side_columns = [indicators(side["components"]) for side in sides]
    base = sp.Matrix.hstack(odd, *side_columns)
    if base.rank() != base.cols:
        raise ValueError("This release helper assumes independent non-grid side kernels.")
    joined = sp.Matrix.hstack(base, full)
    complete = column_basis(joined)
    if complete.cols != full.cols:
        raise ValueError("The supplied full kernel must contain the supplied side relations.")
    offset = 2 + sum(matrix.cols for matrix in side_columns[:side_index])
    if first == second or not all(0 <= i < side_columns[side_index].cols
                                  for i in (first, second)):
        raise ValueError("Choose two different old side components.")
    i, j = offset+first, offset+second
    columns = []
    for k in range(complete.cols):
        if k == j:
            continue
        columns.append(complete[:, k] + complete[:, j] if k == i else complete[:, k])
    retained = sp.Matrix.hstack(*columns)
    assert retained.cols == full.cols-1
    return retained


def abstract_c55_setup():
    """Own side partitions plus two arbitrary mixed directions; NOT a graph."""
    def parts(central, outside):
        return [[INDEX[tuple(sorted((c, y)))] for c in central for y in part]
                for part in outside]
    sides = [
        dict(name="left", components=parts((0, 1),
             [(2, 3, 4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]),
             original_grid_components=[1, 2, 3, 4]),
        dict(name="right", components=parts((2, 3),
             [(0, 1, 6, 7), (4, 5), (8, 9), (10, 11), (12, 13)]),
             original_grid_components=[1, 2, 3, 4]),
    ]
    odd = sp.Matrix(44, 2, lambda i, c:
                    int(2*c in LABELS[i])-int(2*c+1 in LABELS[i]))
    mixed = sp.zeros(44, 2)
    for c, y, value in [(0,8,1),(1,8,-1),(0,9,-1),(1,9,1),
                        (2,10,1),(3,10,-1),(2,11,-1),(3,11,1)]:
        mixed[INDEX[c, y], 0] = value
    for c, y, value in [(0,10,1),(1,10,1),(0,11,-1),(1,11,-1),
                        (2,8,1),(3,8,1),(2,9,-1),(3,9,-1)]:
        mixed[INDEX[c, y], 1] = value
    full = sp.Matrix.hstack(odd, indicators(sides[0]["components"]),
                           indicators(sides[1]["components"]), mixed)
    assert full.rank() == 14
    return full, sides


PROOF = [
    "For a two-star side X, the accepted exact formula is8T_X=L8-u*u^t, where L8=8(2I-Gamma_X)+3(I-F)+(I-M)+(I-FM) is a weighted graph Laplacian with nonnegative edge weights. The known star difference is u. Every old component indicator is balanced, hence orthogonal to u.",
    "Let W be the retained global kernel constraints. For old component indicators K_i, form H={a:sum_i a_i K_i belongs to W}. If a is in H, any proposed target satisfies L8_new*(sum_i a_i K_i)=0. The Laplacian energy is a sum of nonnegative weighted squares, so every new network edge joins vertices with identical values in every such potential.",
    "Give old component i its row signature in any basis of H. No target network edge can cross between distinct signatures. Consequently each union of equally signed old components has its indicator in ker T_X_new. Under full T PSD, a principal kernel extends by zero to the full kernel. These indicator relations can therefore be added to W and iterated on both sides.",
    "The target may split old components. It may only merge pieces from old components having equal signatures. For an old four-label grid component with a unique signature, fixed F/M connectivity forces it to remain a network component. C1 then forces the two internal same-star edges, and the C1-prime mate-label capacity forbids diagonal cross edges, forcing the two straight cross edges. Thus the actual grid remains and contributes two prisms. At least four such retained grids on both sides exclude the NG7 objective within this kernel class.",
    "For a codimension-one retained subspace in a full old kernel, assume first that all four universal star relations are retained. Restrict the discarded functional to a side component space, obtaining alpha. If alpha=0, all old component potentials remain. Otherwise H=ker(alpha) and two different component signatures coincide exactly when e_i-e_j is proportional to alpha. Thus a genuine single-relation relaxation can merge old side components only for a pair-difference functional alpha proportional to e_i-e_j.",
    "If a nonzero alpha is not a pair difference, every old component indicator is recovered by the network closure. At least one of them was outside the retained hyperplane, so the entire old global kernel is recovered. This proves that many formally codimension-one relaxations are completely ineffective, without enumerating a single target graph.",
    "In the non-grid c55 layout, one side has one active component of two root mate classes and four singleton grid components. The only component-merging directions for one released relation are the ten unordered pairs: four active/singleton merges leave at least three old grids; six singleton/singleton merges leave at least two. This is a classification of component restrictions, NOT an exhaustive classification of global discarded functionals: their action on mixed relations and the coupling of the two sides remains free.",
    "A grid-overlap kernel also contains the indicator1_O. Write K_geom=(3*B^t*B+B^t*M*B-2*J)/8, so T=3I-Gamma-K_geom. Preserving that relation forces the grid: K_geom*1_O=1_O on O and0 outside, so T*1_O=0 means Gamma*1_O=2*1_O; nonnegative adjacency gives no O-F edges, and C1 makes the internal degree-two overlap the geometric C4. Any search retaining1_O cannot reach a non-grid target.",
    "A convex interpolation between a T-PSD grid block and a T-PSD non-grid block loses the relation1_O: for0<s<1, ker((1-s)T_grid+sT_nongrid)=kerT_grid intersect kerT_nongrid. If the grid seed has nullity14, the interior of this segment has nullity at most13. This does not forbid paths along different PSD faces, nonlinear paths, discrete moves, or non-grid endpoints of nullity14.",
]


def report():
    full, sides = abstract_c55_setup()
    zero = [0]*5
    active_merge = [1,-1,0,0,0]
    grid_merge = [0,1,-1,0,0]
    generic = [1,2,3,4,-10]
    cases = [
        ("generic_both", generic, generic, [0,0], 14, [4,4]),
        ("generic_left_pair_right", generic, active_merge, [0,0], 14, [4,4]),
        ("left_active_grid_merge", active_merge, zero, [0,0], 13, [3,4]),
        ("left_two_grids_merge", grid_merge, zero, [0,0], 13, [2,4]),
        ("active_grid_merge_both", active_merge, active_merge, [0,0], 13, [3,3]),
        ("mixed_relation_only", zero, zero, [1,0], 13, [4,4]),
    ]
    results = []
    for name, alpha, beta, mixed, expected_dimension, expected_grids in cases:
        assert sum(alpha) == sum(beta) == 0
        functional = sp.Matrix([[0,0]+alpha+beta+mixed])
        retained = full * sp.Matrix.hstack(*functional.nullspace())
        result = close_retained_kernel(retained, sides)
        assert result["input_dimension"] == 13
        assert result["closed_dimension"] == expected_dimension
        actual = [len(side["forced_original_grid_components"])
                  for side in result["final_sides"]]
        assert actual == expected_grids
        assert column_basis(sp.Matrix.hstack(full, result["closed_basis"])).cols == 14
        result.pop("closed_basis")
        results.append(dict(name=name, left_released_functional=alpha,
                            right_released_functional=beta,
                            mixed_released_functional=mixed, **result))
    # The constructive helper realizes a deliberate active/grid release.
    deliberate = release_component_merge(full, sides, 0, 0, 1)
    assert deliberate.rank() == 13
    deliberate_closed = close_retained_kernel(deliberate, sides)
    assert deliberate_closed["closed_dimension"] == 13
    assert [len(s["forced_original_grid_components"])
            for s in deliberate_closed["final_sides"]] == [3, 4]
    return dict(
        status="EXACT_NONNEGATIVE_NETWORK_KERNEL_CLOSURE",
        fixtures_are_abstract_subspaces_not_graphs=True,
        full_abstract_kernel_dimension=14,
        sides=sides,
        cases=results,
        proof=PROOF,
        limitation="No proof of N9-NG, NG5 or NG7. A relaxation that survives this closure need not contain any admissible target, PSD target or new graph.",
    )


def serializable(value):
    if isinstance(value, sp.MatrixBase):
        return [[str(x) for x in value.row(i)] for i in range(value.rows)]
    if isinstance(value, dict):
        return {k: serializable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serializable(v) for v in value]
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="JSON with retained(44xr) and sides; components use LABELS indices.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.input:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = close_retained_kernel(data["retained"], data["sides"])
    else:
        result = report()
    Path(args.output).write_text(json.dumps(serializable(result), indent=2)+"\n", encoding="utf-8")
    if "cases" in result:
        print(json.dumps(dict(status=result["status"],
              cases=[dict(name=c["name"], input_dimension=c["input_dimension"],
                          closed_dimension=c["closed_dimension"],
                          forced_grids=[len(s["forced_original_grid_components"])
                                        for s in c["final_sides"]])
                     for c in result["cases"]]), indent=2))
    else:
        print(json.dumps({k:v for k,v in result.items() if k not in ("closed_basis", "rounds")}, indent=2))
