"""Multiplicities of the integral eigenvalues 0..7 of T_SS (exact: rank of 8T - 8 theta I over F_p, two large primes),
h-invariance and grid flag, over many germs.  Summary of (m0, m1, ..., m7, h-invariant)."""
import sys, json, glob
from collections import Counter
import numpy as np
sys.path.insert(0, ".")
from modp_germ import t8, rank_mod

PR = (2147483629, 2147483587)

def rank_big(M, p):
    A = np.array(M, dtype=np.int64) % p
    n, m = A.shape
    r = 0
    for c in range(m):
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        k = r + nz[0]
        if k != r:
            A[[r, k]] = A[[k, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        col = A[:, c].copy()
        col[r] = 0
        nzr = np.nonzero(col)[0]
        if len(nzr):
            A[nzr] = (A[nzr] - (col[nzr, None] * A[r][None, :]) % p) % p
        r += 1
        if r == n:
            break
    return r

def hperm(labels):
    h = {0: 1, 1: 0, 2: 3, 3: 2}
    idx = {l: i for i, l in enumerate(labels)}
    return [idx[tuple(sorted((h.get(a, a), h.get(b, b))))] for (a, b) in labels]

pats = sys.argv[1:]
files = sorted(set(sum((glob.glob(p) for p in pats), [])))
summ = Counter()
for f in files:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    if not isinstance(d, dict) or "labels" not in d or "edges" not in d or len(d["labels"]) != 44:
        continue
    labels = [tuple(sorted(l)) for l in d["labels"]]
    M8, G = t8(labels, d["edges"])
    ev = np.linalg.eigvalsh(M8 / 8.0)
    if ev.min() < -1e-7:
        continue
    r0 = rank_big(M8.tolist(), PR[0])
    if r0 != 30:
        continue
    mult = []
    for th in range(8):
        M = (M8 - 8 * th * np.eye(44, dtype=np.int64)).tolist()
        r = rank_big(M, PR[0])
        r2 = rank_big(M, PR[1])
        assert r == r2, (f, th, r, r2)
        mult.append(44 - r)
    hp = hperm(labels)
    hinv = all(G[hp[i], hp[j]] == G[i, j] for i in range(44) for j in range(44))
    summ[(tuple(mult), hinv)] += 1
    if not hinv:
        print("NONH", f, flush=True)
for k, v in sorted(summ.items(), key=lambda kv: -kv[1]):
    print("m0..m7 =", k[0], " h-invariant" if k[1] else " NOT h-invariant", ":", v)
