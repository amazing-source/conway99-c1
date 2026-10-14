"""For each remaining rank b, the smallest norm 2n such that B must contain a nonzero vector of norm <= 2n
(largest m with c_7 = ... = c_m = 0 still feasible; then some c_k > 0 for 7 <= k <= m + 1), with the proved bounds
a_2 >= 462, a_4 >= 14970, c_7 <= 7920, c_8 <= 360360 (NOTE_NIGHT 19-20). Exact arithmetic."""
from fractions import Fraction
import exact_lp as X
from theta7_c8 import system

for b in range(30, 44, 2):
    MA, MWB, E, e, G, g = system(b, {("a", 2): 462, ("a", 4): 14970}, {("c", 7): 7920, ("c", 8): 360360})
    m = 6
    while m < 20:
        E2 = E + [MWB[k] for k in range(7, m + 2)]
        e2 = e + [0] * (m + 2 - 7)
        ok, _ = X.feasible(E2, e2, G, g, 15)
        if not ok:
            break
        m += 1
    print("b = %d: B must contain a vector of norm <= %d (c_7..c_%d = 0 is feasible, adding c_%d = 0 is not)"
          % (b, 2 * (m + 1), m, m + 1), flush=True)
