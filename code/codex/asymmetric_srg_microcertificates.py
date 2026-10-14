"""Small exact certificates for asymmetric SRGs on 25 and 57 vertices.

Standard library only. No graph-automorphism package is needed.

For 25 vertices, the union of all K5s is intrinsic. Enumerate every
automorphism of this core and test its action on exterior neighbour sets.

For 57 vertices, reconstruct Erskine--Griggs (2024), Figure 2, system A0.
Enumerate every possible image of three generating points of its STS(19).
Kaski--Ostergard (2004), Theorem 2.5, identifies its automorphism group
with that of its block graph. These are reproductions of known examples,
not new graphs or exclusions of Conway parameters.
"""

import argparse
import hashlib
import json
from itertools import combinations, permutations
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "data/codex_asymmetry_synthesis_20261014"
A0 = "2468acegi6d8bhcfid5hiafge7cibghiahgefdfighgecdfehfbgiihhi"


def verify_srg(adj, parameters):
    n, k, lam, mu = parameters
    assert len(adj) == n
    assert all(len(neighbours) == k and i not in neighbours
               for i, neighbours in enumerate(adj))
    assert all((j in adj[i]) == (i in adj[j])
               for i, j in combinations(range(n), 2))
    assert all(len(adj[i] & adj[j]) == (lam if j in adj[i] else mu)
               for i, j in combinations(range(n), 2))


def certificate25():
    path = DATA / "paley_sources/reconstructed_13.edges"
    adj = [set() for _ in range(25)]
    for line in path.read_text().splitlines():
        u, v = map(int, line.split())
        adj[u].add(v)
        adj[v].add(u)
    verify_srg(adj, (25, 12, 5, 6))
    cliques = [c for c in combinations(range(25), 5)
               if all(v in adj[u] for u, v in combinations(c, 2))]
    assert len(cliques) == 3
    core = set().union(*map(set, cliques))
    assert len(core) == 15

    def cross_components(c, d):
        unseen = set(c) | set(d)
        sizes = []
        while unseen:
            queue = [unseen.pop()]
            size = 0
            while queue:
                v = queue.pop()
                size += 1
                opposite = set(d) if v in c else set(c)
                assert len(adj[v] & opposite) == 2
                new = adj[v] & opposite & unseen
                unseen -= new
                queue.extend(new)
            sizes.append(size)
        return sorted(sizes)

    cross = {(i, j): cross_components(cliques[i], cliques[j])
             for i, j in combinations(range(3), 2)}
    distinguished = [i for i in range(3)
                     if all(cross[tuple(sorted((i, j)))] == [10]
                            for j in range(3) if j != i)]
    assert len(distinguished) == 1
    x = cliques[distinguished[0]]
    others = [c for i, c in enumerate(cliques) if i != distinguished[0]]
    autos = []
    attempted = 0
    for destinations in permutations(others):
        lookups = [{frozenset(adj[v] & set(x)): v for v in d}
                   for d in destinations]
        assert all(len(lookup) == 5 for lookup in lookups)
        for images in permutations(x):
            attempted += 1
            f = dict(zip(x, images))
            valid = True
            for source, lookup in zip(others, lookups):
                for v in source:
                    image = frozenset(f[t] for t in adj[v] & set(x))
                    if image not in lookup:
                        valid = False
                        break
                    f[v] = lookup[image]
                if not valid:
                    break
            if valid and all((v in adj[u]) == (f[v] in adj[f[u]])
                             for u, v in combinations(sorted(core), 2)):
                autos.append(f)
    exterior = sorted(set(range(25)) - core)
    profiles = {frozenset(adj[w] & core): w for w in exterior}
    assert len(profiles) == len(exterior) == 10
    nonidentity = [f for f in autos if any(f[u] != u for u in core)]
    assert len(autos) == 2 and len(nonidentity) == 1
    tau = nonidentity[0]
    obstructions = []
    for w in exterior:
        profile = adj[w] & core
        image = {tau[v] for v in profile}
        if frozenset(image) not in profiles:
            obstructions.append({"vertex": w, "profile": sorted(profile),
                                 "image_under_tau": sorted(image)})
    assert obstructions
    return {
        "graph": str(path.relative_to(REPO)).replace("\\", "/"),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "parameters": [25, 12, 5, 6],
        "all_K5": cliques,
        "cross_components": {str(k): v for k, v in cross.items()},
        "intrinsically_distinguished_clique": x,
        "core_candidates_checked": attempted,
        "core_automorphism_order": len(autos),
        "tau_pairs": [(u, tau[u]) for u in sorted(core) if tau[u] > u],
        "exterior_profiles": {str(w): sorted(adj[w] & core) for w in exterior},
        "obstructions_to_tau": obstructions,
        "proved_graph_automorphism_order": 1,
    }


