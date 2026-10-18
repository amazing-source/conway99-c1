"""Order-10 prism LP with the E3 zeros (LAB, 18/10/2026; exploration, floating point).
Reads the census2 order-10 JSON entry by entry (low memory), keeps every type count >= 0 (orders 2..10; the order-10
entries are embedding counts, aut = null, which has the same sign), and imposes N_H = 0 for the E3 type of order 9 and
for every order-10 type that contains it (exactly its one-vertex extensions).  Rows are scaled by their largest
coefficient.  Maximises P, without and with the E3 zeros.
usage: py -3 -I p852_order10_e3.py <census2 order-10 json> <census2.py directory> <E3 key of order 9> <out.json>"""
import json
import sys
from array import array
from itertools import combinations

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

path, c2dir, e3key, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
sys.path.insert(0, c2dir)
import census2 as C2                                    # noqa: E402

text = open(path).read()
dec = json.JSONDecoder()
i = text.index('"params"')
i = text.index("[", i)
params, i = dec.raw_decode(text, i)
NP = len(params)
assert params[0][0] == 6
rows_i, rows_j, rows_v, consts, keys = array('i'), array('i'), array('d'), array('d'), []
e3_rows = {}
t = text.index('"types"')
pos = text.index("{", t) + 1
while True:
    while text[pos] in " ,\n\r\t":
        pos += 1
    if text[pos] == "}":
        break
    order, pos = dec.raw_decode(text, pos)
    pos = text.index("[", pos) + 1
    order = int(order)
    while True:
        while text[pos] in " ,\n\r\t":
            pos += 1
        if text[pos] == "]":
            pos += 1
            break
        entry, pos = dec.raw_decode(text, pos)
        key, rows, aut, form = entry
        vals = {int(p): float(v) for p, v in form.items()}
        scale = max(abs(x) for x in vals.values()) if vals else 0.0
        if scale == 0.0:
            vals, scale = {}, 1.0
        r = len(keys)
        keys.append((order, key))
        consts.append(vals.get(0, 0.0) / scale)
        for p, v in vals.items():
            if p:
                rows_i.append(r)
                rows_j.append(p - 1)
                rows_v.append(v / scale)
        if order == 9 and key == e3key:
            e3_rows[9] = rows
del text
A = csr_matrix((np.frombuffer(rows_v, dtype=np.float64), (np.frombuffer(rows_i, dtype=np.int32), np.frombuffer(rows_j, dtype=np.int32))), shape=(len(keys), NP))
b = np.frombuffer(consts, dtype=np.float64).copy()
assert 9 in e3_rows, "E3 key not found at order 9"

# one-vertex extensions of the E3 type = all order-10 types containing it as an induced subgraph
base = e3_rows[9]
ext = set()
for mask in range(1 << 9):
    rows = list(base) + [mask]
    rows = [r | ((mask >> v & 1) << 9) if v < 9 else r for v, r in enumerate(rows)]
    ok = True
    for x, y in combinations(range(10), 2):
        cmn = bin(rows[x] & rows[y]).count("1")
        if (rows[x] >> y & 1 and cmn > 1) or (not rows[x] >> y & 1 and cmn > 2):
            ok = False
            break
    if ok:
        ext.add(C2.canon(10, rows)[0])
index = {k: n for n, k in enumerate(keys)}
zero = [index[(9, e3key)]] + [index[(10, k)] for k in sorted(ext) if (10, k) in index]
missing = [k for k in ext if (10, k) not in index]
assert not missing, ("E3 extension not in the census", missing[:3])
c = np.zeros(NP)
c[0] = -1.0
result = {"types": len(keys), "parameters": NP, "E3_order10_extensions": len(ext)}
for label, eq in (("baseline", []), ("with_E3_zeros", zero)):
    kw = dict(A_eq=A[eq], b_eq=-b[eq]) if eq else {}
    res = linprog(c, A_ub=-A, b_ub=b, bounds=[(None, None)] * NP, method="highs", **kw)
    result[label] = {"status": int(res.status), "message": res.message, "max_P": (-res.fun if res.status == 0 else None)}
    print(label, result[label], flush=True)
json.dump(result, open(out, "w"), indent=1)
