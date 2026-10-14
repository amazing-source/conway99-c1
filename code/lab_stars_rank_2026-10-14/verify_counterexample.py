"""Independent exact verifier for star structures: candidate counterexamples to (A) (three stars) or to H4 / H4'
(four stars 0,1,2,3), 14/10/2026.

Statement (A): every admissible three-star structure (stars 0, 1 mates, and 2; letters 0..13, mate of x = x xor 1)
with T >= 0, U >= 0 and c(l) = 1 has rank T = 31.  A counterexample needs, exactly:
  (adm) admissibility, re-checked here from scratch: (C1) exact counts towards the three stars, (C1') partial counts
        towards the other letters, (C2) caps on common neighbours inside S plus shared letters;
  (c1)  c(l) = 1, i.e. rank T_X = 22 on X = L_0 u L_1;
  (r30) rank T = 30 on the 34 labels (nullity 4: the three stars and one more);
  (psd) T >= 0 and U = 7 Pi_S - T >= 0, certified exactly: a principal submatrix of size rank is positive definite
        (exact LDL^T pivots > 0) and has the same rank as the whole matrix.
Everything is computed with Fractions from the label names and the edge list only (K re-derived from its formula,
Pi from D), without importing the search code.
usage: python verify_counterexample.py <json> <path to record: key[:index], or 'edges' for a top-level edge list>
       [stars, default 0,1,2]   e.g.  symz_606_found.json found:3      h4_4_PSD_1.json edges 0,1,2,3
"""
import itertools
import json
import sys
from fractions import Fraction as Fr

MATE = lambda x: x ^ 1


def kval(a, b):
    inter = len(a & b)
    m = sum(1 for x in a for y in b if y == MATE(x))
    return Fr(-1, 4) + Fr(3, 8) * inter + Fr(1, 8) * m


