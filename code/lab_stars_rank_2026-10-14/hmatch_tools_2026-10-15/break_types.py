"""Single vs double breaks per pair of label orbits (LAB 15/10/2026, task T3).
For label orbits O = {r, hr}, O' = {r', hr'} (O != O') the 2 x 2 block [[a, b], [c, d]] = Gamma on rows (r, hr) and
columns (r', hr') is h-symmetric iff a = d and b = c.  A block is SINGLY broken if exactly one of a != d, b != c holds
(then the even quotient Gamma_+(O,O') = (a+b+c+d)/2 is a half-integer), DOUBLY broken if both hold (Gamma_+ integral).
Prints q (broken blocks), b (broken edge orbits), the single/double split, and the l / m / cross location of the
broken blocks.  usage: python break_types.py <json> [...]"""
import json, random, sys
sys.path.insert(0, '.')
from stars_rank import build
S, idx, e, F = build([0, 1, 2, 3], random.Random(5))
n = len(S)
hm = {0: 1, 1: 0, 2: 3, 3: 2}
hp = [idx[frozenset(hm.get(y, y) for y in s)] for s in S]
reps = sorted({min(i, hp[i]) for i in range(n)})
def side(i):
    s = S[i]
    return "l" if s & {0, 1} and not s & {2, 3} else ("m" if s & {2, 3} and not s & {0, 1} else "x")
for f in sys.argv[1:]:
    d = json.load(open(f))
    E = {tuple(sorted(x)) for x in d["edges"]}
    G = lambda i, j: 1 if tuple(sorted((i, j))) in E else 0
    single = double = 0
    loc = {}
    plus_half = 0
    for ai, r in enumerate(reps):
        for r2 in reps[ai + 1:]:
            a, b, c, dd = G(r, r2), G(r, hp[r2]), G(hp[r], r2), G(hp[r], hp[r2])
            x, y = a != dd, b != c
            if x or y:
                key = "".join(sorted(side(r) + side(r2)))
                if x and y:
                    double += 1
                    key += "/double"
                else:
                    single += 1
                    key += "/single"
                loc[key] = loc.get(key, 0) + 1
    print("%s: q = %d broken blocks (single %d, double %d), b = %d broken edge orbits; by location %s"
          % (f, single + double, single, double, single + 2 * double, dict(sorted(loc.items()))))
