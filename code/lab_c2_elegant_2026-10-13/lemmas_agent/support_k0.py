# Microscope, not a proof step.
# Support structures of a sigma-odd integer (-4)-eigenfunction with entries 0,+-1, m orbits in the support,
# in the sub-case k = 0 (no inner orbit), e = 0 (P independent).  Then the "orbit graph" B on m vertices
# (i ~ j iff p_i ~ sigma p_j) is 4-regular with all codegrees <= 2 (report, Lemma 3 and section B.6).
#
# What the script does, for a given m:
#   1. enumerates the labelled 4-regular graphs on m vertices with all codegrees <= 2, with the neighbours of
#      vertex 0 fixed to {1,2,3,4} and the row of vertex 1 fixed up to the relabellings that preserve this;
#   2. reduces them to isomorphism classes (exact canonical form, individualisation-refinement);
#   3. for each class applies
#        (PSD)     3I + B and 4I - B positive semidefinite (exact, integer Gauss elimination);
#        (DESCENT) the lattice L = Z a + sum_i Z H e_i (i in the support) has no vector of norm 1..F,
#                  F = min(m-1, 10)  (Lemma 4 of the report: norm(k a - H c) = k^2 m - 14 k sum(c) + 7 c^t (3I+B) c).
# Limits: one process, pure Python + numpy, < 2 GB, intended < 5 minutes per value of m.
#
# usage: python support_k0.py m
import sys, time, itertools
from fractions import Fraction
import numpy as np

def enumerate_graphs(n):
    """labelled 4-regular graphs, codegree <= 2, N(0) = {1,2,3,4}, row 1 normalised."""
    out = []
    adj = [0] * n
    deg = [0] * n
    cod = [[0] * n for _ in range(n)]

    def add(i, j):
        # returns False (and leaves state unchanged) if a codegree would exceed 2
        ni = [w for w in range(n) if adj[i] >> w & 1]
        nj = [w for w in range(n) if adj[j] >> w & 1]
        for w in ni:
            if cod[j][w] >= 2:
                return False
        for w in nj:
            if cod[i][w] >= 2:
                return False
        for w in ni:
            cod[j][w] += 1; cod[w][j] += 1
        for w in nj:
            cod[i][w] += 1; cod[w][i] += 1
        adj[i] |= 1 << j; adj[j] |= 1 << i
        deg[i] += 1; deg[j] += 1
        return True

    def rem(i, j):
        adj[i] &= ~(1 << j); adj[j] &= ~(1 << i)
        deg[i] -= 1; deg[j] -= 1
        ni = [w for w in range(n) if adj[i] >> w & 1]
        nj = [w for w in range(n) if adj[j] >> w & 1]
        for w in ni:
            cod[j][w] -= 1; cod[w][j] -= 1
        for w in nj:
            cod[i][w] -= 1; cod[w][i] -= 1

    for j in (1, 2, 3, 4):
        assert add(0, j)

    def fill(i):
        # complete the neighbourhood of vertex i using vertices > i, then go to i+1
        if i == n:
            out.append(tuple(adj))
            return
        need = 4 - deg[i]
        if need < 0:
            return
        cands = [j for j in range(i + 1, n) if deg[j] < 4 and not (adj[i] >> j & 1)]
        if len(cands) < need:
            return
        if i == 1:
            # normalisation: t neighbours among {2,3,4} -> take the first t; the others the first of 5,6,...
            choices = []
            for t in (0, 1, 2):
                c = tuple(range(2, 2 + t)) + tuple(range(5, 5 + 3 - t))
                if all(x < n for x in c):
                    choices.append(c)
        else:
            choices = itertools.combinations(cands, need)
        for c in choices:
            done = []
            ok = True
            for j in c:
                if add(i, j):
                    done.append(j)
                else:
                    ok = False
                    break
            if ok:
                # remaining vertices must still be completable: quick degree count
                fill(i + 1)
            for j in reversed(done):
                rem(i, j)

    fill(1)
    return out

def refine(adj, n, col):
    while True:
        sig = []
        for v in range(n):
            s = sorted(col[w] for w in range(n) if adj[v] >> w & 1)
            sig.append((col[v], tuple(s)))
        keys = sorted(set(sig))
        idx = {k: i for i, k in enumerate(keys)}
        new = [idx[s] for s in sig]
        if new == col:
            return col
        col = new

def canon(adj, n):
    best = [None]

    def rec(col):
        col = refine(adj, n, col)
        cells = {}
        for v, c in enumerate(col):
            cells.setdefault(c, []).append(v)
        target = None
        for c in sorted(cells):
            if len(cells[c]) > 1:
                target = c
                break
        if target is None:
            order = sorted(range(n), key=lambda v: col[v])
            pos = {v: i for i, v in enumerate(order)}
            cert = []
            for v in order:
                row = 0
                for w in range(n):
                    if adj[v] >> w & 1:
                        row |= 1 << pos[w]
                cert.append(row)
            cert = tuple(cert)
            if best[0] is None or cert < best[0]:
                best[0] = cert
            return
        for v in cells[target]:
            # individualise v: give it a new smallest colour inside its cell
            col2 = [2 * c + 1 for c in col]
            col2[v] -= 1
            rec(col2)

    rec([0] * n)
    return best[0]

