"""C1, lab session, 2026-10-10. Rank-free spectral test of the CANDIDATES of the cell of x_1 in the norm-14 world
(floating point, exploration; nothing here is a certificate).

For a base (39 vertices) and a candidate member u of the cell B1 (neighbours: x_1, y_j, 1 or 2 vertices of B0, three
far vertices), the 40 x 40 principal blocks of
    E_{-4} - f f^t / 14      and      E_3 - g' g'^t / |g'|^2
must be positive semidefinite (see fano_psd.py). With G the 39 x 39 block (PSD, singular), h the new column and d the
new diagonal entry this is: h in the range of G, and d - h^t G^+ h >= 0.
The script counts, for a sample of bases, how many combinatorial candidates of each member pass the two tests, and
then how many PAIRS of candidates of two members do (41 x 41 blocks; adjacency inside the cell is known).

python fano_psd_cell.py <dump of orbits> <number of bases> <step in the dump>
One process, below 1 GB."""
import sys, itertools, time
import numpy as np
LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
def cell(point): return [j for j in range(7) if point not in LINES[j]] + [j for j in range(7) if point in LINES[j] for s in (0, 1)]
B0 = cell(0); B1 = cell(1); FL = [(4, 6), (5, 8), (7, 9)]; forb = set(FL) | {(4, 5), (6, 7), (8, 9)}
quota1 = [1 + (0 in LINES[j]) for j in B1]
triples = list(itertools.combinations(range(15), 3))
f = np.zeros(39); f[:7] = 1; f[7:14] = -1
g = np.zeros(39); g[:14] = 3; g[14:29] = -1; gp = g - 3 / 11; ng = 1470 / 11
I39 = np.eye(39); J39 = np.ones((39, 39)); TOL = 1e-8
D4 = 28 / 63; D3 = 42 / 77 - (3 / 11) ** 2 / ng               # diagonal entries of a boundary vertex (f = 0, g' = -3/11 there)

def base_matrix(E):
    A = np.zeros((39, 39))
    for x in range(7):
        for y in range(7):
            if x not in LINES[y]: A[x, 7 + y] = A[7 + y, x] = 1
    for t, j in enumerate(B0): A[29 + t, 0] = A[0, 29 + t] = 1; A[29 + t, 7 + j] = A[7 + j, 29 + t] = 1
    for a, b in FL: A[29 + a, 29 + b] = A[29 + b, 29 + a] = 1
    for k, (a, b) in enumerate(E): A[14 + k, 29 + a] = A[29 + a, 14 + k] = 1; A[14 + k, 29 + b] = A[29 + b, 14 + k] = 1
    return A

def columns(avec):
    """columns of a boundary vertex with adjacency rows avec (n x 39) in the two deflated blocks"""
    h4 = (1 - 9 * avec) / 63
    h3 = (11 * avec - 2) / 77 + (3 / 11) * gp[None, :] / ng
    return h4, h3

def run(dump, nb, step):
    lines = open(dump).read().split("\n"); t0 = time.time(); done = 0; tot = np.zeros((10, 3)); pairstat = np.zeros(4)
    for li in range(0, len(lines), step):
        if done >= nb or not lines[li]: break
        v = [int(x) for x in lines[li].split()]; E = [(v[1 + 2 * k], v[2 + 2 * k]) for k in range(15)]; done += 1
        A = base_matrix(E); blk0 = [set() for _ in range(10)]
        for k, (a, b) in enumerate(E): blk0[a].add(k); blk0[b].add(k)
        G4 = (27 * I39 - 9 * A + J39) / 63 - np.outer(f, f) / 14; G3 = (11 * A + 44 * I39 - 2 * J39) / 77 - np.outer(gp, gp) / ng
        P4 = np.linalg.pinv(G4, rcond=1e-10, hermitian=True); P3 = np.linalg.pinv(G3, rcond=1e-10, hermitian=True)
        R4 = I39 - G4 @ P4; R3 = I39 - G3 @ P3                # projectors on the kernels
        keep = []
        for m, j in enumerate(B1):
            rows = []
            for Pset in itertools.combinations(range(10), quota1[m]):
                if any(B0[t] == j and j != 0 for t in Pset): continue
                if len(Pset) == 2:
                    a, b = Pset
                    if (a, b) in forb or (blk0[a] & blk0[b]) or B0[a] == B0[b]: continue
                for tri in triples:
                    T = set(tri)
                    if any((B0[t] == j) + len(T & blk0[t]) > (1 if t in Pset else 2) for t in range(10)): continue
                    if any(E[k][0] in Pset and E[k][1] in Pset for k in tri): continue
                    a = np.zeros(39); a[1] = 1; a[7 + j] = 1
                    for t in Pset: a[29 + t] = 1
                    for k in tri: a[14 + k] = 1
                    rows.append(a)
            av = np.array(rows); h4, h3 = columns(av)
            inr = (np.abs(h4 @ R4).max(axis=1) < 1e-7) & (np.abs(h3 @ R3).max(axis=1) < 1e-7)
            s4 = D4 - np.einsum("ij,jk,ik->i", h4, P4, h4); s3 = D3 - np.einsum("ij,jk,ik->i", h3, P3, h3)
            ok = inr & (s4 > -TOL) & (s3 > -TOL)
            tot[m] += (len(av), inr.sum(), ok.sum()); keep.append((av[ok], s4[ok], s3[ok]))
        # pairs: members 0 and 1 (two e-type members, not adjacent), 41 x 41 blocks
        a0, a1 = keep[0][0], keep[1][0]
        if len(a0) and len(a1):
            n0, n1 = min(len(a0), 60), min(len(a1), 60); good = 0; comb = 0
            h40, h30 = columns(a0[:n0]); h41, h31 = columns(a1[:n1])
            for i in range(n0):
                for k in range(n1):
                    if (a0[i][14:] * a1[k][14:]).sum() > 1: continue        # common neighbours in far + B0: at most one
                    comb += 1
                    ok = True
                    for G, P, ha, hb, d, off in ((G4, P4, h40[i], h41[k], D4, 1 / 63), (G3, P3, h30[i], h31[k], D3, -2 / 77 - (3 / 11) ** 2 / ng)):
                        S = np.array([[d - ha @ P @ ha, off - ha @ P @ hb], [off - ha @ P @ hb, d - hb @ P @ hb]])
                        if np.linalg.eigvalsh(S)[0] < -TOL: ok = False; break
                    good += ok
            pairstat += (n0 * n1, comb, good, 1)
    print("bases %d  [%.0f s]" % (done, time.time() - t0))
    print("per member of the cell of x_1 (mean over the bases): combinatorial candidates / in the range (kernel relations hold) / spectrally allowed")
    for m in range(10): print("   member %d (line %d, %d neighbours in B0): %7.0f %7.0f %7.1f" % (m, B1[m], quota1[m], *(tot[m] / done)))
    if pairstat[3]: print("pairs of allowed candidates of members 0 and 1 (first 60 of each): %d examined, %d combinatorially compatible, %d spectrally allowed" % tuple(pairstat[:3]))

if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
