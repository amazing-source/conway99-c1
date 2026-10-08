"""C1, lab session, 2026-10-08. All 0/+-1 representatives of small projected norm with support at most 10, from census2.

  python reps10.py <census2 json> <out json> [max order]

For every admissible type H of order n <= max order and every split of ALL its vertices into W (+1) and Y (-1) with
|W| - |Y| divisible by 3:  Q = 3 n - 2 (e(W) + e(Y) - e(W,Y)) + (|W| - |Y|)^2 / 9.
The number of signed vectors psi = 1_W - 1_Y of the hypothetical graph with a given (|W|, |Y|, Q) is
    sum over H of N_H * #(splits of H with that data),   N_H = x_H / |Aut H|,
both signs being counted because (W, Y) and (Y, W) are both enumerated. Output: for Q = 4, 6, 8 and every shape (a, b),
the count as an affine form in the census parameters. These are REPRESENTATIVES: distinct vectors psi, not distinct
classes of M (no collision is removed here). One process; memory below 2 GB."""
import sys, json, time
from fractions import Fraction as Fr
from itertools import combinations
import census2 as C2
t0 = time.time(); D = json.load(open(sys.argv[1])); nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 10
out = {}; pc = lambda x: bin(x).count("1")
for n in range(2, nmax + 1):
    full = (1 << n) - 1; shapes = [(a, n - a) for a in range(n + 1) if (2 * a - n) % 3 == 0]; used = 0
    for key, rows, aut, form in D["types"][str(n)]:
        e_tot = sum(pc(r) for r in rows) // 2; tally = {}
        if 3 * n - 2 * e_tot > 8 + 0 and all(True for _ in ()): pass
        for a, b in shapes:
            s2 = Fr((a - b) ** 2, 9)
            for W in combinations(range(n), a):
                wm = 0
                for i in W: wm |= 1 << i
                ym = full & ~wm; ew = sum(pc(rows[i] & wm) for i in W) // 2; cross = sum(pc(rows[i] & ym) for i in W); ey = e_tot - ew - cross
                Q = 3 * n - 2 * (ew + ey - cross) + s2
                if Q in (4, 6, 8): tally[(a, b, int(Q))] = tally.get((a, b, int(Q)), 0) + 1
        if not tally: continue
        used += 1; au = aut if aut else C2.aut_order(n, rows)
        for k_, c in tally.items():
            acc = out.setdefault(k_, {})
            for p, val in form.items(): acc[p] = acc.get(p, 0) + Fr(val) * c / au
    print("order %d done: %d types carry representatives of norm <= 8  [%.0f s]" % (n, used, time.time() - t0), flush=True)
res = {"%d,%d,%d" % k_: {p: str(val) for p, val in f.items() if val} for k_, f in sorted(out.items())}
json.dump(res, open(sys.argv[2], "w"))
for k_, f in sorted(out.items(), key=lambda kv: (kv[0][2], kv[0][0] + kv[0][1], kv[0])):
    print("  shape (%d,%d) norm %d: constant term %s, %d parameters" % (k_[0], k_[1], k_[2], f.get("0", 0), len([p for p, val in f.items() if val and p != "0"])))
