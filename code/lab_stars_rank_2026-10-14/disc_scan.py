"""Fast DISC scan of saved four-star structures (15/10/2026).

For each json (labels, edges): M8 = 8T_S (integral, PSD for the structures we keep).  Symmetric elimination with
diagonal pivots (enough for a PSD matrix: a zero diagonal entry of a PSD Schur complement has a zero row) gives the
rank r and d = det(M8_I) for the pivot set I (|I| = r).  If r = 30 the label set spans V and, in a Conway graph,
d = disc(Lambda_8T) [Lambda_8T : Lambda_I]^2 = 2^69 7^(30-k) x square with k even (L17, LAB re-derivation of det K,
Codex L2), i.e. d = 2 x (perfect square).  Equivalently det(A_H - 3I) = 4 * 7^(30-k) * square for the star complement
H = N[v] u I.  Robust part (no Codex lemma): every prime other than 2 and 7 has an even exponent in d.
usage: python disc_scan.py <json> [<json> ...]
"""
import json
import math
import sys
from fractions import Fraction as Fr

import numpy as np

from stars_rank import kval


def sym_pivot_det(M):
    A = [[Fr(x) for x in row] for row in M]
    n = len(A)
    alive = list(range(n))
    det, piv = Fr(1), []
    while True:
        p = next((i for i in alive if A[i][i] != 0), None)
        if p is None:
            # PSD check: remaining block must be zero
            if any(A[i][j] != 0 for i in alive for j in alive):
                return None, None, None
            break
        d = A[p][p]
        if d < 0:
            return None, None, None
        det *= d
        piv.append(p)
        alive.remove(p)
        rowp = A[p]
        for i in alive:
            if rowp[i] != 0:
                f = rowp[i] / d
                Ai = A[i]
                for j in alive:
                    if rowp[j] != 0:
                        Ai[j] -= f * rowp[j]
    return len(piv), det, piv


def small_odd_primes(d, bound=20000):
    """exponent parities of d for primes < bound; returns (odd-exponent primes, cofactor)."""
    odd = []
    p = 2
    while p < bound and d > 1:
        e = 0
        while d % p == 0:
            d //= p
            e += 1
        if e % 2:
            odd.append(p)
        p += 1 if p == 2 else 2
    return odd, d


def main():
    for f in sys.argv[1:]:
        dj = json.load(open(f))
        S = [frozenset(l) for l in dj["labels"]]
        n = len(S)
        G = np.zeros((n, n), dtype=np.int64)
        for i, j in dj["edges"]:
            G[i, j] = G[j, i] = 1
        K8 = np.rint(8 * np.array([[kval(a, b) for b in S] for a in S])).astype(np.int64)
        M8 = (24 * np.eye(n, dtype=np.int64) - 8 * G - K8).tolist()
        r, det, piv = sym_pivot_det(M8)
        if r is None:
            print("%s: not PSD (exact)" % f, flush=True)
            continue
        d = int(det)
        assert det == d
        odd, cof = small_odd_primes(d)
        cof_sq = math.isqrt(cof) ** 2 == cof
        # Conway target: d = 2 x square  <=>  odd == [2] and cofactor a perfect square
        ok = odd == [2] and cof_sq
        robust = all(p in (2, 7) for p in odd) and cof_sq
        cofs = "1" if cof == 1 else ("square" if cof_sq else "non-square (%d digits)" % len(str(cof)))
        if r == 30:
            verdict = "DISC OK" if ok else ("fails only at 2/7 (Codex lemmas)" if robust else "DISC FAILS (robust)")
        else:
            verdict = "n/a (rank != 30)"
        print("%s: rank %d, det(8T_I) odd-exponent primes %s, cofactor %s -> %s" % (f, r, odd, cofs, verdict), flush=True)


if __name__ == "__main__":
    main()
