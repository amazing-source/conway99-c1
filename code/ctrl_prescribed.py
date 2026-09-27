"""Positive control for the prescribed-coverage h search (h_exact, rigid mode), C1 27/09.
Takes a known valid h-configuration H* of U (found without y), prescribes w = w(H*) (1 on B1(H*), 3 elsewhere), keeps y = 0,
and truncates the candidate list to M with M mod 8 != 0 (containing H*): the search must find a configuration.
Usage: python ctrl_prescribed.py <envelope.json>"""
import sys, json, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from h_stage2 import setup
from y_first import h_exact
rec = json.load(open(sys.argv[1]))
B, Bf, R, X3, X4c, X4, S = setup(rec['gens'])
HS = np.rint(X4 @ S.T).astype(np.int64); ok = np.abs(HS).max(axis=1) <= 1
H, Hc, HSb = X4[ok], X4c[ok], (HS[ok] != 0)
par = [int(''.join(str(int(b) & 1) for b in row[::-1]), 2) for row in Hc]
z = np.zeros(24)
t0 = time.time()
star = h_exact(z, z, np.zeros(len(S), bool), False, H, Hc, HSb, par, X3, S, t0, 120)
assert star is not None, 'no configuration without y'
w = HSb[star].sum(axis=0)
B1 = w == 1
print('H* =', star, 'w values', sorted(set(w.tolist())), '|B1| =', int(B1.sum()), flush=True)
for M in (max(star) + 1 + k for k in (0, 1, 2, 3, 5, 6, 7)):
    if M % 8 == 0 or M > len(H):
        continue
    t1 = time.time()
    r = h_exact(z, z, B1, True, H[:M], Hc[:M], HSb[:M], par[:M], X3, S, t1, 120)
    good = r is not None and np.array_equal(HSb[r].sum(axis=0), w)
    print('M =', M, '(mod 8 =', M % 8, ') found', r is not None, 'coverage matches', good, round(time.time() - t1, 1), 's', flush=True)
