"""C1, lab session. 3-side: forced short vectors, with the larger set of forced dual vectors LOWS2 (NOTE.md section 11).
For each d: the largest threshold t such that "no vector of projected norm nu < t in any class" is feasible (3-ladder), and
the exact minimum of the number of vectors with nu < t' for several t'.     python theta3_ladder.py <N> [d ...]"""
import sys
from fractions import Fraction as Fr
import theta3 as H
H.test_toy(); H.test_fricke()
LOWS2 = {3: 1386, 4: 12474, 5: 182952, 6: 1521828, 7: 5987560, 9: 3076920}
V = H.variables(); nus = sorted({v[1] for v in V})
ds = [int(x) for x in sys.argv[2:]] or list(range(34, 44, 2))
for d in ds:
    if H.solve(d, lows=LOWS2)[0] == "infeasible": print("d = %d (r = %d): INFEASIBLE" % (d, d + 1), flush=True); continue
    lad = None
    for t in nus:
        if H.solve(d, zero={v for v in V if v[1] < t}, lows=LOWS2)[0] == "infeasible": break
        lad = t
    line = "d = %d (r = %d): shells nu < %s may all be empty, nu <= %s not;" % (d, d + 1, lad, lad)
    for tp in (13, 15, 17, 19, 21):
        r = H.solve(d, objective={v for v in V if v[1] < tp}, lows=LOWS2)
        line += " N(nu<%d) >= %s;" % (tp, ("%.6g" % float(r[1])) if r[0] == "feasible" else r[0])
    print(line, flush=True)
