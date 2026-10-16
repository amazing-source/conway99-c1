"""Batch DISC scan: for every json with labels+edges, exact rank of 8T_S and square class of det(8T_I) (pivot set I).
Summary by (rank, PSD, odd-exponent primes of det, cofactor square?).  Conway at rank 30 needs class 2 or 14
(robust: primes other than 2, 7 to even powers; 2 to an odd power)."""
import sys, json, math, glob, os
from collections import Counter
import numpy as np
sys.path.insert(0, os.getcwd())
from disc_scan import sym_pivot_det, small_odd_primes
from stars_rank import kval

def scan(f):
    try:
        dj = json.load(open(f))
    except Exception:
        return None
    if not isinstance(dj, dict) or "labels" not in dj or "edges" not in dj:
        return None
    S = [frozenset(l) for l in dj["labels"]]
    n = len(S)
    if n != 44:
        return None
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in dj["edges"]:
        G[i, j] = G[j, i] = 1
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    M8 = (24 * np.eye(n, dtype=np.int64) - 8 * G - K8).tolist()
    r, det, piv = sym_pivot_det(M8)
    if r is None:
        return ("notPSD_T",)
    d = int(det)
    odd, cof = small_odd_primes(d)
    cof_sq = math.isqrt(cof) ** 2 == cof
    return (r, tuple(odd), "sq" if cof_sq else "NONSQ")

pats = sys.argv[1:]
files = sorted(set(sum((glob.glob(p) for p in pats), [])))
summ = Counter(); alive = []
for f in files:
    res = scan(f)
    if res is None:
        continue
    summ[res] += 1
    if len(res) == 3 and res[0] == 30:
        odd = set(res[1])
        if res[2] == "sq" and odd <= {2, 7} and 2 in odd:
            alive.append(f)
for k, v in sorted(summ.items(), key=lambda kv: str(kv[0])):
    print(k, v)
print("DISC-alive rank-30 germs:", len(alive))
for f in alive[:30]:
    print("  ", f)
