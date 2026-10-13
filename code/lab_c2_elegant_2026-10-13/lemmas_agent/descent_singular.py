# Microscope, not a proof step.  Completes support_k0_v2.py for the classes where 3I + B is singular (eigenvalue -3
# of B): there the generators a, He_i are linearly dependent, and the short-vector search needs a true basis.
# Method: exact rational elimination on the Gram matrix of the generators -> a maximal independent subset and the
# rational coordinates of the others -> Hermite normal form -> a basis of the lattice -> Fincke-Pohst.
# It is run on EVERY survivor file line (singular or not), so it is also a second implementation of the descent test.
#
# usage: python descent_singular.py m      (reads support_k0_m{m}_survivors.txt)
import sys
from fractions import Fraction
from math import gcd
import numpy as np

def lattice_basis_gram(G):
    """G: PSD integer Gram matrix (list of lists) of generators.  Returns (Gram of a Z-basis, the basis as integer
    combinations of the generators is not needed)."""
    n = len(G)
    # choose a maximal independent subset greedily (exact)
    idx = []
    def indep(sub):
        M = [[Fraction(G[i][j]) for j in sub] for i in sub]
        k = len(sub)
        for c in range(k):
            pr = next((r for r in range(c, k) if M[r][c] != 0), None)
            if pr is None:
                return False
            M[c], M[pr] = M[pr], M[c]
            for r in range(c + 1, k):
                if M[r][c] != 0:
                    f = M[r][c] / M[c][c]
                    M[r] = [x - f * y for x, y in zip(M[r], M[c])]
        return True
    for i in range(n):
        if indep(idx + [i]):
            idx.append(i)
    r = len(idx)
    # coordinates of every generator in the basis g_idx: solve G[idx][idx] q = G[idx][j]
    A = [[Fraction(G[i][j]) for j in idx] for i in idx]
    def solve(rhs):
        M = [row[:] + [Fraction(b)] for row, b in zip(A, rhs)]
        for c in range(r):
            pr = next(rr for rr in range(c, r) if M[rr][c] != 0)
            M[c], M[pr] = M[pr], M[c]
            inv = 1 / M[c][c]
            M[c] = [x * inv for x in M[c]]
            for rr in range(r):
                if rr != c and M[rr][c] != 0:
                    f = M[rr][c]
                    M[rr] = [x - f * y for x, y in zip(M[rr], M[c])]
        return [M[i][r] for i in range(r)]
    coords = []
    for j in range(n):
        q = solve([G[i][j] for i in idx])
        # check that generator j really equals this combination (norm of the difference is 0)
        diff = Fraction(G[j][j]) - 2 * sum(q[a] * G[idx[a]][j] for a in range(r)) \
            + sum(q[a] * q[b] * G[idx[a]][idx[b]] for a in range(r) for b in range(r))
        assert diff == 0
        coords.append(q)
    D = 1
    for q in coords:
        for x in q:
            D = D * x.denominator // gcd(D, x.denominator)
    rows = [[int(x * D) for x in q] for q in coords]
    # Hermite normal form by integer row operations
    basis = []
    rows = [row for row in rows if any(row)]
    col = 0
    while rows and col < r:
        rows.sort(key=lambda row: (row[col] == 0, abs(row[col])))
        if rows[0][col] == 0:
            col += 1
            continue
        changed = True
        while changed:
            changed = False
            rows.sort(key=lambda row: (row[col] == 0, abs(row[col])))
            piv = rows[0]
            for t in range(1, len(rows)):
                if rows[t][col] != 0:
                    f = rows[t][col] // piv[col]
                    rows[t] = [x - f * y for x, y in zip(rows[t], piv)]
                    if rows[t][col] != 0:
                        changed = True
        rows.sort(key=lambda row: (row[col] == 0, abs(row[col])))
        basis.append(rows[0])
        rows = [row for row in rows[1:] if any(row)]
        col += 1
    assert len(basis) == r and not rows
    Gb = [[Fraction(sum(basis[a][i] * basis[b][j] * G[idx[i]][idx[j]] for i in range(r) for j in range(r)), D * D)
           for b in range(r)] for a in range(r)]
    for row in Gb:
        for x in row:
            assert x.denominator == 1
    return [[int(x) for x in row] for row in Gb]

def short_vectors(G, bound):
    n = len(G)
    Gf = np.array(G, dtype=float)
    R = np.linalg.cholesky(Gf).T
    res = set()
    x = [0] * n
    def rec(i, partial):
        if i < 0:
            if any(x):
                nrm = sum(x[a] * G[a][b] * x[b] for a in range(n) for b in range(n))
                if 0 < nrm <= bound:
                    res.add(nrm)
            return
        s = sum(R[i, j] * x[j] for j in range(i + 1, n))
        rem = bound + 1e-6 - partial
        if rem < 0:
            return
        rad = (rem ** 0.5) / R[i, i]
        lo = int(np.ceil(-s / R[i, i] - rad)); hi = int(np.floor(-s / R[i, i] + rad))
        for xi in range(lo, hi + 1):
            x[i] = xi
            t = R[i, i] * xi + s
            rec(i - 1, partial + t * t)
        x[i] = 0
    rec(n - 1, 0.0)
    return sorted(res)

def main():
    m = int(sys.argv[1])
    F = min(m - 1, 10)
    tot = 0; killed = 0; sing = 0; sing_killed = 0
    for line in open(f"support_k0_m{m}_survivors.txt"):
        note = "SINGULAR" in line
        edges = line.split("#")[0].split()
        B = [[0] * m for _ in range(m)]
        for e in edges:
            i, j = map(int, e.split("-"))
            B[i][j] = B[j][i] = 1
        # generators a, He_0..He_{m-1}
        G = [[0] * (m + 1) for _ in range(m + 1)]
        G[0][0] = m
        for i in range(m):
            G[0][i + 1] = G[i + 1][0] = 7
            for j in range(m):
                G[i + 1][j + 1] = 7 * ((3 if i == j else 0) + B[i][j])
        Gb = lattice_basis_gram(G)
        sv = short_vectors(Gb, F)
        tot += 1
        sing += note
        if sv:
            killed += 1
            sing_killed += note
            print("killed (norms", sv, "):", " ".join(edges), "[rank %d]" % len(Gb))
    print(f"m = {m}: {tot} classes read, {sing} with 3I+B singular; killed by the descent test now: {killed}"
          f" (of which singular: {sing_killed}); remaining: {tot - killed}")

if __name__ == "__main__":
    main()
