"""Exploration: ranks b = 24..42 with the shell bounds of NOTE_NIGHT 19 (a_3 >= 930, a_4 >= 14970, a_5 >= 1625)."""
from fractions import Fraction
import exact_lp as X
import theta7_lp as T
from theta7_explore2 import run

for low, up in (({3: 930, 4: 14970, 5: 1625}, {}), ({3: 930, 4: 14970, 5: 1625}, {1: 56}), ({4: 14970}, {})):
    res = [b for b in range(24, 44, 2) if not run(b, low, up)]
    print("low", low, "up", up, ": infeasible ranks among 24..42:", res, flush=True)
