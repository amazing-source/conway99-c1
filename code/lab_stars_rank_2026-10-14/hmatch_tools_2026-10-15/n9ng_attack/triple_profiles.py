"""Kernel profiles on Y supported on the m-blocks of 3 outer lines (exact): are they line-constant?
usage: python triple_profiles.py <json> [side: m or l]"""
import json, sys, itertools
from fractions import Fraction as F
sys.path.insert(0, '.'); sys.path.insert(0, 'hmatch_tools_2026-10-15/n9ng_attack')
from stars_rank import kval
from exact_lin import rref, nullspace
f = sys.argv[1]; side = sys.argv[2] if len(sys.argv) > 2 else "m"
a, b = (2, 3) if side == "m" else (0, 1)
d = json.load(open(f)); S = [frozenset(l) for l in d["labels"]]; n = 44; idx = {s: i for i, s in enumerate(S)}
E = set()
for p, q in d["edges"]: E.add((p, q)); E.add((q, p))
T = [[(3 if i == j else 0) - (1 if (i, j) in E else 0) - F(int(round(8 * kval(S[i], S[j]))), 8) for j in range(n)] for i in range(n)]
Kb = nullspace(T)
LINES = [(4, 5), (6, 7), (8, 9), (10, 11), (12, 13)]
Ylab = [frozenset((s, y)) for ln in LINES for s in (a, b) for y in ln]   # per line: a y, a y', b y, b y'
Ylab = []
for ln in LINES:
    for s in (a, b):
        for y in ln: Ylab.append(frozenset((s, y)))
P = [[v[idx[s]] for s in Ylab] for v in Kb]
Rp, _ = rref(P)
print(f, "side", side, "dim P =", len(Rp))
for A in itertools.combinations(range(5), 3):
    off = [k for k in range(20) if k // 4 not in A]
    # profiles in span(Rp) vanishing on 'off' coordinates: solve c^T Rp[:, off] = 0
    M = [[Rp[i][k] for i in range(len(Rp))] for k in off]
    cs = nullspace(M) if M else [[F(int(i == j)) for i in range(len(Rp))] for j in range(len(Rp))]
    profs = [[sum(c[i] * Rp[i][k] for i in range(len(Rp))) for k in range(20)] for c in cs]
    profs, _ = rref(profs) if profs else ([], [])
    lc = all(all(pr[4 * L] == pr[4 * L + 1] == pr[4 * L + 2] == pr[4 * L + 3] for L in A) for pr in profs)
    msym = all(all(pr[4 * L] == pr[4 * L + 2] and pr[4 * L + 1] == pr[4 * L + 3] for L in A) for pr in profs)
    print("  lines %s: rel %d, all line-constant %s, all m-symmetric %s" % (A, len(profs), lc, msym))
    if not lc:
        for pr in profs:
            print("     ", " | ".join(" ".join(str(pr[4 * L + t]) for t in range(4)) for L in A))
