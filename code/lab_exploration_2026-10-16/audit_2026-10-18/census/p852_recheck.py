"""Re-check of the prism ceiling P <= 852 on the INDEPENDENT census census2.py (LAB 08/10), and the same LP with the
E3 lemma added (LAB, 18/10/2026).

1. Codex's exact certificate (codex_order9_prism_cap.json: 16 order-9 types, weights >= 0) is evaluated on the census2
   family itself: sum_H w_H N_H must be 11088/13 - P identically in the 57 census2 parameters.
2. E3 types: a vertex v, its two lines {v,a,a*}, {v,b,b*}, and the four common neighbours w_xy (x in {a,a*},
   y in {b,b*}, w_xy != v) with exactly three edges among the w_xy.  In a srg(99,14,1,2) any induced 9-set of this
   isomorphism type IS such a configuration (mu(x, y) = 2 forces w_xy to be the second common neighbour of x and y), and
   e(Q) = 3 is impossible (E3), so N_H = 0 for these types.
3. LP (HiGHS, floating point, exploration): maximise P subject to N_H >= 0 for every admissible type of order 2..9,
   without and with the E3 zeros.  An exact certificate is then extracted from the dual and checked in Fractions.
usage: py -3 -I p852_recheck.py <census2 json> <codex_order9_prism_cap.json> <census2.py directory> <out.json>"""
import json
import sys
from fractions import Fraction as Fr
from itertools import combinations

census_path, cap_path, c2dir, out_path = sys.argv[1:5]
sys.path.insert(0, c2dir)
import census2 as C2                                    # noqa: E402  (stdlib only; canonical form)

data = json.load(open(census_path))
NP = len(data["params"])                                 # 57
names = ["1"] + ["N%d_%d" % (n, key) for n, key, rows in data["params"]]
forms = {}                                               # (order, key) -> list of Fr, length NP + 1 (constant first)
for n, lst in data["types"].items():
    for key, rows, aut, form in lst:
        v = [Fr(0)] * (NP + 1)
        for p, val in form.items():
            v[int(p)] = Fr(val) / aut
        forms[(int(n), key)] = v
P_INDEX = 1
assert data["params"][0][0] == 6, "the first parameter must be the order-6 prism"
report = {"census_types": len(forms), "parameters": NP}

# 1. Codex's certificate on the census2 family
cap = json.load(open(cap_path))
pairs9 = list(combinations(range(9), 2))


def rows_from_codex_code(code):
    rows = [0] * 9
    for k, (i, j) in enumerate(pairs9):
        if code >> k & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return rows


total = [Fr(0)] * (NP + 1)
for code, w in cap["certificate"]:
    rows = rows_from_codex_code(int(code))
    key, _ = C2.canon(9, rows)
    assert (9, key) in forms, ("certificate type unknown to census2", code)
    w = Fr(w)
    assert w >= 0
    total = [a + w * b for a, b in zip(total, forms[(9, key)])]
nonzero = {names[i]: str(x) for i, x in enumerate(total) if x}
ok = nonzero == {"1": str(Fr(11088, 13)), names[P_INDEX]: "-1"}
report["codex_certificate_on_census2"] = {"terms": len(cap["certificate"]), "sum": nonzero, "identity_11088_13_minus_P": ok}
print("1. Codex certificate on census2:", nonzero, "->", ok)

# 2. E3 types
V, A, AS, B, BS = 0, 1, 2, 3, 4
W = {(A, B): 5, (A, BS): 6, (AS, B): 7, (AS, BS): 8}
base = [(V, A), (V, AS), (V, B), (V, BS), (A, AS), (B, BS)]
for (x, y), w in W.items():
    base += [(x, w), (y, w)]
labels = list(W.values())
lpairs = list(combinations(labels, 2))


def admissible(rows, n):
    for i in range(n):
        for j in range(i + 1, n):
            c = bin(rows[i] & rows[j]).count("1")
            if (rows[i] >> j & 1 and c > 1) or (not rows[i] >> j & 1 and c > 2):
                return False
    return True


