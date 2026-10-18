"""Letter-level extension of Codex's count design (LAB, 18/10/2026).  Measurement tool (exact Farkas certificates).

New fact used (LEMMES_C12_2026-10-18.md sec. 7.5; checked on 423 components of a real srg(243,22,1,2)): for a root line a
and a component K of G_{l_a} (block P, |P| = p, singleton blocks = prisms included), the letter imbalance
d^K_w = |N(w) cap K cap N(a*)| - |N(w) cap K cap N(a')| of the labels w off line a (set D_a) satisfies
  (E1) sum_{u in N(w) cap D_a} d^K_u = -d^K_w            for w in D_a,
  (B)  sum_{u in N(v) cap D_a} d^K_u = 2(6-p) s(v) if v in K,  -2p s(v) if v in line a's labels outside K
       (s(v) = +1 / -1 for v adjacent to a* / a'),
  (L)  sum_{u in N(l) cap D_a} d^K_u = 0                 for every letter l not on line a.
Count-level consequences, linear in multiplicities once each label also carries, for every root a off its rectangle,
the vector delta^a = (delta^{aj})_j, delta^{aj}_w = (its neighbours in Q_aj adjacent to a*) - (adjacent to a'):
  N1  for every G not containing a:  sum_{w in G} d^K_w + sum_{w in D_a} d^K_w z_w(G) = 0;
  N3  for every j != a:              sum_{w in D_a} d^K_w z_w(Q_aj) = 0;
  N3s for every j != a:              sum_{w in D_a} d^K_w delta^{aj}_w = 8(6-p) if j in P, -8p otherwise;
  N4  for every line j != a:         sum_{w in D_a, w on line j} d^K_w = 0;
with d^K_w = sum_{j in P} delta^{aj}_w, |delta^{aj}_w| <= z_w(Q_aj), delta = z mod 2, sum_j delta^{aj}_w = 0.
Columns: Codex's (class, z-state) multiplicities, plus (class, z-state, root a, delta^a) multiplicities linked by
sum_delta m = n (the joint law across roots is relaxed).  Codex's linear_system (four rows, symmetry, all moments, E3,
histograms) and find_certificate are used unchanged; the certificate is re-checked here in integers.
usage: python jhat_letter_lp.py <codex dir> <catalogue> <first> <last> [--only i,j] [--no-base-moments]"""
import json
import sys
import time
from itertools import combinations, product

codex = sys.argv[1]
sys.path.insert(0, codex)
from root_component_z_design_certificate import linear_system, find_certificate   # noqa: E402

from jhat_catalogue import catalogue as dfs_catalogue                               # noqa: E402
from jhat_rows import records, blocks_of                                             # noqa: E402

RECT = list(combinations(range(7), 2))
RI = {q: i for i, q in enumerate(RECT)}


def rq(a, j):
    return RI[(a, j) if a < j else (j, a)]


def delta_vectors(z, a):
    """All delta^a for a z-row of a label off line a: one value per j != a."""
    js = [j for j in range(7) if j != a]
    zs = [z[rq(a, j)] for j in js]
    assert sum(zs) == 4
    out = []
    for d in product(*[range(-v, v + 1, 2) for v in zs]):
        if sum(d) == 0:
            out.append(dict(zip(js, d)))
    return out


