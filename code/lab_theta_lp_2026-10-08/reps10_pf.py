"""C1, lab session, 2026-10-08. Representatives of norm 6 and 8 with support <= 10, split by PRISM CONTENT.

  python reps10_pf.py <census2 json> <out json> [max order]

Same enumeration as reps10.py (every admissible type H, every split of ALL its vertices into W (+1) and Y (-1) with
|W| - |Y| divisible by 3, Q = 3 n - 2 (e(W) + e(Y) - e(W,Y)) + (|W| - |Y|)^2 / 9). Each representative is put in one class:
   "pf"  : neither W nor Y contains an induced prism (6 vertices, all induced degrees 3);
   "fp"  : W or Y contains an induced prism.
Why: two representatives of the same class of M that differ by a twin-prism difference 1_X - 1_X' have
W cap X = A, Y cap X' = B and the partner has X' minus B in W', X minus A in Y'. If both are prism-free then
1 <= |A|, |B| <= 5 (a "two-sided" collision). Full swaps (A = X or B = X') only involve representatives of class "fp".
Output: affine forms in the census parameters for (|W|, |Y|, Q, class). Both signs are counted. One process, < 2 GB."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10
out = {}; pc = lambda x: bin(x).count("1")
for n in range(2, nmax + 1):
    full = (1 << n) - 1; shapes = [(a, n - a) for a in range(n + 1) if (2 * a - n) % 3 == 0]; used = 0
    for key, rows, aut, form in D["types"][str(n)]:
        e_tot = sum(pc(r) for r in rows) // 2; tally = {}; prisms = None
        for a, b in shapes:
            s2 = Fr((a - b) ** 2, 9)
            for W in combinations(range(n), a):
                wm = 0
                for i in W: wm |= 1 << i
                ym = full & ~wm; ew = sum(pc(rows[i] & wm) for i in W) // 2; cross = sum(pc(rows[i] & ym) for i in W); ey = e_tot - ew - cross
                Q = 3 * n - 2 * (ew + ey - cross) + s2
                if Q not in (6, 8): continue
                if prisms is None:
                    prisms = []
                    for S in combinations(range(n), 6):
                        sm = 0
                        for i in S: sm |= 1 << i
                        if all(pc(rows[i] & sm) == 3 for i in S): prisms.append(sm)
                cl = "fp" if any((p & wm) == p or (p & ym) == p for p in prisms) else "pf"
                k_ = (a, b, int(Q), cl); tally[k_] = tally.get(k_, 0) + 1
        if not tally: continue
        used += 1; au = aut if aut else C2.aut_order(n, rows)
        for k_, c in tally.items():
            acc = out.setdefault(k_, {})
            for p, val in form.items(): acc[p] = acc.get(p, 0) + Fr(val) * c / au
    print("order %d done: %d types carry representatives of norm 6 or 8  [%.0f s]" % (n, used, time.time() - t0), flush=True)
res = {"%d,%d,%d,%s" % k_: {p: str(val) for p, val in f.items() if val} for k_, f in sorted(out.items())}
json.dump(res, open(sys.argv[2], "w"))
for k_, f in sorted(out.items(), key=lambda kv: (kv[0][2], kv[0][0] + kv[0][1], kv[0])):
    print("  shape (%d,%d) norm %d class %s: constant %s, coefficient of P %s, %d parameters" % (k_[0], k_[1], k_[2], k_[3], f.get("0", 0), f.get("1", 0), len([p for p, val in f.items() if val and p != "0"])))
