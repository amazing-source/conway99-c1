"""Independent design model of gz 5602 (LAB 19/10/2026; own formulation, no code of Codex).
Unknowns: for each of the 84 labels w (rectangle q, corner (s_a, s_b) = choice of the letter on each line of q), one
row h_w of the exact catalogue of q (cat5602.py).  Constraints, each a proved consequence (audit 18/10, NUIT_2026-10-19):
  four-sum      R_{F,.} = sum_{w in F} h_w            (R = P^T H), defines R on the 14 non-grid rectangles;
  grid          sum_{w in q} h_w = 0 for a grid q      (R_{q,.} = 0);
  symmetry      R_FG = R_GF;  diagonal R_FF in {2,4,6,8};  R_FG <= 4 (disjoint) or <= 0 (one common line);
  2nd moment    7 R_FG = sum_w h_w(F) h_w(G)          (H^T H = 7R; linear in the row choices);
  letters       sum_{w adjacent to the letter} h_w = 0 for each of the 14 letters  (T B^T = 0).
A feasible point is a concrete first+second-moment 'survivor'; INFEASIBLE is a CP-SAT verdict (no certificate).
usage: python design5602.py <cat5602.json> <seconds> <workers> [out.json]"""
import json
import sys
import time
from itertools import combinations

from ortools.sat.python import cp_model

cat = json.load(open(sys.argv[1]))
seconds, workers = float(sys.argv[2]), int(sys.argv[3])
FLAGS = set(a for a in sys.argv[4:] if a.startswith("--"))
args_out = [a for a in sys.argv[4:] if not a.startswith("--")]
E = cat["edges"]
RECT = ["%d%d" % q for q in combinations(range(7), 2)]
grid = [q for q in RECT if q not in E]
m = cp_model.CpModel()
labels = [(q, sa, sb) for q in RECT for sa in (0, 1) for sb in (0, 1)]
x = {}
h = {}
for (q, sa, sb) in labels:
    rs = cat["rows"][q]
    xs = [m.NewBoolVar("x_%s_%d%d_%d" % (q, sa, sb, i)) for i in range(len(rs))]
    m.AddExactlyOne(xs)
    x[(q, sa, sb)] = (xs, rs)
    h[(q, sa, sb)] = [sum(r[j] * v for r, v in zip(rs, xs)) for j in range(len(E))]


def share(F, G):
    return bool(set(F) & set(G))


R = {}
for F in RECT:
    s = [sum(h[(F, sa, sb)][j] for sa in (0, 1) for sb in (0, 1)) for j in range(len(E))]
    if F in grid:
        for j in range(len(E)):
            m.Add(s[j] == 0)
    else:
        R[F] = s
for i, F in enumerate(E):
    d = m.NewIntVarFromDomain(cp_model.Domain.FromValues([2, 4, 6, 8]), "d_" + F)
    m.Add(R[F][i] == d)
    for j, G in enumerate(E):
        if j <= i:
            continue
        m.Add(R[F][j] == R[G][i])
        m.Add(R[F][j] <= (0 if share(F, G) else 4))
# second moment: 7 R_FG = sum_w h_w(F) h_w(G), linear in the row choices
for i, F in enumerate(E):
    if '--no-moment' in FLAGS:
        break
    for j in range(i, len(E)):
        if '--diag-moment' in FLAGS and j != i:
            continue
        G = E[j]
        m.Add(7 * R[F][j] == sum(r[i] * r[j] * v for (xs, rs) in x.values() for r, v in zip(rs, xs) if r[i] * r[j]))
# letters: letter (a, s) is adjacent to the labels of rectangles {a, b} whose corner uses s on line a
for a in range(7):
    for s in (0, 1):
        ws = []
        for q in RECT:
            qa, qb = int(q[0]), int(q[1])
            if a == qa:
                ws += [(q, s, sb) for sb in (0, 1)]
            elif a == qb:
                ws += [(q, sa, s) for sa in (0, 1)]
        for j in range(len(E)):
            if '--no-letters' not in FLAGS:
                m.Add(sum(h[w][j] for w in ws) == 0)
if '--flipbreak' in FLAGS:
    # the letters of each line a can be exchanged (s_a -> 1 - s_a in every rectangle containing a); for line a pick one
    # non-grid rectangle {a, b(a)} and require sum_{s_b} idx(h_{s_a = 0}) <= sum_{s_b} idx(h_{s_a = 1}); this quantity is
    # invariant under the exchange of any other line, so the 7 conditions can be imposed together (lex-leader).
    for a in range(7):
        q = next(q for q in E if str(a) in q)
        pa = 0 if q[0] == str(a) else 1
        def idx(w):
            xs, rs = x[w]
            return sum(k * v for k, v in enumerate(xs))
        lo = [w for w in [(q, sa, sb) for sa in (0, 1) for sb in (0, 1)] if (w[1] if pa == 0 else w[2]) == 0]
        hi_ = [w for w in [(q, sa, sb) for sa in (0, 1) for sb in (0, 1)] if (w[1] if pa == 0 else w[2]) == 1]
        m.Add(sum(idx(w) for w in lo) <= sum(idx(w) for w in hi_))
if '--codex-e03' in FLAGS:            # Codex 19/10: e03 = e12 = 2 is necessary (H03 = -H12 + C2 bounds)
    m.Add(R['03'][E.index('03')] == 4); m.Add(R['12'][E.index('12')] == 4)
solver = cp_model.CpSolver()
solver.parameters.max_time_in_seconds = seconds
solver.parameters.num_search_workers = workers
t0 = time.time()
st = solver.Solve(m)
name = solver.StatusName(st)
print(json.dumps({"status": name, "wall": round(time.time() - t0, 1), "vars": len(m.Proto().variables),
                  "constraints": len(m.Proto().constraints)}))
if st in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    rows = {"%s_%d%d" % w: [rs[k] for k, v in enumerate(xs) if solver.Value(v)][0] for w, (xs, rs) in x.items()}
    Rv = [[solver.Value(R[F][j]) for j in range(len(E))] for F in E]
    print("R diag", [Rv[i][i] for i in range(len(E))])
    if args_out:
        json.dump({"edges": E, "rows": rows, "R": Rv}, open(args_out[0], "w"))
