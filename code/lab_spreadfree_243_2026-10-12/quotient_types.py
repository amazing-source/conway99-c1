"""Lab session, 2026-10-12. QUOTIENT TYPES of a semiregular group of order 27 on a srg(243,22,1,2) (nine orbits).
The 9x9 matrix M = (number of neighbours in orbit j of a vertex of orbit i) is symmetric, has row sums 22 and
eigenvalues 22, 4, -5, so Y = M + 5I - 3J is 9 times a projection: Y^2 = 9Y. Diagonal entries of M are even
(inverse-closed sets in a group of odd order) and at most 6 (a set of projective points with no three collinear and
no point on two secants in a group of order 27 has at most 3 points; used only as the bound m_ii <= 6).
All such integer matrices are listed up to permutation of the orbits (rows kept in non-increasing order of
(diagonal, sorted row); final classes separated by a permutation-invariant key).
python quotient_types.py"""
import itertools, collections, sys

def rows_for(a):
    """multisets of 8 off-diagonal entries x = m - 3 >= -3 with sum -2-a and sum of squares (a+2)(7-a)"""
    S1, S2 = -2 - a, (a + 2) * (7 - a); out = []
    def rec(k, lo, s1, s2, cur):
        if k == 0:
            if s1 == 0 and s2 == 0: out.append(tuple(cur))
            return
        for x in range(lo, 5):
            if x * x > s2: continue
            rec(k - 1, x, s1 - x, s2 - x * x, cur + [x])
    rec(8, -3, S1, S2, [])
    return out

if __name__ == "__main__":
    for a in (0, 2, 4, 6): print("diagonal %d: off-diagonal multisets (entries m_ij): %s" % (a, [tuple(x + 3 for x in r) for r in rows_for(a)]))
    n = 9; sols = []
    Y = [[None] * n for _ in range(n)]
    def ok_partial(i):
        """rows 0..i completely known in columns 0..n-1? check Y^2 = 9Y for the pairs of complete rows"""
        for p in range(i + 1):
            for q in range(p, i + 1):
                if sum(Y[p][k] * Y[q][k] for k in range(n)) != 9 * Y[p][q]: return False
        return True
    def rec(i, diag):
        if i == n:
            M = tuple(tuple(Y[p][q] + 3 - (5 if p == q else 0) for q in range(n)) for p in range(n)); sols.append(M); return
        a = diag[i]; Y[i][i] = a + 2
        known = [Y[i][k] for k in range(i)]                               # symmetric part already fixed
        for r in rows_for(a):
            cnt = collections.Counter(r)
            okk = True
            for x in known:
                if cnt[x] == 0: okk = False; break
                cnt[x] -= 1
            if not okk: continue
            rest = sorted(cnt.elements())
            for perm in set(itertools.permutations(rest)):
                for t, k in enumerate(range(i + 1, n)): Y[i][k] = perm[t]; Y[k][i] = perm[t]
                if ok_partial(i): rec(i + 1, diag)
        for k in range(i + 1, n): Y[i][k] = None; Y[k][i] = None
    types = {}
    for diag in itertools.combinations_with_replacement((6, 4, 2, 0), n):
        del sols[:]; rec(0, diag)
        for M in sols:
            key = tuple(sorted((M[p][p], tuple(sorted(M[p][q] for q in range(n) if q != p))) for p in range(n)))
            key2 = tuple(sorted((M[p][q], M[p][p], M[q][q]) for p in range(n) for q in range(p + 1, n)))
            types.setdefault((key, key2), M)
        print("diagonal %s: %d matrices (labelled, rows in this diagonal order)" % (diag, len(sols)), flush=True) if sols else None
    print("%d types up to the invariant key" % len(types))
    for (key, key2), M in sorted(types.items()):
        ev = "trace %d" % sum(M[p][p] for p in range(n))
        print(" diagonal %s (%s; eigenvalue 4 with multiplicity %d):" % (tuple(M[p][p] for p in range(n)), ev, (sum(M[p][p] for p in range(n)) + 18) // 9))
        for row in M: print("     " + " ".join("%d" % x for x in row))
