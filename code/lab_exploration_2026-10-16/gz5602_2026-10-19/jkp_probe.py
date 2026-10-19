"""Joint known-structure + profile probe for ONE c3 template (LAB 19/10/2026, exploratory: CP-SAT, no proof).
Known rectangles K = all grids of the template + every non-grid rectangle appearing in a forced two-term relation
(H_A = -H_B or H_A = H_B, exact kernel W).  Variables: adjacency E(w, v) between every label w and every KNOWN label v
(no outside-outside variable).  Constraints (all exact consequences of srg(99,14,1,2) at the root):
  * W-relations: for every row w, every vector c of W supported on K: sum_F c_F (base(w,F) - z_w(F)) = 0; for KNOWN
    rows every vector of a basis of W (outside columns are known-outside edges, which exist as variables);
  * grids: z_w(F) = base(w, F) (part of W);
  * letter quotas: known rows exact, outside rows upper bounds (their outside part is unknown);
  * C2: known pairs exact (all their edges exist); known-outside and outside-outside pairs: common KNOWN neighbours
    + shared letters + adjacency (if a variable) <= 2.
usage: python jkp_probe.py <catalogue.json.gz> <index> [--time=120] [--no-c2]"""
import gzip
import json
import sys
from fractions import Fraction
from itertools import combinations, product

from ortools.sat.python import cp_model

recs = json.load(gzip.open(sys.argv[1]))["open"]
idx = int(sys.argv[2])
TL = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--time=")), 120))
NOC2 = "--no-c2" in sys.argv
t = recs[idx]["template"]
RECT = list(combinations(range(7), 2)); ridx = {q: i for i, q in enumerate(RECT)}
ng = {tuple(e) for e in t["nongrid_edges"]}
grids = [q for q in RECT if q not in ng]


def W_rows():
    rows = []
    for q in grids:
        v = [0] * 21; v[ridx[q]] = 1; rows.append(v)
    for a, groups in enumerate(t["nontrivial_component_groups"]):
        for P in groups:
            v = [0] * 21
            for j in P:
                v[ridx[tuple(sorted((a, j)))]] = 1
            rows.append(v)
    return rows


def rref(rows):
    rows = [[Fraction(x) for x in r] for r in rows]; piv = []; r = 0
    for c in range(21):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]; rows[r] = [x / rows[r][c] for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    return rows[:r], piv


def in_W(B, v):
    rows, piv = B; v = [Fraction(x) for x in v]
    for row, c in zip(rows, piv):
        if v[c] != 0:
            f = v[c]; v = [x - f * y for x, y in zip(v, row)]
    return all(x == 0 for x in v)


B = rref(W_rows())
assert 21 - len(B[0]) == t["kernel_dimension"]
two = set()
for A, Bq in combinations(sorted(ng), 2):
    for sg in (1, -1):
        v = [0] * 21; v[ridx[A]] = 1; v[ridx[Bq]] = sg
        if in_W(B, v):
            two |= {A, Bq}
K = set(grids) | two
# relations supported on K: basis of W intersected with span(e_F, F in K): W rows already in K plus combinations;
# compute by RREF of W with the non-K columns first (eliminate them).
order = [ridx[q] for q in RECT if q not in K] + [ridx[q] for q in RECT if q in K]
Wr = [[r[c] for c in order] for r in B[0]]
Wr2, piv2 = rref([[x for x in r] + [0] * 0 for r in Wr]) if Wr else ([], [])
nK = 21 - len(K)
WK = [r for r, p in zip(Wr2, piv2) if p >= nK]          # rows with no non-K column (pivot beyond the non-K block)
WK = [[r[order.index(i)] for i in range(21)] for r in WK]
WALL = B[0]
LAB = [(2 * i + s, 2 * j + u) for (i, j) in RECT for s, u in product(range(2), repeat=2)]
rect_of = [RECT[k // 4] for k in range(84)]
known = [k for k in range(84) if rect_of[k] in K]
kset = set(known)


def base(q, f):
    return 2 if q == f else (0 if set(q) & set(f) else 1)


m = cp_model.CpModel()
E = {}


def e(a, b):
    a, b = min(a, b), max(a, b)
    if (a, b) not in E:
        E[(a, b)] = m.NewBoolVar("")
    return E[(a, b)]


def z(w, F):
    return sum(e(w, v) for v in range(84) if rect_of[v] == F and v != w)


for w in range(84):
    rels = WALL if w in kset else WK
    for c in rels:
        if all(x == 0 for x in c):
            continue
        den = 1
        for x in c:
            den = den * x.denominator // __import__("math").gcd(den, x.denominator)
        ci = [int(x * den) for x in c]
        if w in kset:
            m.Add(sum(ci[ridx[F]] * (base(rect_of[w], F) - z(w, F)) for F in RECT if ci[ridx[F]]) == 0)
        else:
            m.Add(sum(ci[ridx[F]] * (base(rect_of[w], F) - z(w, F)) for F in RECT if ci[ridx[F]]) == 0)
LM = [[v for v in range(84) if l in LAB[v]] for l in range(14)]
for w in range(84):
    for l in range(14):
        quota = 2 - int(l in LAB[w]) - int((l ^ 1) in LAB[w])
        if w in kset:
            m.Add(sum(e(w, v) for v in LM[l] if v != w) == quota)
        else:
            m.Add(sum(e(w, v) for v in LM[l] if v in kset) <= quota)
if not NOC2:
    AND = {}

    def andv(a, b, c):           # E(a,c) and E(b,c)
        key = (min(a, b), max(a, b), c)
        if key not in AND:
            x = m.NewBoolVar(""); p, q = e(a, c), e(b, c)
            m.AddImplication(x, p); m.AddImplication(x, q); m.AddBoolOr([p.Not(), q.Not(), x])
            AND[key] = x
        return AND[key]
    for u, v in combinations(range(84), 2):
        sh = len(set(LAB[u]) & set(LAB[v]))
        both = u in kset and v in kset
        if not (u in kset or v in kset) and False:
            pass
        mids = [w for w in range(84) if w not in (u, v) and (both or w in kset)]
        com = [andv(u, v, w) for w in mids]
        adj = [e(u, v)] if (u in kset or v in kset) else []
        if both:
            m.Add(sum(com) + sh + sum(adj) == 2)
        else:
            m.Add(sum(com) + sh + sum(adj) <= 2)
s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = TL; s.parameters.num_search_workers = 2
st = s.StatusName(s.Solve(m))
print(json.dumps({"index": idx, "kernel_dimension": t["kernel_dimension"], "grids": ["%d%d" % q for q in grids],
                  "known_rectangles": ["%d%d" % q for q in RECT if q in K], "known_labels": len(known),
                  "relations_on_K": len(WK), "variables": len(E), "status": st, "wall": round(s.WallTime(), 1),
                  "no_c2": NOC2}))
