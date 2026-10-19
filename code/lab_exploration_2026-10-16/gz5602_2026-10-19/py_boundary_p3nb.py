"""Boundary covers for the family P3NB (LAB 19/10/2026): shared pair H01 = -H02 (core Q01 u Q02), Y-grids Q45 and Q46
(a path through line 4), and a B-grid Q13 through b = 1 and the free line 3.  Q12 is NOT assumed to be a grid.
The boundary is the Y-part only (as for P3/P3N: each Y label sees a core pair, the pairs of a grid partition the core,
Codex's catalogue with forced corner oppositions, same-letter compatibility on the shared root 4, multiset <= T); the
B-grid matchings are enumerated later as attachments by py_extend.py (family P3NB).
Symmetry: the B-grid sits on line 1, so the swap b <-> c (lines 1 <-> 2) is NOT a symmetry of this family; the group
is (letter flips of lines 0, 1, 2 that stabilise the core) x (relabellings of lines 4, 5, 6 preserving {45, 46}, with
letter flips).  The core types are therefore taken up to letter flips only (paircores8.json reduced here).
usage: python py_boundary_p3nb.py <codex dir> <paircores8.json> <out dir> [core indices | all]"""
import gzip
import json
import sys
import time
from collections import Counter
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path

codex, cores_path, outdir = sys.argv[1:4]
sel = sys.argv[4] if len(sys.argv) > 4 else "all"
sys.path.insert(0, codex)
from root_component_shared_core_colors import deficit                       # noqa: E402
from root_component_shared_k3_boundary import matching_catalogue, compatible  # noqa: E402

GRIDS = ((0, 1), (0, 2))          # local Y roots 0, 1, 2 = lines 4, 5, 6
NG = 2
CORE_LABELS = [(2 * i + s, 2 * j + t) for (i, j) in ((0, 1), (0, 2)) for s, t in product(range(2), repeat=2)]
LOOK = {q: k for k, q in enumerate(CORE_LABELS)}


def flip_perm(f):
    return [LOOK[tuple(sorted(x ^ f[x // 2] for x in q))] for q in CORE_LABELS]


FLIPS = [flip_perm(f) for f in product(range(2), repeat=3)]


def core_key(core, p):
    return tuple(sorted(tuple(sorted((p[u], p[v]))) for u, v in core["edges"]))


def flip_stabilizer(core):
    e = core_key(core, list(range(8)))
    out = []
    for p in FLIPS:
        if core_key(core, p) == e:
            out.append(tuple(sum(1 << p[v] for v in range(8) if mask & (1 << v)) for mask in range(256)))
    return out


def y_group():
    out = []
    for p in permutations(range(3)):
        img = [tuple(sorted((p[a], p[b]))) for a, b in GRIDS]
        if sorted(img) != sorted(GRIDS):
            continue
        for f in product((0, 1), repeat=3):
            m = {}
            for g, (a, b) in enumerate(GRIDS):
                ng = GRIDS.index(tuple(sorted((p[a], p[b]))))
                na, nb = GRIDS[ng]
                for corner in range(4):
                    s, t = divmod(corner, 2)
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
    transforms = flip_stabilizer(core)
    states = set(); cnt = Counter()
    shared = [(0, 1, 0, 0)]          # Q45 and Q46 share local root 0 (line 4), first coordinate of both
    for combo in combinations_with_replacement(range(len(cat)), NG):
        ms = [cat[i] for i in combo]
        used = Counter(k for m in ms for k in m["ids"])
        if any(n > T[k] for k, n in used.items()):
            continue
        cnt["matching_tuples"] += 1
        for lays in product(*[m["layouts"] for m in ms]):
            if all(compatible(lays[g], lays[h], 1 - kg, 1 - kh) for g, h, kg, kh in shared):
                states.add(canon(b"".join(bytes(l) for l in lays), transforms))
    return {"status": "COMPLETE_BOUNDARY_COVER", "family": "P3NB", "core": core, "counts": dict(cnt),
            "boundaries_hex": sorted(s.hex() for s in states), "boundary_count": len(states),
            "symmetry": "flip stabiliser of the core x Y-group(45,46)", "cpu_seconds": round(time.process_time() - t0, 2)}


cores = json.load(open(cores_path))
reps = {}
for ci, c in enumerate(cores):
    k = min(core_key(c, p) for p in FLIPS)
    reps.setdefault(k, ci)
rep_list = sorted(reps.values())
Path(outdir).mkdir(parents=True, exist_ok=True)
Path(outdir, "core_reps_flips.json").write_text(json.dumps({"group": "letter flips of lines 0,1,2 (order 8)",
                                                              "representatives": rep_list}))
todo = rep_list if sel == "all" else [int(x) for x in sel.split(",")]
for ci in todo:
    assert ci in rep_list, ci
    res = enumerate_boundary(cores[ci])
    res["core_index"] = ci
    Path(outdir, "core_%03d.json.gz" % ci).write_bytes(gzip.compress(json.dumps(res).encode(), mtime=0))
    print(json.dumps({k: res.get(k) for k in ("core_index", "status", "boundary_count", "counts", "cpu_seconds")}), flush=True)
