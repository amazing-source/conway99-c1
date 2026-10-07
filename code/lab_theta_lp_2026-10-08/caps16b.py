"""C1, lab session. Exact LP at d = 32 (r = 33) under set "ext" and the caps a_7 <= 7920, b_1 <= 3784, a_8 <= CAP.
  python caps16b.py <N> <CAP> [<CAP> ...]     writes certificates_caps16_N<N>.json (Farkas multipliers for "a_7 = 0")"""
import sys, json
from fractions import Fraction as Fr
import theta_lp as T
import theta_lp_exact as X
T.selfcheck(); out = []
for cap in [int(x) for x in sys.argv[2:]]:
    A, B, C = X.build(32, "ext")
    C.append(("a_7 <= 7920", T.add(T.aff(7920), A[7], -1))); C.append(("b_1 <= 3784", T.add(T.aff(3784), B[1], -1))); C.append(("a_8 <= %d" % cap, T.add(T.aff(cap), A[8], -1)))
    lo7 = X.minimise(C, A[7]); lo79 = X.minimise(C, T.add(A[7], A[9])); lo9 = X.minimise(C, A[9])
    C0 = C + [("a_7 <= 0", T.sc(A[7], -1))]; st = X.feasible(C0); assert st[0] == "infeasible"
    out.append({"d": 32, "cap_a8": cap, "min_a7": str(lo7[1]), "certificate_a7_zero": [[nm, str(l)] for nm, l in st[1]]})
    print("r = 33, a_8 <= %d: min a_7 = %s = %.4f; min a_9 = %s; min (a_7 + a_9) = %.2f; 'a_7 = 0' infeasible, certificate on: %s" % (
        cap, lo7[1], float(lo7[1]), X.show(lo9[1]), float(lo79[1]), ", ".join(nm for nm, _ in st[1])), flush=True)
json.dump(out, open("certificates_caps16_N%d.json" % X.N, "w"), indent=1)
