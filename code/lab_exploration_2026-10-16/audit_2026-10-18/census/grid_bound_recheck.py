"""Exact re-check of Codex's new certificate 3P + 4G <= 2772 on the INDEPENDENT census census2 (LAB, 18/10/2026).
Codex (c4_prism_grid_bound.json): 12 order-9 counts with weights >= 0, plus (4/3)(G - 77), sum to 2464/3 - P.
Equivalently sum_H w_H N_H = 924 - P - (4/3) G identically, where G = N(K3 x K3), so 3P + 4G <= 2772 in every
srg(99,14,1,2), with no assumption on c.
usage: py -3 -I grid_bound_recheck.py <census2 json> <c4_prism_grid_bound.json> <census2.py directory>"""
import json
import sys
from fractions import Fraction as Fr
from itertools import combinations

census_path, cert_path, c2dir = sys.argv[1:4]
sys.path.insert(0, c2dir)
import census2 as C2                                    # noqa: E402

data = json.load(open(census_path))
NP = len(data["params"])
forms = {}
for n, lst in data["types"].items():
    for key, rows, aut, form in lst:
        v = [Fr(0)] * (NP + 1)
        for p, val in form.items():
            v[int(p)] = Fr(val) / aut
        forms[(int(n), key)] = v
pairs9 = list(combinations(range(9), 2))


def rows_from_code(code):
    rows = [0] * 9
    for k, (i, j) in enumerate(pairs9):
        if code >> k & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    return rows


grid = [0] * 9                                           # K3 x K3 on (r, c), vertex 3r + c
for a in range(9):
    for b in range(9):
        if a != b and (a // 3 == b // 3 or a % 3 == b % 3):
            grid[a] |= 1 << b
gkey, _ = C2.canon(9, grid)
gpar = [i + 1 for i, (n, key, rows) in enumerate(data["params"]) if n == 9 and key == gkey]
assert len(gpar) == 1, "the grid must be an order-9 parameter (minimum degree 4)"
G = gpar[0]
assert forms[(9, gkey)][G] == 1 and sum(1 for x in forms[(9, gkey)] if x) == 1
cert = json.load(open(cert_path))
total = [Fr(0)] * (NP + 1)
for item in cert["certificate"]:
    w = Fr(item["weight"])
    assert w >= 0
    if item["row"] == "grid_lower_bound":
        continue                                         # (4/3)(G - 77) is moved to the right-hand side below
    code = int(item["row"].split("_")[-1])
    key, _ = C2.canon(9, rows_from_code(code))
    assert (9, key) in forms, item
    total = [a + w * b for a, b in zip(total, forms[(9, key)])]
names = ["1"] + ["N%d_%d" % (n, key) for n, key, rows in data["params"]]
got = {names[i]: str(x) for i, x in enumerate(total) if x}
want = {"1": "924", names[1]: "-1", names[G]: "-4/3"}
print("sum_H w_H N_H on census2 =", got)
print("identity sum = 924 - P - (4/3) G :", got == want, "| grid parameter:", names[G])
