"""C1, lab session. Farkas certificates for the cases using the stronger dual bounds ("ext2", "ext3") and the caps.
  python certificates2.py <N> write | check        file certificates2_N<N>.json
Each case: (mode string for theta_lp_exact.build, d). Certificate = list of (constraint label, positive rational lambda);
check: sum lambda_i coef_i = 0 in the seven coordinates and sum lambda_i const_i < 0, forms rebuilt from the q-expansions."""
import sys, json
from fractions import Fraction as Fr
import theta_lp_exact as X
N = X.N; FILE = "certificates2_N%d.json" % N
CASES = [("ext2", 28), ("ext3", 28), ("ext2+caps", 30), ("ext2+caps", 32), ("ext3+caps", 30), ("ext3+caps", 32), ("ext3+caps+min:10", 34)]
if sys.argv[2] == "write":
    out = []
    for mode, d in CASES:
        A, B, C = X.build(d, mode); st = X.feasible(C); assert st[0] == "infeasible", (mode, d)
        out.append({"mode": mode, "d": d, "r": d + 1, "certificate": [[nm, str(l)] for nm, l in st[1]]}); print("%s d = %d: %s" % (mode, d, ", ".join(nm for nm, _ in st[1])), flush=True)
    json.dump({"N": N, "cases": out}, open(FILE, "w"), indent=1)
else:
    data = json.load(open(FILE)); good = 0
    for case in data["cases"]:
        A, B, C = X.build(case["d"], case["mode"]); form = dict(C); assert len(form) == len(C)
        lam = [(form[nm], Fr(s)) for nm, s in case["certificate"]]
        ok = all(l > 0 for _, l in lam) and all(sum(l * f[k] for f, l in lam) == 0 for k in range(1, 8)) and sum(l * f[0] for f, l in lam) < 0
        good += ok; print("%-18s d = %2d (r = %2d): %s  [%s]" % (case["mode"], case["d"], case["r"], "certificate verified" if ok else "FAIL", ", ".join(nm for nm, _ in case["certificate"])))
    print("%d of %d certificates verified" % (good, len(data["cases"]))); sys.exit(0 if good == len(data["cases"]) else 1)
