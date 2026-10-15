"""p-adic elementary divisors of M = 8 T_S4 for saved four-star structures (LAB 15/10/2026, SQ30 mechanism hunt).

Elimination over Z/p^K (K = 40) with a pivot of minimal p-adic valuation at each step; the valuations of the pivots are
the p-adic valuations of the non-zero invariant factors of M (those < K are exact; a remaining block = 0 mod p^K is the
kernel, nullity counted by rank over Q given separately).  The discriminant group of R = M Z^44 (form x^T M y) is the
torsion of coker M, so v_p(disc) = sum of the finite valuations.  Prints, per structure, the multiset of non-zero
valuations at p = 2, 3, 5, 7.
usage: python padic_snf.py <bundle json (list of structures) or structure json> [...]"""
import json
import sys

import numpy as np

from stars_rank import kval

K = 40


def padic_vals(M, p):
    mod = p ** K
    A = [[x % mod for x in row] for row in M]
    n = len(A)
    vals = []
    rows = list(range(n))
    cols = list(range(n))
    while rows:
        best = None
        for i in rows:
            for j in cols:
                a = A[i][j]
                if a:
                    v = 0
                    while a % p == 0:
                        a //= p
                        v += 1
                    if best is None or v < best[0]:
                        best = (v, i, j)
                        if v == 0:
                            break
            if best is not None and best[0] == 0:
                break
        if best is None:
            break
        v, i, j = best
        vals.append(v)
        piv = A[i][j]
        u = piv // p ** v
        uinv = pow(u, -1, mod)
        for r in rows:
            if r == i or A[r][j] == 0:
                continue
            f = (A[r][j] // p ** v) * uinv % mod
            Ar, Ai = A[r], A[i]
            for c in cols:
                if Ai[c]:
                    Ar[c] = (Ar[c] - f * Ai[c]) % mod
        rows.remove(i)
        cols.remove(j)
        # column elimination is implicit: the pivot row is dropped, the remaining block is the Schur complement mod p^K
        for r in rows:
            A[r][j] = 0
    return sorted(vals)


def load(f):
    d = json.load(open(f))
    if isinstance(d, dict) and "structures" in d:
        for s in d["structures"]:
            s.setdefault("labels", d["labels"])
        return d["structures"]
    if isinstance(d, list):
        return d
    return [d]


def m8(d):
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    G = np.zeros((n, n), dtype=np.int64)
    for i, j in d["edges"]:
        G[i, j] = G[j, i] = 1
    K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
    return (24 * np.eye(n, dtype=np.int64) - 8 * G - K8).tolist()


def main():
    tally = {}
    for f in sys.argv[1:]:
        for k, d in enumerate(load(f)):
            M = m8(d)
            prof = []
            for p in (2, 3, 5, 7):
                v = [x for x in padic_vals(M, p) if x > 0]
                prof.append("%d:%s" % (p, ",".join(map(str, v)) or "-"))
            key = " ".join(prof[1:])
            tally[key] = tally.get(key, 0) + 1
            print("%s[%d] c=%s | %s" % (f, k, d.get("c"), " | ".join(prof)), flush=True)
    print("TALLY of (3,5,7) profiles:")
    for key, c in sorted(tally.items(), key=lambda t: -t[1]):
        print("  %5d  %s" % (c, key))


if __name__ == "__main__":
    main()
