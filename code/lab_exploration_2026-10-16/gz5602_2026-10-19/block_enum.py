"""Exhaustive principal-block test for one root template (LAB 19/10/2026), first target gz 5602.

Facts (proved; see NUIT_2026-10-19.md and the audit of 18/10):
  (a) R = P^T H : the row F of R is the sum of the rows h_w of the four labels w of the rectangle F (four-sum);
  (b) h_w^T R^+ h_w <= T_ww = 5/2 and h_w in im R  (T = 7 P_U, (P_U)_ww = 5/14 for every label);
  (c) for a principal block S = R_II and p = (h_w)_I : p in im S and p^T S^+ p <= h_w^T R^+ h_w (Schur), so
      [[2S, 2p], [2p^T, 5]] >= 0 for every label w;
  (d) every row h_w is in the exact catalogue of its rectangle (cat5602.py: zero sums at every root, boxes).
For a coordinate set I (non-grid rectangles), every realisation gives S = R_II whose row F (F in I) is a four-sum of
catalogue rows of F projected on I.  The script enumerates ALL such symmetric S >= 0, then tests each:
  S is FORBIDDEN if for some F in I no four rows of F with admissible projections (c) sum to S_F.
A forbidden verdict uses a permissive float test (tolerance in favour of admitting a row), so it is sound; every
S declared forbidden is then re-checked in exact integer arithmetic (principal minors) before being counted.
usage: python block_enum.py <cat.json> <coords, e.g. 04,16,25,35> [--limit N]"""
import json
import sys
import time
from fractions import Fraction
from itertools import combinations, combinations_with_replacement

import numpy as np

cat = json.load(open(sys.argv[1]))
E = cat["edges"]
I = sys.argv[2].split(",")
ix = [E.index(c) for c in I]
rows = {F: [tuple(r[i] for i in ix) for r in cat["rows"][F]] for F in I}
proj = {F: sorted(set(rows[F])) for F in I}
t0 = time.time()


def sums4(A):
    """all four-fold sums (with repetition) of vectors of A, as a dict sum -> one witness"""
    A = list(A)
    two = {}
    for a, b in combinations_with_replacement(range(len(A)), 2):
        s = tuple(x + y for x, y in zip(A[a], A[b]))
        two.setdefault(s, (A[a], A[b]))
    four = {}
    keys = list(two)
    for i in range(len(keys)):
        for j in range(i, len(keys)):
            s = tuple(x + y for x, y in zip(keys[i], keys[j]))
            if s not in four:
                four[s] = two[keys[i]] + two[keys[j]]
    return four


S4 = {F: sums4(proj[F]) for F in I}
print("coords", I, "distinct projections", {F: len(proj[F]) for F in I}, "four-sums", {F: len(S4[F]) for F in I},
      "%.1fs" % (time.time() - t0), flush=True)
k = len(I)
# candidate S: choose s_F in S4[F] for each F, consistent with symmetry; F-th coordinate of s_F is R_FF
cands = []
# index the four-sums of the i-th coordinate by their first i entries (fixed by symmetry once rows 0..i-1 are chosen)
index = []
for i, F in enumerate(I):
    d = {}
    for s in S4[F]:
        if s[i] in (2, 4, 6, 8):
            d.setdefault(s[:i], []).append(s)
    index.append(d)


def rec(i, chosen):
    if i == k:
        cands.append(tuple(chosen))
        return
    key = tuple(chosen[j][i] for j in range(i))
    for s in index[i].get(key, []):
        chosen.append(s)
        M = np.array([c[:i + 1] for c in chosen], dtype=float)      # leading (i+1) x (i+1) block, must be PSD
        if np.linalg.eigvalsh(M).min() >= -1e-9:
            rec(i + 1, chosen)
        chosen.pop()


rec(0, [])
print("symmetric PSD candidate blocks S:", len(cands), "%.1fs" % (time.time() - t0), flush=True)


def admissible_float(S, p):
    w, V = np.linalg.eigh(S)
    pos = w > 1e-9
    c = V.T @ np.array(p, dtype=float)
    if np.any(np.abs(c[~pos]) > 1e-6):
        return False                      # p not in im S (the residual of an integer vector would be much larger)
    return float(np.sum(c[pos] ** 2 / w[pos])) <= 2.5 + 1e-7


def det(M):
    M = [[Fraction(x) for x in r] for r in M]
    n = len(M); d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if M[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            M[c], M[p] = M[p], M[c]; d = -d
        d *= M[c][c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for j in range(c, n):
                M[r][j] -= f * M[c][j]
    return d


def admissible_exact(S, p):
    M = [[2 * S[i][j] for j in range(k)] + [2 * p[i]] for i in range(k)] + [[2 * x for x in p] + [5]]
    n = k + 1
    return all(det([[M[i][j] for j in sub] for i in sub]) >= 0 for r in range(1, n + 1) for sub in combinations(range(n), r))


def in4(A, s):
    """is s a sum of four (not necessarily distinct) vectors of A ?  meet in the middle on pair sums"""
    two = {tuple(x + y for x, y in zip(a, b)) for a, b in combinations_with_replacement(A, 2)}
    return any(tuple(u - v for u, v in zip(s, x)) in two for x in two)


forbidden, alive = [], []
P = {F: np.array(proj[F], dtype=float) for F in I}
for S in cands:
    Sm = np.array(S, dtype=float)
    w, V = np.linalg.eigh(Sm)
    pos = w > 1e-9
    dead_at = None
    for i, F in enumerate(I):
        C = P[F] @ V                                   # coordinates of every projection in the eigenbasis of S
        ok = (np.abs(C[:, ~pos]) <= 1e-6).all(axis=1) & ((C[:, pos] ** 2 / w[pos]).sum(axis=1) <= 2.5 + 1e-7)
        A = [proj[F][j] for j in np.nonzero(ok)[0]]
        if not in4(A, S[i]):
            dead_at = F
            break
    if dead_at is None:
        alive.append(S)
        continue
    # exact re-check of the forbidden verdict: recompute the admissible set exactly (it can only shrink)
    F = dead_at; i = I.index(F)
    A = [p for p in proj[F] if admissible_exact(S, p)]
    assert not in4(A, S[i])
    forbidden.append((S, F))
print("forbidden", len(forbidden), "alive", len(alive), "%.1fs" % (time.time() - t0))
json.dump({"coords": I, "candidates": len(cands), "forbidden": [[list(map(list, S)), F] for S, F in forbidden],
           "alive": [list(map(list, S)) for S in alive]},
          open("block_enum_%s.json" % "_".join(I), "w"))
