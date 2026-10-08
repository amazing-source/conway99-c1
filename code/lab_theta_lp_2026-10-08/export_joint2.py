"""C1, lab session, 2026-10-08. Exact data of the joint LP of lp_joint2.py, for an independent rational certificate.
  python export_joint2.py <census2 order-10 json> <reps10 json> <out json>
Numbering: parameter p (1..549) is the p-th entry of "params" in the census file; "0" is the constant term.
All coefficients are exact rationals written as strings. Nothing is solved here."""
import sys, json, hashlib
from fractions import Fraction as Fr
D = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); pc = lambda x: bin(x).count("1")
npar = len(D["params"])
g = [i for i, p in enumerate(D["params"]) if p[0] == 9 and sum(pc(x) for x in p[2]) // 2 == 18][0]
r8 = {}; shapes = {}
for k_, f in sorted(R.items()):
    a_, b_, q_ = (int(x) for x in k_.split(","))
    if a_ + b_ > 9 or q_ != 8: continue
    shapes[k_] = f
    for p, v_ in f.items(): r8[p] = r8.get(p, Fr(0)) + Fr(v_)
seen = set(); rows = []
for n in ("6", "7", "8", "9", "10"):
    for key, rws, aut, form in D["types"][n]:
        sig = tuple(sorted(form.items()))
        if sig in seen or not form: continue
        seen.add(sig); rows.append(form)
out = {
    "what": "joint LP of lp_joint2.py (rank 37): maximise ceiling - floor; exclusion at c when the maximum is negative",
    "census_file_sha256": hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest(),
    "reps_file_sha256": hashlib.sha256(open(sys.argv[2], "rb").read()).hexdigest(),
    "numbering": "1-based position in params of the census file; key 0 = constant term",
    "params": [[p[0], p[1], p[2]] for p in D["params"]],
    "index_P": 1, "index_rho": g + 1, "index_F10": 438,
    "r8": {p: str(v_) for p, v_ in sorted(r8.items(), key=lambda kv: int(kv[0])) if v_},
    "r8_by_shape": shapes,
    "Phi": R["6,3,4"],
    "census_positivity_rows": "not copied (%d distinct forms): every induced type of orders 6..10 of the census file, field form" % len(rows),
    "variables": ["x_1..x_549", "tau", "a7", "a8", "a9", "a10", "b1", "b2", "b3"],
    "constraints": [
        "every form of census_positivity_rows >= 0 (all induced types of orders 6..10, duplicates removed)", "x_p >= 0",
        "4 tau <= Phi", "tau <= 2 P + 3 rho", "17 tau <= 17 P + 105 rho", "tau <= 1403", "P + 5 rho <= 1386", "tau <= P + 5 rho + 17",
        "a7 <= 842", "21 a7 <= 2 N(F10)", "7 a7 + 8 a8 <= 55440", "b1 <= 44", "b2 >= 462 + 41 b1 (lp_joint2) ; lp_joint3 uses the 22 secants of 462 + 41 b1 + b1^2/2 at consecutive even b1 and P >= 6 rho", "b3 >= 45898",
        "a11 = -133154 - 406 a7 - 125 a8 - 34 a9 - 7 a10 + 5726 b1 + 273 b2 + 7 b3 >= 0",
        "a12 = 736358 + 1183 a7 + 350 a8 + 91 a9 + 13 a10 - 2429 b1 - 476 b2 - 21 b3 >= 0",
        "a13 = 1260308 + 378 a7 + 98 a8 + 7 a9 + 6 a10 + 25830 b1 + 70 b2 - 7 b3 >= 0",
        "tau, a7, a8, a9, a10, b1, b2, b3 >= 0"],
    "objective": "maximise  [14006902 + 2793 a7 + 532 a8 + 77 a9 + 7 a10 - 8987 b1 - 664 b2 - 35 b3] - [2 r8 - c tau] / 3",
    "r8_definition": "number of signed vectors 1_W - 1_Y, W and Y disjoint, |W| + |Y| <= 9, |W| - |Y| divisible by 3, with "
                     "Q = 3(|W|+|Y|) - 2(e(W) + e(Y) - e(W,Y)) + (|W|-|Y|)^2/9 = 8; both signs counted; no collision removed",
    "floor_hypothesis": "classes of norm 8 >= (2 r8 - C)/3 with C <= c tau (c = collisions charged per twin pair): hypothesis, not proved",
}
json.dump(out, open(sys.argv[3], "w"))
print("parameters %d; index rho %d; r8: constant %s, %d parameters; Phi: %d terms; %d positivity rows; shapes %s" % (
    npar, g + 1, r8.get("0", 0), len([p for p, v_ in r8.items() if v_ and p != "0"]), len(R["6,3,4"]), len(rows), " ".join(sorted(shapes))))
