"""Exploration: ranges of the shells at b = 32 and 34 under all proved bounds (NOTE_NIGHT 25)."""
import sys
import exact_lp as X
from theta7_c8 import system

low = {("a", 2): 462, ("a", 3): 24948, ("a", 4): 1749210, ("a", 5): 3415104, ("a", 6): 10869012, ("a", 7): 6503112, ("a", 8): 1555092}
up = {("c", 7): 7920, ("c", 8): 360360}
for b in [int(t) for t in sys.argv[1:]]:
    MA, MWB, E, e, G, g = system(b, low, up)
    out = []
    for name, row in [("a%d" % n, MA[n]) for n in (1, 2, 3, 4, 5, 6, 7, 8)] + [("c%d" % n, MWB[n]) for n in (7, 8, 9, 10, 11)]:
        lo = X.optimum(row, E, e, G, g, 15, sense=-1)
        hi = X.optimum(row, E, e, G, g, 15, sense=1)
        f = lambda v: "%.4g" % float(v) if v not in (None, "unbounded") else str(v)
        out.append("%s [%s, %s]" % (name, f(lo), f(hi)))
    print("b=%d: " % b + "; ".join(out), flush=True)
