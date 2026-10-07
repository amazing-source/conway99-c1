"""C1, lab session. Writes, then re-reads and re-checks, the exact Farkas certificates of theta_lp_exact.py.

  python certificates.py <N> write     -> certificates_N<N>.json
  python certificates.py <N> check     -> re-verifies every certificate of that file (no simplex: only the three exact tests)

A certificate for (mode, d) is a list of (constraint label, lambda) with lambda > 0 rational. Check: with the affine forms
const_i + coef_i . beta of the labelled constraints (rebuilt from the q-expansions), sum lambda_i coef_i = 0 in all seven
coordinates and sum lambda_i const_i < 0. Since every constraint says const_i + coef_i . beta >= 0, no beta exists.
Cases written: mode "ext" for d = 2..26, mode "ext+a7" for d = 28, 30 (a_7 = 0 is Codex's lemma: norm 14 forces r >= 33)."""
import sys, json
from fractions import Fraction as Fr
import theta_lp_exact as X
N = X.N; FILE = "certificates_N%d.json" % N
CASES = [("ext", d) for d in range(2, 28, 2)] + [("ext+a7", 28), ("ext+a7", 30)]

if sys.argv[2] == "write":
    out = []
    for mode, d in CASES:
        A, B, C = X.build(d, mode); st = X.feasible(C); assert st[0] == "infeasible", (mode, d)
        out.append({"mode": mode, "d": d, "r": d + 1, "certificate": [[nm, str(l)] for nm, l in st[1]]})
        print("%s d = %d: certificate on %d constraints" % (mode, d, len(st[1])), flush=True)
    json.dump({"N": N, "cases": out}, open(FILE, "w"), indent=1)
else:
    data = json.load(open(FILE)); assert data["N"] == N; good = 0
    for case in data["cases"]:
        A, B, C = X.build(case["d"], case["mode"]); form = dict(C); assert len(form) == len(C)
        lam = [(form[nm], Fr(s)) for nm, s in case["certificate"]]
        ok = all(l > 0 for _, l in lam) and all(sum(l * f[k] for f, l in lam) == 0 for k in range(1, 8)) and sum(l * f[0] for f, l in lam) < 0
        good += ok; print("%-7s d = %2d (r = %2d): %s  [%s]" % (case["mode"], case["d"], case["r"], "certificate verified" if ok else "FAIL", ", ".join(nm for nm, _ in case["certificate"])))
    print("%d of %d certificates verified" % (good, len(data["cases"]))); sys.exit(0 if good == len(data["cases"]) else 1)