def certificate57(outdir):
    pairs = list(combinations(range(19), 2))
    unused = set(pairs)
    blocks = []
    operation = [[i if i == j else -1 for j in range(19)] for i in range(19)]
    for character in A0:
        x, y = min(unused)
        z = int(character, 36)
        assert x < y < z < 19
        block = (x, y, z)
        for a, b in combinations(block, 2):
            assert (a, b) in unused
            unused.remove((a, b))
            operation[a][b] = operation[b][a] = next(
                p for p in block if p not in (a, b))
        blocks.append(block)
    assert len(blocks) == 57 and not unused

    seed = (0, 1, 3)
    known = set(seed)
    rules = []
    while True:
        changed = False
        for x, y in pairs:
            if x in known and y in known and operation[x][y] not in known:
                z = operation[x][y]
                known.add(z)
                rules.append((z, x, y))
                changed = True
        if not changed:
            break
    assert len(known) == 19
    autos = []
    bijections = []
    attempted = 0
    for images in permutations(range(19), len(seed)):
        attempted += 1
        f = [-1] * 19
        for x, y in zip(seed, images):
            f[x] = y
        used = set(images)
        valid = True
        for z, x, y in rules:
            image = operation[f[x]][f[y]]
            if image in used:
                valid = False
                break
            f[z] = image
            used.add(image)
        if valid:
            failure = next(((x, y) for x, y in pairs
                            if f[operation[x][y]] != operation[f[x]][f[y]]), None)
            bijections.append({"seed_images": images,
                               "violated_pair": failure})
            if failure is None:
                autos.append(f)
    assert autos == [list(range(19))]
    adj = [{j for j in range(57) if i != j and set(blocks[i]) & set(blocks[j])}
           for i in range(57)]
    verify_srg(adj, (57, 24, 11, 9))
    edges = "".join(f"{i} {j}\n" for i in range(57) for j in sorted(adj[i]) if i < j)
    graph_path = outdir / "erskine_griggs_A0_57.edges"
    graph_path.write_text(edges, encoding="utf-8")
    return {
        "source": "https://arxiv.org/pdf/2405.07750",
        "source_locator": "Figure 2, system A0; notation defined in section 1",
        "compact_STS19": A0,
        "blocks": blocks,
        "generating_points": seed,
        "forced_extension_rules_z_x_y": rules,
        "seed_images_checked": attempted,
        "bijective_candidates": bijections,
        "proved_STS_automorphism_order": len(autos),
        "block_graph_parameters_verified": [57, 24, 11, 9],
        "graph_file": graph_path.name,
        "graph_sha256": hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        "group_transfer": "Kaski--Ostergard (2004), Theorem 2.5 (v >= 19)",
        "proved_graph_automorphism_order": 1,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DATA / "microcertificates")
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    result = {"srg25": certificate25(), "srg57": certificate57(args.outdir)}
    target = args.outdir / "certificates.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"srg25": {"core_candidates": 240, "Aut": 1},
                      "srg57": {"STS_seed_images": 5814, "Aut": 1},
                      "certificate": str(target)}))


if __name__ == "__main__":
    main()
