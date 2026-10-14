"""Exploration: largest c_14, c_15, c_16 (norms 28, 30, 32 in B) allowed at b = 30 under the proved bounds."""
import exact_lp as X
from theta7_c8 import system
MA, MWB, E, e, G, g = system(30, {("a", 2): 462, ("a", 4): 14970}, {("c", 7): 7920, ("c", 8): 304920})
for n in (14, 15, 16):
    hi = X.optimum(MWB[n], E, e, G, g, 15, sense=1)
    lo = X.optimum(MWB[n], E, e, G, g, 15, sense=-1)
    print("b=30 c_%d in [%.4g, %.4g]" % (n, float(lo), float(hi)), flush=True)
