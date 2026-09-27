r"""Diagnostic (C1 27/09): for one (y1,y2) pair of a rigid envelope, where does the prescribed-coverage h search die?
Reports: number of h-candidates orthogonal to y1, y2; per B1 item the number of candidates covering it; the maximum depth reached,
and at the deepest nodes which constraint fails (coverage, cells, orthogonality).
Usage: python diag_depth.py <envelope.json> <gpairs.json> <k>"""
import json, os, sys, time
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from h_stage2 import setup

rec = json.load(open(sys.argv[1]))
pairs = json.load(open(sys.argv[2]))['pairs']
k = int(sys.argv[3])
B, Bf, R, X3, X4c, X4, S = setup(rec['gens'])
HS = np.rint(X4 @ S.T).astype(np.int64)
ok = np.abs(HS).max(axis=1) <= 1
H, Hc, COV = X4[ok], X4c[ok], (HS[ok] != 0)
y1 = np.array([float(F(x)) for x in pairs[k][0]]); y2 = np.array([float(F(x)) for x in pairs[k][1]])
yh1 = np.abs(np.abs(S @ y1) - 1.5) < 1e-6; yh2 = np.abs(np.abs(S @ y2) - 1.5) < 1e-6
B1 = yh1 | yh2
idx = np.nonzero((np.abs(H @ y1) < 1e-9) & (np.abs(H @ y2) < 1e-9))[0]
Hh, C = H[idx], COV[idx]
print('items', len(S), '|B1|', int(B1.sum()), 'hits y1', int(yh1.sum()), 'hits y2', int(yh2.sum()), 'h cands perp y', len(idx))
# a candidate may cover at most... in B1 each item exactly once overall; per candidate: how many B1 / B3 items
nb1 = C[:, B1].sum(axis=1); nb3 = C[:, ~B1].sum(axis=1)
print('per candidate: B1 items covered', dict(zip(*np.unique(nb1, return_counts=True))), ' B3 items', dict(zip(*np.unique(nb3, return_counts=True))))
# required: 7 h cover |B1| once and |B3| three times: sum nb1 = |B1|, sum nb3 = 3 |B3|
print('need sum over 7 h: B1', int(B1.sum()), 'B3', 3 * int((~B1).sum()), '-> average per h', B1.sum() / 7, 3 * (~B1).sum() / 7)
# which (nb1, nb3) combos can sum to the targets with 7 terms?
combos = {}
for a, b in zip(nb1, nb3):
    combos[(int(a), int(b))] = combos.get((int(a), int(b)), 0) + 1
print('candidate profiles (B1, B3):', sorted(combos.items()))
X3p = X3[(np.abs(X3 @ y1) < 1e-9) & (np.abs(X3 @ y2) < 1e-9)]
print('norm-3 vectors orthogonal to y1, y2:', len(X3p))