def is_psd_int(M):
    """exact test of positive semidefiniteness of a symmetric integer matrix (fractions)."""
    n = len(M)
    A = [[Fraction(int(x)) for x in row] for row in M]
    for i in range(n):
        if A[i][i] < 0:
            return False
        if A[i][i] == 0:
            if any(A[i][j] != 0 for j in range(n)):
                return False
            continue
        for r in range(i + 1, n):
            if A[r][i] != 0:
                f = A[r][i] / A[i][i]
                for c in range(i, n):
                    A[r][c] -= f * A[i][c]
                for c in range(i, n):
                    A[c][r] = A[r][c]
        # zero out the processed row/column for later pivots
        for r in range(i + 1, n):
            A[i][r] = Fraction(0); A[r][i] = Fraction(0)
    return True

def short_vectors(G, bound):
    """all nonzero integer vectors x (up to sign) with x^t G x <= bound, G positive definite (float FP,
    norms recomputed exactly in integers)."""
    n = G.shape[0]
    L = np.linalg.cholesky(G.astype(float))
    R = L.T                                   # G = R^t R, R upper triangular
    res = []
    x = [0] * n

    def rec(i, partial):
        # partial = sum_{l>i} (sum_{j>=l} R[l][j] x_j)^2
        if i < 0:
            if any(x):
                xv = np.array(x, dtype=object)
                nrm = int(sum(int(x[a]) * int(G[a, b]) * int(x[b]) for a in range(n) for b in range(n)))
                if 0 < nrm <= bound:
                    res.append((nrm, tuple(x)))
            return
        s = sum(R[i, j] * x[j] for j in range(i + 1, n))
        rem = bound + 1e-6 - partial
        if rem < 0:
            return
        rad = (rem ** 0.5) / R[i, i]
        lo = int(np.ceil(-s / R[i, i] - rad))
        hi = int(np.floor(-s / R[i, i] + rad))
        for xi in range(lo, hi + 1):
            x[i] = xi
            t = R[i, i] * xi + s
            rec(i - 1, partial + t * t)
        x[i] = 0

    rec(n - 1, 0.0)
    # keep one of +-x
    seen = set(); out = []
    for nrm, v in res:
        mv = tuple(-a for a in v)
        if mv in seen:
            continue
        seen.add(v); out.append((nrm, v))
    return out

def descent_test(B, m, F):
    """lattice generated by a and H e_i, i = 0..m-2 (H e_{m-1} = 7a - sum of the others).
    Gram: (a,a) = m, (a,He_i) = 7, (He_i,He_j) = 7(3 delta_ij + B_ij).  Returns the vectors of norm 1..F."""
    n = m
    G = np.zeros((n, n), dtype=np.int64)
    G[0, 0] = m
    for i in range(m - 1):
        G[0, i + 1] = G[i + 1, 0] = 7
        for j in range(m - 1):
            G[i + 1, j + 1] = 7 * ((3 if i == j else 0) + B[i][j])
    return short_vectors(G, F)

def main():
    m = int(sys.argv[1])
    t0 = time.time()
    labelled = enumerate_graphs(m)
    t1 = time.time()
    classes = {}
    for adj in labelled:
        c = canon(list(adj), m)
        classes.setdefault(c, 0)
        classes[c] += 1
    t2 = time.time()
    print(f"m = {m}: labelled graphs with the normalisation: {len(labelled)}  ({t1 - t0:.1f} s)")
    print(f"isomorphism classes (4-regular, all codegrees <= 2): {len(classes)}  ({t2 - t1:.1f} s)")
    F = min(m - 1, 10)
    n_psd = 0; n_desc = 0
    survivors = []
    for c in sorted(classes):
        B = [[(c[i] >> j) & 1 for j in range(m)] for i in range(m)]
        M3 = [[(3 if i == j else 0) + B[i][j] for j in range(m)] for i in range(m)]
        M4 = [[(4 if i == j else 0) - B[i][j] for j in range(m)] for i in range(m)]
        if not (is_psd_int(M3) and is_psd_int(M4)):
            continue
        n_psd += 1
        # the lattice needs a positive definite Gram: 3I + B may be singular (eigenvalue -3 of B); then the
        # generators are dependent; we then test on the float side with a tiny ridge and exact recomputation
        ev = np.linalg.eigvalsh(np.array(B, dtype=float))
        if ev[0] < -3 + 1e-9:
            # singular case: some integer c with (3I+B)c = 0, no information lost for the report; flag it
            sv = "SINGULAR"
            survivors.append((c, ev, sv))
            n_desc += 1
            continue
        sv = descent_test(B, m, F)
        if not sv:
            n_desc += 1
            survivors.append((c, ev, None))
    print(f"classes with 3I+B and 4I-B positive semidefinite (exact): {n_psd}")
    print(f"classes that also pass the descent test (no vector of norm 1..{F} in Z a + sum Z He_i): {n_desc}")
    for c, ev, sv in survivors:
        edges = [f"{i}-{j}" for i in range(m) for j in range(i + 1, m) if (c[i] >> j) & 1]
        print("  survivor:", " ".join(edges))
        print("     spectrum:", " ".join(f"{x:.4f}" for x in ev), "" if sv is None else sv)
    print(f"total time {time.time() - t0:.1f} s")

if __name__ == "__main__":
    main()
