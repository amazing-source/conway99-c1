"""Boundary cover of a shared pair core with a set of Y-grids (LAB 19/10/2026), parameterised version of Codex's
root_component_shared_k3_boundary.py (main 30d68c38) so that the K3 case (Y-grids on local roots (0,1),(0,2),(1,2) =
lines 45, 46, 56) reproduces Codex's counts exactly and the P3 case uses only (0,1),(0,2) = lines 45, 46.
Facts used (as in Codex's generator): each Y-grid dominates the core perfectly (a perfect matching inside supp(T));
corner layouts respect the forced oppositions; two labels of Y-grids sharing a root and carrying the same letter on
it do not see the same core pair; the multiset of matchings stays below T.  Quotient: core stabilisers (from the
order-16 group) x relabellings of the Y roots that preserve the set of Y-grids (permutations and letter flips); the
canonical form is the minimum over the whole group (brute force, no normalisation shortcut).
Imports Codex's unchanged helpers (matchings, matching_catalogue, compatible, core_stabilizers, colourings).
usage: python py_boundary.py <codex dir> <paircores8.json> <orbits16.json> <K3|P3> <out dir> <core indices>"""
import gzip
import json
import sys
import time
from collections import Counter
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path

codex, cores_path, orbits_path, family, outdir, sel = sys.argv[1:7]
sys.path.insert(0, codex)
from root_component_shared_core_colors import PAIRS, PAIR_ID, deficit, colourings      # noqa: E402
from root_component_shared_k3_boundary import matching_catalogue, compatible, core_stabilizers  # noqa: E402

# Y roots: lines 4, 5, 6 (local 0, 1, 2); for 2K2 lines 3, 4, 5, 6 (local 0..3), grids Q34 and Q56
GRIDS = {"K3": ((0, 1), (0, 2), (1, 2)), "P3": ((0, 1), (0, 2)), "K2": ((0, 1),), "2K2": ((0, 1), (2, 3)), "2K2N": ((0, 1), (2, 3))}[family]
NR = 4 if family in ("2K2", "2K2N") else 3
NEED_Q12 = family != "2K2N"          # 2K2N: Q_bc not assumed to be a grid, so no colour-factor skip
NG = len(GRIDS)


def y_group():
    """relabellings of the three Y roots (perm p, flips f) preserving the set GRIDS, as maps on (grid, corner)"""
    out = []
    for p in permutations(range(NR)):
        img = [tuple(sorted((p[a], p[b]))) for a, b in GRIDS]
        if sorted(img) != sorted(GRIDS):
            continue
        for f in product((0, 1), repeat=NR):
            m = {}
            for g, (a, b) in enumerate(GRIDS):
                ng = GRIDS.index(tuple(sorted((p[a], p[b]))))
                na, nb = GRIDS[ng]
                for corner in range(4):
                    s, t = divmod(corner, 2)                      # corner = 2*s + t, s on root a, t on root b
                    vals = {p[a]: s ^ f[a], p[b]: t ^ f[b]}
                    m[(g, corner)] = (ng, 2 * vals[na] + vals[nb])
            out.append(m)
    return out


YG = y_group()


def canon(state, transforms):
    best = None
    for tr in transforms:
        s = [tr[b] for b in state]
        for m in YG:
            img = [0] * (4 * NG)
            for g in range(NG):
                for c in range(4):
                    ng, nc = m[(g, c)]
                    img[4 * ng + nc] = s[4 * g + c]
            key = bytes(img)
            if best is None or key < best:
                best = key
    return best


def enumerate_boundary(core):
    t0 = time.process_time()
    T = deficit(core)
    cat = matching_catalogue(core)
    transforms = core_stabilizers(core)
    states = set(); cnt = Counter()
    shared = [(g, h, GRIDS[g].index(r), GRIDS[h].index(r)) for g in range(NG) for h in range(g + 1, NG)
              for r in set(GRIDS[g]) & set(GRIDS[h])]
    for combo in combinations_with_replacement(range(len(cat)), NG):
        ms = [cat[i] for i in combo]
        used = Counter(k for m in ms for k in m["ids"])
        if any(n > T[k] for k, n in used.items()):
            continue
        cnt["matching_tuples"] += 1
        for lays in product(*[m["layouts"] for m in ms]):
            ok = True
            for g, h, kg, kh in shared:
                # compatible(a, b, shift_a, shift_b): shift = bit of the shared root in the corner index (1 = first root)
                if not compatible(lays[g], lays[h], 1 - kg, 1 - kh):
                    ok = False; break
            if ok:
                states.add(canon(b"".join(bytes(l) for l in lays), transforms))
    cnt["canonical_states"] = len(states)
    return {"status": "COMPLETE_BOUNDARY_COVER", "family": family, "grids_local_roots": GRIDS, "core": core,
            "counts": dict(cnt), "boundaries_hex": sorted(s.hex() for s in states), "boundary_count": len(states),
            "cpu_seconds": round(time.process_time() - t0, 2)}


cores = json.load(open(cores_path))
Path(outdir).mkdir(parents=True, exist_ok=True)
for ci in [int(x) for x in sel.split(",")]:
    _, cols = colourings(cores[ci])
    if NEED_Q12 and not cols:
        res = {"status": "EXCLUDED_Q12_COLOUR_FACTORS", "boundary_count": 0}
    else:
        res = enumerate_boundary(cores[ci])
    res["core_index"] = ci
    Path(outdir, "core_%03d.json.gz" % ci).write_bytes(gzip.compress(json.dumps(res).encode(), mtime=0))
    print(json.dumps({k: res.get(k) for k in ("core_index", "status", "boundary_count", "counts", "cpu_seconds")}), flush=True)