e3_keys, e3_detail = set(), []
for three in combinations(lpairs, 3):
    rows = [0] * 9
    for i, j in base + list(three):
        rows[i] |= 1 << j
        rows[j] |= 1 << i
    if not admissible(rows, 9):
        continue
    key, _ = C2.canon(9, rows)
    assert (9, key) in forms
    e3_keys.add(key)
    e3_detail.append({"Q_edges": [[i, j] for i, j in three], "census2_key": key})
report["E3_types"] = {"admissible_configurations": len(e3_detail), "distinct_types": sorted(e3_keys)}
print("2. E3 configurations: %d admissible, %d distinct types %s" % (len(e3_detail), len(e3_keys), sorted(e3_keys)))

# 3. LP
import numpy as np                                       # noqa: E402
from scipy.optimize import linprog                       # noqa: E402

keys = sorted(forms)
Amat = np.array([[float(x) for x in forms[k][1:]] for k in keys])
bvec = np.array([float(forms[k][0]) for k in keys])
c = np.zeros(NP)
c[P_INDEX - 1] = -1.0                                    # maximise P


def solve(extra_zero):
    # N_H = b + A x >= 0  <=>  -A x <= b ;  N_E = 0 for E in extra_zero
    eq = [i for i, k in enumerate(keys) if k[0] == 9 and k[1] in extra_zero]
    res = linprog(c, A_ub=-Amat, b_ub=bvec, A_eq=Amat[eq] if eq else None, b_eq=-bvec[eq] if eq else None,
                  bounds=[(None, None)] * NP, method="highs")
    return res, eq


def exact_certificate(res, eq):
    """Rationalise the dual and verify exactly; returns (bound, support) or None."""
    y = -np.array(res.ineqlin.marginals)                 # multipliers of N_H >= 0
    z = -np.array(res.eqlin.marginals) if eq else np.array([])
    for denom in (10 ** 4, 10 ** 6, 10 ** 8, 10 ** 10):
        yr = [Fr(v).limit_denominator(denom) if v > 1e-12 else Fr(0) for v in y]
        zr = [Fr(v).limit_denominator(denom) for v in z]
        tot = [Fr(0)] * (NP + 1)
        for i, yi in enumerate(yr):
            if yi:
                tot = [a + yi * b for a, b in zip(tot, forms[keys[i]])]
        for j, zj in zip(eq, zr):
            if zj:
                tot = [a + zj * b for a, b in zip(tot, forms[keys[j]])]
        coef = tot[1:]
        if all(x == 0 for i, x in enumerate(coef) if i != P_INDEX - 1) and coef[P_INDEX - 1] == -1:
            support = [(keys[i][0], keys[i][1], str(yi)) for i, yi in enumerate(yr) if yi]
            zsupport = [(keys[j][0], keys[j][1], str(zj)) for j, zj in zip(eq, zr) if zj]
            return tot[0], support, zsupport, denom
    return None


for label, zero in (("baseline", set()), ("with_E3_zeros", e3_keys)):
    res, eq = solve(zero)
    entry = {"status": res.status, "message": res.message, "max_P_float": (-res.fun if res.status == 0 else None)}
    if res.status == 0:
        cert = exact_certificate(res, eq)
        if cert:
            bound, support, zsupport, denom = cert
            entry.update(exact_bound=str(bound), exact_bound_float=float(bound), floor=int(bound // 1),
                         support_size=len(support), e3_multipliers=zsupport, support=support, limit_denominator=denom)
        else:
            entry["exact_certificate"] = "not found by rationalisation"
    report[label] = entry
    print("3. LP %-14s: max P = %s, exact certificate: %s" % (label, entry.get("max_P_float"),
          entry.get("exact_bound", entry.get("exact_certificate"))))
json.dump(report, open(out_path, "w"), indent=1)
