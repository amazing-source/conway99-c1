"""Exploration at b = 30: smallest c_9 (norm-18 vectors of B) as a function of upper bounds on c_7 and c_8."""
from fractions import Fraction
import exact_lp as X
from theta7_c8 import system

for X7, X8 in ((7920, 360360), (2000, 100000), (500, 20000), (100, 5000), (0, 0)):
    MA, MWB, E, e, G, g = system(30, {("a", 2): 462, ("a", 4): 14970}, {("c", 7): X7, ("c", 8): X8})
    v = X.optimum(MWB[9], E, e, G, g, 15, sense=-1)
    w = X.optimum(MWB[10], E, e, G, g, 15, sense=-1)
    print("c_7 <= %d, c_8 <= %d: min c_9 = %s, min c_10 = %s" % (X7, X8, float(v) if v not in (None, "unbounded") else v,
                                                               float(w) if w not in (None, "unbounded") else w), flush=True)