def build(t, cat, base_moments=True):
    columns, equations, bounds = linear_system(t, cat, degree_histograms=True)
    if not base_moments:
        equations = [e for e in equations if e["kind"] != "neighbor_moment" or e["indices"][0] == e["indices"][1]]
    nbase = len(columns)
    bl = blocks_of(t)
    # components at each root: list of (frozenset P)
    comps = {}
    for a in range(7):
        parts = [tuple(p) for p in t["nontrivial_component_groups"][a]]
        used = {j for p in parts for j in p}
        parts += [(j,) for j in range(7) if j != a and j not in used]
        comps[a] = parts
    ext = []                                   # (base column index, a, delta dict)
    for ci, (qi, si, z) in enumerate(columns):
        q = RECT[qi]
        for a in range(7):
            if a in q:
                continue
            for d in delta_vectors(z, a):
                ext.append((ci, a, d))
    allcols = columns + [("ext", e) for e in ext]
    n = len(allcols)
    neq = []

    def eq(coeff, target, kind, idx):
        if any(coeff) or target != 0:
            neq.append({"coefficients": coeff, "target": target, "kind": kind, "indices": idx})

    # linking: sum_delta m_{ci,a,delta} - n_ci = 0
    by_link = {}
    for k, (ci, a, d) in enumerate(ext):
        by_link.setdefault((ci, a), []).append(nbase + k)
    for (ci, a), ks in by_link.items():
        c = [0] * n
        c[ci] = -1
        for k in ks:
            c[k] = 1
        eq(c, 0, "link", [ci, a])
    for a in range(7):
        for P in comps[a]:
            p = len(P)
            dK = [0] * n
            for k, (ci, aa, d) in enumerate(ext):
                if aa == a:
                    dK[nbase + k] = sum(d[j] for j in P)
            # N1: G not containing a
            for G in RECT:
                if a in G:
                    continue
                gi = RI[G]
                c = [0] * n
                for k, (ci, aa, d) in enumerate(ext):
                    if aa != a:
                        continue
                    qi, si, z = columns[ci]
                    v = dK[nbase + k] * z[gi] + (dK[nbase + k] if qi == gi else 0)
                    c[nbase + k] = v
                eq(c, 0, "N1", [a, list(P), gi])
            for j in range(7):
                if j == a:
                    continue
                c3 = [0] * n
                c3s = [0] * n
                for k, (ci, aa, d) in enumerate(ext):
                    if aa != a:
                        continue
                    qi, si, z = columns[ci]
                    c3[nbase + k] = dK[nbase + k] * z[rq(a, j)]
                    c3s[nbase + k] = dK[nbase + k] * d[j]
                eq(c3, 0, "N3", [a, list(P), j])
                eq(c3s, 8 * (6 - p) if j in P else -8 * p, "N3s", [a, list(P), j])
                c4 = [0] * n
                for k, (ci, aa, d) in enumerate(ext):
                    if aa != a:
                        continue
                    qi, si, z = columns[ci]
                    if j in RECT[qi]:
                        c4[nbase + k] = dK[nbase + k]
                eq(c4, 0, "N4", [a, list(P), j])
    # pad base equations and bounds to the new width
    for e in equations:
        e["coefficients"] = list(e["coefficients"]) + [0] * (n - nbase)
    for b in bounds:
        b["coefficients"] = list(b["coefficients"]) + [0] * (n - nbase)
    return allcols, equations + neq, bounds, len(ext)


def recheck(cols, equations, bounds, cert):
    """Recompute the certificate from the stored rows in integers (generic: uses the coefficient lists)."""
    key = lambda e: (e["kind"], json.dumps(e["indices"]))
    eqs = {key(e): e for e in equations}
    bds = {key(b): b for b in bounds}
    vec = [0] * len(cols)
    const = 0
    for term in cert["equation_multipliers"]:
        e = eqs[key(term)]
        w = term["multiplier"]
        assert type(w) is int
        vec = [a + w * b for a, b in zip(vec, e["coefficients"])]
        const += w * e["target"]
    for term in cert["upper_bound_multipliers"]:
        b = bds[key(term)]
        w = term["multiplier"]
        assert type(w) is int and w >= 0
        vec = [a + w * c for a, c in zip(vec, b["coefficients"])]
        const += w * b["upper"]
    assert min(vec) >= 0 and const < 0
    return const


if __name__ == "__main__":
    path, first, last = sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    only = None
    if "--only" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")}
    base_moments = "--no-base-moments" not in sys.argv
    for idx, t in enumerate(records(path)):
        if idx < first or (only is not None and idx not in only):
            continue
        if idx >= last:
            break
        t0 = time.time()
        cat = dfs_catalogue(t)
        cols, eqs, bds, next_ = build(t, cat, base_moments)
        cert = find_certificate(cols, eqs, bds)
        out = {"index": idx, "dim": t.get("kernel_dimension"), "k": 21 - len(t["nongrid_edges"]),
               "columns": len(cols), "ext_columns": next_, "equations": len(eqs), "status": cert["status"],
               "lp_status_code": cert.get("lp_status_code")}
        if cert["status"] == "EXCLUDED_BY_INTEGER_CERTIFICATE":
            out["constant"] = recheck(cols, eqs, bds, cert)
            out["kinds"] = sorted({m["kind"] for m in cert["equation_multipliers"]})
        out["seconds"] = round(time.time() - t0, 1)
        print(json.dumps(out), flush=True)
