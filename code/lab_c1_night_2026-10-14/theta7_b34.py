"""Exploration at b = 34: largest a_4 and a_3 as functions of a lower bound on a_5 and a_6 (NOTE_NIGHT 27)."""
import exact_lp as X
from theta7_c8 import system

for L5, L6 in ((3415104, 10869012), (1e7, 10869012), (3e7, 10869012), (3415104, 1e9), (3e7, 5e9)):
    low = {("a", 2): 462, ("a", 3): 24948, ("a", 4): 1749210, ("a", 5): int(L5), ("a", 6): int(L6), ("a", 7): 6503112, ("a", 8): 1555092}
    MA, MWB, E, e, G, g = system(34, low, {("c", 7): 7920, ("c", 8): 360360})
    ok, _ = X.feasible(E, e, G, g, 15)
    if not ok:
        print("a_5 >= %.3g, a_6 >= %.3g: INFEASIBLE" % (L5, L6), flush=True)
        continue
    h4 = X.optimum(MA[4], E, e, G, g, 15, sense=1)
    h3 = X.optimum(MA[3], E, e, G, g, 15, sense=1)
    print("a_5 >= %.3g, a_6 >= %.3g: max a_4 = %.4g, max a_3 = %.4g" % (L5, L6, float(h4), float(h3)), flush=True)
