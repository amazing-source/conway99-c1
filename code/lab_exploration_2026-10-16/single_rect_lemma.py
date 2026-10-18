"""Single-rectangle count obstruction (LAB, 18/10/2026).
Observation: Codex's reduced integer certificates for c <= 2 templates use ONE rectangle Q only: its diagonal moment,
the four-row counts, block symmetry and the degree histogram of Q.  This checker decides that one-rectangle system
exactly (no solver), for every rectangle Q of a template:
  * z_w(F) = |N(w) cap Q_F|; every label's row z_w is one of the integral states of the component equations
    (Codex's row_catalogue: C z = b, 0 <= z_F <= 2 or 4);
  * the four corners of Q choose states (a multiset); their own coordinates are the corner degrees, whose histogram
    must come from a corner graph with e(Q) edges, e <= 2 if Q is non-grid (E3), e = 4 if grid;
  * block symmetry: for every rectangle F != Q, sum over the 4 labels of F of z_w(Q) = K_FQ = K_QF = sum over the corners
    u of Q of z_u(F);
  * diagonal moment (sum of the six C2 equations of the corner pairs of Q): sum over all 84 labels w of C(z_w(Q), 2)
    = 8 - e(Q).
If no choice satisfies all of this, the template is impossible (the system is a relaxation of a real graph).
--local : use only the component equations of the two lines of Q (and of the line pair of each F, for the row
          states of F); this tests whether the obstruction depends on the two lines of Q alone.
usage: python single_rect_lemma.py <codex dir> <catalogue (open/survivors/templates)> <index> [--local] [--rect a,b]"""
import gzip
import json
import sys
from itertools import combinations, combinations_with_replacement
from pathlib import Path

codex = Path(sys.argv[1])
cat, index = sys.argv[2], int(sys.argv[3])
local = "--local" in sys.argv
only = None
if "--rect" in sys.argv:
    only = tuple(int(x) for x in sys.argv[sys.argv.index("--rect") + 1].split(","))
sys.path.insert(0, str(codex.resolve()))
from root_rectangle_domains import corner_graphs          # noqa: E402

RECT = list(combinations(range(7), 2))
raw = Path(cat).read_bytes()
doc = json.loads(gzip.decompress(raw) if cat.endswith(".gz") else raw)
recs = doc.get("open") or doc.get("survivors") or doc.get("templates")
rec = recs[index]
t = rec.get("template", rec)
parts_by_line = []
for root, nontrivial in enumerate(t["nontrivial_component_groups"]):
    parts = [tuple(p) for p in nontrivial]
    used = {j for p in parts for j in p}
    parts += [(j,) for j in range(7) if j != root and j not in used]
    parts_by_line.append(parts)
nongrid = {tuple(e) for e in t["nongrid_edges"]}


def equations_for(q, lines):
    """Component equations (Codex's form) restricted to the given lines, for a label of rectangle q."""
    eqs = []
    for root in lines:
        for part in parts_by_line[root]:
            support = {tuple(sorted((root, j))) for j in part}
            coeff = [int(F in support) for F in RECT]
            rhs = 3 * int(q in support) + len(part) * (1 - int(root in q)) - sum(j in part for j in q)
            eqs.append((coeff, rhs))
    return eqs


_cache = {}


