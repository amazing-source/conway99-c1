"""C1, lab session, 2026-10-10. Rank-free spectral test of the bases of the norm-14 world (floating point, exploration).

In a srg(99,14,1,2) the projectors E_{-4} = (27 I - 9 A + J)/63 and E_3 = (11 A + 44 I - 2 J)/77 are positive
semidefinite, so every principal submatrix is. With a norm-14 eigenvector f = 1_X - 1_Y one knows two more vectors:
f in the (-4)-eigenspace and g' = g - (3/11) 1 in the 3-eigenspace, g = 3.1_core - 1_far (A g = 3 g + 3.1). Hence on
any vertex set U
    E_{-4}[U] - f_U f_U^t / 14 >= 0      and      E_3[U] - g'_U g'_U^t / |g'|^2 >= 0,   |g'|^2 = 1470/11.
The test is applied to the 39-vertex base (core, far, the ten boundary neighbours of x_0) of every orbit.

python fano_psd.py <dump of fano37 (FANO37_ORBIT=1 FANO37_DUMP=file FANO37_RANKONLY=1 ./fano37 all 1 0)>
One process, below 1 GB, about a minute."""
import sys, time
import numpy as np
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
def cell(point): return [j for j in range(7) if point not in LINES[j]] + [j for j in range(7) if point in LINES[j] for s in (0, 1)]
B0 = cell(0); FL = [(4, 6), (5, 8), (7, 9)]
A0 = np.zeros((39, 39))
for x in range(7):
    for y in range(7):
        if x not in LINES[y]: A0[x, 7 + y] = A0[7 + y, x] = 1
for t, j in enumerate(B0): A0[29 + t, 0] = A0[0, 29 + t] = 1; A0[29 + t, 7 + j] = A0[7 + j, 29 + t] = 1
for a, b in FL: A0[29 + a, 29 + b] = A0[29 + b, 29 + a] = 1
f = np.zeros(39); f[:7] = 1; f[7:14] = -1
g = np.zeros(39); g[:14] = 3; g[14:29] = -1; gp = g - 3 / 11; ng = 1470 / 11
I = np.eye(39); J = np.ones((39, 39))
t0 = time.time(); n = 0; tot = 0; hist = {}; mins4 = []; mins3 = []; passed = []
for line in open(sys.argv[1]):
    v = [int(x) for x in line.split()]; size = v[0]; E = [(v[1 + 2 * k], v[2 + 2 * k]) for k in range(15)]
    A = A0.copy()
    for k, (a, b) in enumerate(E): A[14 + k, 29 + a] = A[29 + a, 14 + k] = 1; A[14 + k, 29 + b] = A[29 + b, 14 + k] = 1
    M4 = (27 * I - 9 * A + J) / 63 - np.outer(f, f) / 14
    M3 = (11 * A + 44 * I - 2 * J) / 77 - np.outer(gp, gp) / ng
    e4 = np.linalg.eigvalsh(M4)[0]; e3 = np.linalg.eigvalsh(M3)[0]
    ok4 = e4 > -1e-9; ok3 = e3 > -1e-9; key = (bool(ok4), bool(ok3)); hist[key] = hist.get(key, (0, 0)); hist[key] = (hist[key][0] + 1, hist[key][1] + size)
    mins4.append(e4); mins3.append(e3); n += 1; tot += size
    if ok4 and ok3: passed.append(line.strip())
print("orbits %d (labelled bases %d)  [%.0f s]" % (n, tot, time.time() - t0))
for key in sorted(hist): print("   E_-4 test %s, E_3 test %s: %d orbits (%d labelled)" % ("passes" if key[0] else "FAILS", "passes" if key[1] else "FAILS", hist[key][0], hist[key][1]))
m4 = np.array(mins4); m3 = np.array(mins3)
print("least eigenvalue of the deflated E_-4 block: min %.4f, median %.4f, max %.4f" % (m4.min(), np.median(m4), m4.max()))
print("least eigenvalue of the deflated E_3 block:  min %.4f, median %.4f, max %.4f" % (m3.min(), np.median(m3), m3.max()))
print("smallest |least eigenvalue| among those counted as passing: %.2e, %.2e" % (min([abs(x) for x in m4 if x > -1e-9] + [9]), min([abs(x) for x in m3 if x > -1e-9] + [9])))
if len(sys.argv) > 2: open(sys.argv[2], "w").write("\n".join(passed) + "\n")
