"""Independent exact audit of Astra's two-apex witness (dossier 5).

No code is imported from the structures repository. Reconstruct its cyclic
(2,4,1) ball and the ten published supports, then verify integer constraints
and the Green products in F_7. Also check the abstract complete-star Gram
and its reduction perpendicular to the two apexes. See note207.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/codex_generic_star_apex_audit.json"
SOURCE_COMMIT = "3e9690b73955a781e0bf64baef36e5f29ac4dc39"
SUPPORTS = [
    [0, 1, 21, 23, 30, 33],
    [0, 2, 13, 19, 32, 33],
    [0, 3, 13, 16, 29, 31],
    [0, 4, 12, 23, 27, 35],
    [0, 5, 15, 18, 27, 28],
    [0, 7, 15, 22, 25, 26],
    [0, 8, 14, 19, 31, 34],
    [0, 9, 14, 17, 32, 35],
    [0, 10, 20, 22, 28, 29],
    [0, 11, 16, 21, 24, 26],
]


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)]
            for row in a]


def inverse7(a):
    n = len(a)
    aug = [[x % 7 for x in row] + [int(i == j) for j in range(n)]
           for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if aug[i][j])
        aug[pivot], aug[j] = aug[j], aug[pivot]
        factor = pow(aug[j][j], -1, 7)
        aug[j] = [factor*x % 7 for x in aug[j]]
        for i in range(n):
            if i != j:
                factor = aug[i][j]
                aug[i] = [(x-factor*y) % 7 for x, y in zip(aug[i], aug[j])]
    assert all(aug[i][:n] == [int(i == j) for j in range(n)] for i in range(n))
    return [row[n:] for row in aug]


def determinant(a):
    a = [row[:] for row in a]
    sign = previous = 1
    for j in range(len(a)-1):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            sign = -sign
        for i in range(j+1, len(a)):
            for k in range(j+1, len(a)):
                numerator = a[j][j]*a[i][k]-a[i][j]*a[j][k]
                assert numerator % previous == 0
                a[i][k] = numerator // previous
            a[i][j] = 0
        previous = a[j][j]
    return sign*a[-1][-1]


def cyclic_ball():
    a = [[0]*36 for _ in range(36)]

    def edge(i, j):
        assert i != j and not a[i][j]
        a[i][j] = a[j][i] = 1

    for layer, shift in enumerate((0, 2, 4)):
        for i in range(6):
            edge(12*layer+i, 12*layer+6+(i+shift) % 6)
    for t in range(2):
        for i in range(6):
            edge(6*t+i, 12+6*t+i)
            edge(6*t+i, 24+6*t+i)
            edge(12+6*t+i, 24+6*t+(i+1) % 6)
    assert all(sum(row) == 3 for row in a)
    return a


def complete_star_model():
    # Two apexes followed by four matched pairs. This is an abstract target,
    # not the Gram of the published counterexample.
    matching = {(2+2*i, 3+2*i) for i in range(4)}
    gram = [[(6 if i == j else 2 if tuple(sorted((i, j))) in matching else 3)
             for j in range(10)] for i in range(10)]
    assert determinant(gram) % 7 == 2
    # z_i = n_i - 5(a+b), since Gram(a,b)=[[6,3],[3,6]].
    change = []
    for i in range(2, 10):
        change.append([-5, -5] + [int(i == j) for j in range(2, 10)])
    reduced = multiply(multiply(change, gram), list(map(list, zip(*change))))
    reduced = [[x % 7 for x in row] for row in reduced]
    target = [[(3*(i == j)+1-int(i != j and i//2 == j//2)) % 7
               for j in range(8)] for i in range(8)]
    assert reduced == target
    assert determinant(reduced) % 7 == 5
    differences = [[int(j == 2*i)-int(j == 2*i+1) for j in range(8)]
                   for i in range(4)]
    dg = multiply(multiply(differences, reduced), list(map(list, zip(*differences))))
    assert [[x % 7 for x in row] for row in dg] == [
        [int(i == j) for j in range(4)] for i in range(4)]
    # Given the exact sum, norms, and apex products, each row on the other
    # seven non-apex shadows sums to 6. For entries 2/3 this forces one 2.
    assert [d for d in range(8) if (3*7-d) % 7 == 6] == [1]
    return {"gram_determinant_mod7": 2, "apex_gram_determinant_mod7": 6,
            "reduced_gram": reduced, "reduced_determinant_mod7": 5,
            "pair_difference_gram_mod7": [[int(i == j) for j in range(4)]
                                          for i in range(4)]}


def audit():
    a = cyclic_ball()
    h = [[3*int(i == j)-a[i][j] for j in range(36)] for i in range(36)]
    tau = determinant([row[1:] for row in h[1:]])
    assert tau == 3096828960300 and tau % 7 == 5
    inv = inverse7([[x+1 for x in row] for row in h])
    green = [[(x-1) % 7 for x in row] for row in inv]
    assert green == list(map(list, zip(*green)))
    assert all(sum(row) % 7 == 0 for row in green)
    assert all(x % 7 == (int(i == j)-1) % 7
               for i, row in enumerate(multiply(h, green)) for j, x in enumerate(row))
    a2 = multiply(a, a)
    k = [[12*int(i == j)-a[i][j]+2-a2[i][j]-int(i//12 == j//12)
          for j in range(36)] for i in range(36)]
    assert all(k[i][i] == 10 for i in range(36))
    assert min(x for row in k for x in row) == 0
    vectors = [[int(i in support) for i in range(36)] for support in SUPPORTS]
    groups = [s[1] for s in SUPPORTS]
    assert groups == [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    caps = []
    for support, n in zip(SUPPORTS, vectors):
        assert len(set(support)) == 6
        for layer in range(3):
            pair = [i for i in support if i//12 == layer]
            assert len(pair) == 2 and a[pair[0]][pair[1]] == 0
        an = [sum(a[i][j]*n[j] for j in range(36)) for i in range(36)]
        assert all(an[i] <= 2-n[i] for i in range(36))
        caps.append(1-an[0])
    assert caps == [1, 1, 1, 0, 1, 1, 1, 1, 1, 0]
    assert [sum(n[i] for n in vectors) for i in range(36)] == [row[0] for row in k]
    incidence_gram = multiply(list(map(list, zip(*vectors))), vectors)
    assert all(incidence_gram[i][j] <= k[i][j] for i in range(36) for j in range(36))
    overlaps = multiply(vectors, list(map(list, zip(*vectors))))
    assert all(overlaps[i][j] <= 2 for i, j in combinations(range(10), 2))
    gram = multiply(multiply(vectors, green), list(map(list, zip(*vectors))))
    gram = [[x % 7 for x in row] for row in gram]
    assert all(gram[i][i] == 6 for i in range(10))
    apexes = [i for i in range(10) if caps[i] == 0]
    assert [groups[i] for i in apexes] == [4, 11]
    assert all(gram[i][j] == 3 for i in apexes for j in range(10) if i != j)
    failures = [[groups[i], groups[j], gram[i][j]]
                for i, j in combinations(range(10), 2) if gram[i][j] not in (2, 3)]
    assert len(failures) == 19 and failures[0] == [1, 2, 4]
    # Exact-sum Green identities hold despite the failed binary products.
    assert all(sum(gram[i][j] for j in range(10) if j != i) % 7 == (6-caps[i]) % 7
               for i in range(10))
    return {
        "source_repository": "amazing-source/conway99-structures-lab",
        "source_commit": SOURCE_COMMIT,
        "source_path": "astra/RAPPORT_ASTRA_SUIVI4_ET_AUDIT_S5.md",
        "cyclic_parameters": [2, 4, 1], "spanning_trees": tau,
        "spanning_trees_mod7": tau % 7, "supports": SUPPORTS,
        "apex_groups": [4, 11], "capacities": caps, "green_gram_mod7": gram,
        "failed_nonapex_pairs": failures,
        "verified_integer_conditions": ["two nonpartners per layer", "G n <= 2-n",
            "sum(n) = K e_0", "pair overlaps <= 2", "M_star M_star^T <= K"],
        "verified_mod7_conditions": ["all ten norms are 6", "all apex products are 3",
                                     "Green row-sum identities"],
        "complete_star_target": complete_star_model(),
        "conclusion": "Apex-only conditions are feasible; the witness is not a complete star.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.verify_only:
        assert json.loads(OUT.read_text(encoding="utf-8")) == result
    else:
        OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"verified": True, "tau": result["spanning_trees"],
                      "failed_nonapex_pairs": len(result["failed_nonapex_pairs"]),
                      "complete_star_target_determinant_mod7": 2}))


if __name__ == "__main__":
    main()