def states(q, lines):
    """All integral rows z with the bounds and the component equations of `lines`.  Coordinates involved in no chosen
    equation are reported as None (only their bound applies).  Exact affine parametrization (as in Codex's
    row_catalogue): RREF of the equations on the involved coordinates, enumeration of the free ones within bounds."""
    key = (q, tuple(lines))
    if key in _cache:
        return _cache[key]
    import numpy as np
    import sympy as sp
    from math import lcm
    from itertools import product
    eqs = equations_for(q, lines)
    involved = sorted({F for coeff, _ in eqs for F in range(21) if coeff[F]})
    upper = [2 if set(RECT[F]) & set(q) else 4 for F in range(21)]
    if not involved:
        _cache[key] = ([tuple([None] * 21)], upper)
        return _cache[key]
    A = sp.Matrix([[coeff[F] for F in involved] for coeff, _ in eqs])
    b = sp.Matrix([rhs for _, rhs in eqs])
    red, piv = A.row_join(b).rref()
    n = len(involved)
    if any(pv >= n for pv in piv):
        _cache[key] = ([], upper)
        return _cache[key]
    free = [i for i in range(n) if i not in piv]
    offset = sp.zeros(n, 1); lin = sp.zeros(n, len(free))
    for row, pv in enumerate(piv):
        offset[pv] = red[row, n]
        for j, f in enumerate(free):
            lin[pv, j] = -red[row, f]
    for j, f in enumerate(free):
        lin[f, j] = 1
    den = lcm(*([x.q for x in list(offset) + list(lin)] + [1]))
    oi = np.array((offset * den).tolist(), dtype=np.int64).reshape(-1)
    li = np.array((lin * den).tolist(), dtype=np.int64).reshape(n, len(free))
    ub = np.array([upper[F] for F in involved], dtype=np.int64)
    ranges = [range(int(ub[f]) + 1) for f in free]
    out = []
    if free:
        grid = np.array(list(product(*ranges)), dtype=np.int64)
        num = grid @ li.T + oi
    else:
        num = oi.reshape(1, -1)
    ok = np.all((num % den == 0) & (num >= 0) & (num <= ub * den), axis=1)
    for row in (num[ok] // den).tolist():
        z = [None] * 21
        for F, v in zip(involved, row):
            z[F] = int(v)
        out.append(tuple(z))
    _cache[key] = (out, upper)
    return _cache[key]


def allowed_histograms(e):
    hs = set()
    for _, _, h in corner_graphs(e):
        degrees = [2 - x for x in h]
        hs.add(tuple(degrees.count(v) for v in range(3)))
    return hs


def check_rectangle(qi):
    q = RECT[qi]
    lines_q = list(q) if local else list(range(7))
    st_q, upper_q = states(q, lines_q)
    # projected values of z(Q) for the labels of each other rectangle F, with their own local equations
    proj = {}
    for fi, F in enumerate(RECT):
        if fi == qi:
            continue
        lines_f = sorted(set(q) | set(F)) if local else list(range(7))
        st_f, upper_f = states(F, lines_f)
        vals = sorted({s[qi] for s in st_f if s[qi] is not None}) if st_f else []
        if not st_f:
            return {"rectangle": q, "status": "EXCLUDED", "reason": "no row state for rectangle %s" % (F,)}
        if not vals:                       # z(Q) unconstrained by the chosen equations: only the bound
            vals = list(range(upper_f[qi] + 1))
        pairs = {(0, 0)}
        for _ in range(4):
            pairs = {(s + v, c + v * (v - 1) // 2) for s, c in pairs for v in vals}
        by_sum = {}
        for s, c in pairs:
            by_sum.setdefault(s, set()).add(c)
        proj[fi] = by_sum
    grid = q not in nongrid
    edges_allowed = [4] if grid else [0, 1, 2]
    hist_ok = {e: allowed_histograms(e) for e in edges_allowed}
    seen_k = set()
    for M in combinations_with_replacement(range(len(st_q)), 4):
        rows = [st_q[i] for i in M]
        deg = [r[qi] for r in rows]
        if any(d is None for d in deg):
            continue
        two_e = sum(deg)
        if two_e % 2:
            continue
        e = two_e // 2
        if e not in hist_ok or tuple(deg.count(v) for v in range(3)) not in hist_ok[e]:
            continue
        own = sum(d * (d - 1) // 2 for d in deg)
        need = 8 - e - own
        if need < 0:
            continue
        K = []
        for fi in range(21):
            if fi == qi:
                continue
            vs = [r[fi] for r in rows]
            K.append((fi, None if any(v is None for v in vs) else sum(vs)))
        key = (e, own, tuple(K))
        if key in seen_k:
            continue
        seen_k.add(key)
        tot = {0}
        ok = True
        for fi, k in K:
            if k is None:
                opts = set().union(*proj[fi].values())
            else:
                opts = proj[fi].get(k)
                if not opts:
                    ok = False
                    break
            tot = {a + b for a in tot for b in opts if a + b <= need}
            if not tot:
                ok = False
                break
        if ok and need in tot:
            return {"rectangle": q, "status": "PASSES"}
    return {"rectangle": q, "status": "EXCLUDED", "reason": "no consistent corner multiset"}


results = []
for qi, q in enumerate(RECT):
    if only is not None and q != only:
        continue
    r = check_rectangle(qi)
    results.append(r)
    if r["status"] == "EXCLUDED" and only is None:
        break
excl = [r for r in results if r["status"] == "EXCLUDED"]
print(json.dumps({"index": index, "local": local, "status": "EXCLUDED" if excl else "PASSES",
                  "by": excl[0] if excl else None, "rectangles_checked": len(results)}))
