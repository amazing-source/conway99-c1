"""Positive control of the moment identity on a real graph with lambda = 1, mu = 2 (LAB, 18/10/2026).
The Conway constants come from a general derivation for srg(v, k, 1, 2) at a root x (letters = N(x), in k/2 lines;
labels = non-neighbours, each with two letters on two lines; B = letter-label incidence, M = letter matching):
  T = r I - Gamma - (c1 B^T B + c2 B^T M B - c3 J),  with  c1 (k-3) - c2 = r + 1,  -c1 + c2 (k-3) = 1,
  2 c1 + 2 c2 - c3 (k-2) = -2  (so that T B^T = 0);  on ker B, T = r I - Gamma, hence T^2 = (r - s) T.
k = 14 (Conway): r = 3, s = -4, c = (3/8, 1/8, 1/4): T = 3I - Gamma - (3B^TB + B^TMB - 2J)/8 (audit formula).
k = 22 (srg(243,22,1,2), which exists): r = 4, s = -5, c = (4/15, 1/15, 2/15), T^2 = 9T.
This script checks on a genuine srg(243,22,1,2), exactly in integers (15 T):
  T B^T = 0;  T^2 = 9T;  H = T P (P = corner indicators of the 55 rectangles) has H^T H = 9 R with R = P^T T P;
  every entry of H equals base - |N(w) cap Q_f| with base given by the same case analysis (own / one shared root
  line / disjoint) as the Conway encoding of gram_free_moment.py, and the coordinate bounds hold.
usage: python srg243_moment_check.py <edge list of an srg(243,22,1,2)> [root vertex]"""
import sys
from fractions import Fraction
from itertools import combinations

import numpy as np

path = sys.argv[1]
root = int(sys.argv[2]) if len(sys.argv) > 2 else 0
n, k = 243, 22
A = np.zeros((n, n), dtype=np.int64)
for line in open(path):
    a, b = map(int, line.split()[:2])
    A[a, b] = A[b, a] = 1
assert (A.sum(1) == k).all()
A2 = A @ A
assert all(A2[i, j] == (1 if A[i, j] else 2) for i in range(n) for j in range(n) if i != j), "not srg(243,22,1,2)"
letters = [v for v in range(n) if A[root, v]]
labels = [v for v in range(n) if v != root and not A[root, v]]
assert len(letters) == 22 and len(labels) == 220
mate = {a: [b for b in letters if A[a, b]] for a in letters}
assert all(len(m) == 1 for m in mate.values())
lines, seen = [], set()
for a in letters:
    if a not in seen:
        b = mate[a][0]
        lines.append((a, b))
        seen |= {a, b}
line_of = {v: i for i, (a, b) in enumerate(lines) for v in (a, b)}
li = {v: i for i, v in enumerate(letters)}
lb = {v: i for i, v in enumerate(labels)}
B = np.zeros((22, 220), dtype=np.int64)
for w in labels:
    nb = [a for a in letters if A[a, w]]
    assert len(nb) == 2 and line_of[nb[0]] != line_of[nb[1]]
    for a in nb:
        B[li[a], lb[w]] = 1
M = np.zeros((22, 22), dtype=np.int64)
for a in letters:
    M[li[a], li[mate[a][0]]] = 1
G = A[np.ix_(labels, labels)]
J = np.ones((220, 220), dtype=np.int64)
T15 = 60 * np.eye(220, dtype=np.int64) - 15 * G - (4 * B.T @ B + B.T @ M @ B - 2 * J)
print("T B^T = 0:", not (T15 @ B.T).any())
print("T^2 = 9T:", ((T15 @ T15) == 135 * T15).all())
# rectangles: a pair of lines {i, j}; corners = labels with one letter on each
rect = {}
for w in labels:
    nb = sorted(line_of[a] for a in letters if A[a, w])
    rect.setdefault(tuple(nb), []).append(w)
assert len(rect) == 55 and all(len(c) == 4 for c in rect.values())
keys = sorted(rect)
P = np.zeros((220, 55), dtype=np.int64)
for j, q in enumerate(keys):
    for w in rect[q]:
        P[lb[w], j] = 1
H15 = T15 @ P
R15 = P.T @ T15 @ P
print("H^T H = 9R:", ((H15.T @ H15) == 15 * 9 * R15).all())
# the case analysis of h_{w,f} = base - |N(w) cap Q_f|, with 15 * base = 48 (own), -2 (one shared line), 8 (disjoint)
rect_of = {w: q for q, cs in rect.items() for w in cs}
ok, bounds_ok = True, True
own, share, disj = Fraction(0), Fraction(0), Fraction(0)
for w in labels:
    for j, q in enumerate(keys):
        cnt = sum(A[w, u] for u in rect[q])
        rq = rect_of[w]
        base15 = 48 if rq == q else (-2 if set(rq) & set(q) else 8)
        if H15[lb[w], j] != base15 - 15 * cnt:
            ok = False
        lo, hi = ((0, 2) if rq == q else ((0, 2) if set(rq) & set(q) else (0, 4)))
        if not lo <= cnt <= hi:
            bounds_ok = False
print("h = base - |N(w) cap Q_f| on every (label, rectangle):", ok)
print("|N(w) cap Q_f| in [0,2] (own), [0,2] (one shared line), [0,4] (disjoint):", bounds_ok)
print("T_ww = 4 - 6/15 = 54/15 for every label:", (np.diag(T15) == 54).all())