def rank_and_basis(M):
    """Exact rank, pivot columns, and a basis of the kernel (Fractions)."""
    A = [[Fr(x) for x in row] for row in M]
    n, m = len(A), len(A[0])
    piv, r = [], 0
    for c in range(m):
        p = next((i for i in range(r, n) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [x / pv for x in A[r]]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(m) if c not in piv]
    ker = []
    for f in free:
        v = [Fr(0)] * m
        v[f] = Fr(1)
        for i, c in enumerate(piv):
            v[c] = -A[i][f]
        ker.append(v)
    return r, piv, ker


def ldl_positive(M, idx):
    """Exact symmetric elimination on the principal submatrix idx; True iff all pivots are > 0 (positive definite)."""
    A = [[Fr(M[i][j]) for j in idx] for i in idx]
    n = len(A)
    for k in range(n):
        if A[k][k] <= 0:
            return False, k, A[k][k]
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            if f != 0:
                for j in range(k, n):
                    A[i][j] -= f * A[k][j]
    return True, n, None


def psd_certificate(M, name):
    r, piv, ker = rank_and_basis(M)
    # for a symmetric matrix the pivot columns of the row reduction give a nonsingular principal submatrix only if
    # the matrix is PSD-like; search greedily for a principal submatrix of size r with full rank
    idx = []
    for i in range(len(M)):
        trial = idx + [i]
        if rank_and_basis([[M[a][b] for b in trial] for a in trial])[0] == len(trial):
            idx = trial
        if len(idx) == r:
            break
    ok, k, bad = ldl_positive(M, idx)
    print("  %s: exact rank %d, principal submatrix of size %d positive definite: %s%s"
          % (name, r, len(idx), ok, "" if ok else " (pivot %d = %s)" % (k, bad)))
    return ok and len(idx) == r, r, ker


def main():
    path, rec = sys.argv[1], sys.argv[2]
    d = json.load(open(path))
    key, _, k = rec.partition(":")
    item = d if key == "edges" else (d[key][int(k)] if k else d[key])
    stars = tuple(int(t) for t in (sys.argv[3] if len(sys.argv) > 3 else "0,1,2").split(","))
    S = [frozenset(l) for l in d["labels"]]
    n = len(S)
    assert len(set(S)) == n
    assert all(len(l) == 2 and MATE(min(l)) != max(l) for l in S)
    assert set(S) == {frozenset((a, x)) for a in stars for x in range(14) if x not in (a, MATE(a))}
    adj = [[0] * n for _ in range(n)]
    for i, j in item["edges"]:
        assert i != j
        adj[i][j] = adj[j][i] = 1

    def need(l, y):
        return 1 if (y in l or MATE(y) in l) else 2

    # (C1) exact counts towards the stars, (C1') at most the count towards the other letters
    for i, l in enumerate(S):
        for y in range(14):
            cnt = sum(adj[i][j] for j in range(n) if y in S[j])
            if y in stars:
                assert cnt == need(l, y), ("C1", sorted(l), y, cnt)
            else:
                assert cnt <= need(l, y), ("C1'", sorted(l), y, cnt)
    # (C2) caps: common neighbours inside S plus shared letters <= lambda (adjacent) or mu (non-adjacent)
    for i, j in itertools.combinations(range(n), 2):
        common = sum(1 for t in range(n) if adj[i][t] and adj[j][t]) + len(S[i] & S[j])
        assert common <= (1 if adj[i][j] else 2), ("C2", sorted(S[i]), sorted(S[j]), common)
    print("admissibility (C1, C1', C2): OK")
    T = [[(3 if i == j else 0) - adj[i][j] - kval(S[i], S[j]) for j in range(n)] for i in range(n)]
    # star relations
    for y in stars:
        z = [1 if y in l else 0 for l in S]
        assert all(sum(T[i][j] * z[j] for j in range(n)) == 0 for i in range(n)), ("star", y)
    print("the three star vectors are in ker T: OK")
    X = [i for i in range(n) if 0 in S[i] or 1 in S[i]]
    rX = rank_and_basis([[T[i][j] for j in X] for i in X])[0]
    print("rank T_X = %d  ->  c(l) = %d" % (rX, 23 - rX))
    if 3 in stars:
        Xm = [i for i in range(n) if 2 in S[i] or 3 in S[i]]
        rXm = rank_and_basis([[T[i][j] for j in Xm] for i in Xm])[0]
        print("rank T_Xm = %d  ->  c(m) = %d" % (rXm, 23 - rXm))
    # Pi_S from D: Pi = I - D^T (D D^T)^-1 D on the 84 labels, restricted to S
    LAB = [frozenset((a, b)) for a, b in itertools.combinations(range(14), 2) if b != MATE(a)]
    DDt = [[Fr(12 if x == y else (0 if y == MATE(x) else 1)) for y in range(14)] for x in range(14)]
    # invert DDt exactly
    A = [row[:] + [Fr(1 if i == j else 0) for j in range(14)] for i, row in enumerate(DDt)]
    for c in range(14):
        p = next(i for i in range(c, 14) if A[i][c] != 0)
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(14):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    Inv = [row[14:] for row in A]

    def Pi(a, b):
        s = sum(Inv[x][y] for x in a for y in b)
        return (1 if a == b else 0) - s
    U = [[7 * Pi(S[i], S[j]) - T[i][j] for j in range(n)] for i in range(n)]
    okT, rT, kerT = psd_certificate(T, "T")
    okU, rU, kerU = psd_certificate(U, "U")
    print("nullity of T = %d (stars give %d)" % (n - rT, len(stars)))
    # exhibit the extra relation: a kernel vector outside the span of the stars
    Smat = [[Fr(1 if y in l else 0) for l in S] for y in stars]
    rs = rank_and_basis(Smat + kerT)[0]
    print("rank of span(stars, ker T) = %d" % rs)
    if len(stars) == 3:
        verdict = okT and okU and rT == 30 and rX == 22 and rs == 4
        print("VERDICT: %s" % ("COUNTEREXAMPLE TO (A) (admissible, c(l) = 1, rank 30, T >= 0, U >= 0)" if verdict
                               else "not a counterexample to (A)"))
    else:
        print("VERDICT: %s" % ("ADMISSIBLE FOUR-STAR STRUCTURE WITH T >= 0 AND U >= 0 (H4 is false); rank T = %d"
                               % rT if (okT and okU) else "T or U is not PSD"))


if __name__ == "__main__":
    main()
