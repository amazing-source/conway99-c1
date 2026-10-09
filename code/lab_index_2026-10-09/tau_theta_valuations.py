"""C1, lab session, 2026-10-09. Random line balls (cubic near graph G on 36 points: 3 layers of 12, mates, three
transversal matchings; no triangle; K >= 0; connected): exact number of spanning trees tau(G) and
Theta(G) = product of (4 + theta) over the 35 eigenvalues theta != 3 of G = det(4I + G) / 7.
Question: which powers of 2 and 3 divide them?  (Fraction-free Bareiss determinants, exact integers.)
One process, a few MB, seconds."""
import random, sys, collections
from fractions import Fraction

def bareiss(M):
    n = len(M); M = [r[:] for r in M]; sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            p = next((i for i in range(k + 1, n) if M[i][k] != 0), None)
            if p is None: return 0
            M[k], M[p] = M[p], M[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]

def ball(rng, allow4=True, allow3=False):
    A = [[0] * 36 for _ in range(36)]
    for i in range(36): A[i][i ^ 1] = 1
    for l in range(3):
        p = list(range(12)); rng.shuffle(p)
        for i in range(12):
            x, y = 12 * l + i, 12 * ((l + 1) % 3) + p[i]; A[x][y] = A[y][x] = 1
    adj = [set(j for j in range(36) if A[i][j]) for i in range(36)]
    tri = 0
    for i in range(36):
        for j in range(i + 1, 36):
            c = len(adj[i] & adj[j]); same = i // 12 == j // 12
            if A[i][j] and c:
                if not allow3 or c > 1 or same: return None
                tri += 1
            if 2 - A[i][j] - c - same < 0: return None
    four = any((y ^ 1) in adj[x ^ 1] for x in range(0, 36, 2) for y in adj[x] if y != x ^ 1)
    if four and not allow4: return None
    seen = {0}; st = [0]
    while st:
        v = st.pop()
        for w in adj[v]:
            if w not in seen: seen.add(w); st.append(w)
    if len(seen) != 36: return None
    return A, tri // 3, four

def val(n, p):
    v = 0
    while n % p == 0: n //= p; v += 1
    return v

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1])); NB = int(sys.argv[2]); allow3 = len(sys.argv) > 3
    v3 = collections.Counter(); v2 = collections.Counter(); v2t = collections.Counter(); n = 0
    while n < NB:
        b = ball(rng, True, allow3)
        if b is None: continue
        A, tri, four = b; n += 1
        H = [[(3 if i == j else 0) - A[i][j] for j in range(36)] for i in range(36)]
        tau = bareiss([r[1:] for r in H[1:]])
        D4 = bareiss([[(4 if i == j else 0) + A[i][j] for j in range(36)] for i in range(36)])
        assert tau > 0 and D4 % 7 == 0
        th = D4 // 7
        v3[val(tau, 3)] += 1; v2[val(th, 2)] += 1; v2t[val(tau, 2)] += 1
        if n <= 5: print("tau =", tau, " Theta =", th, " triangles", tri)
    print("balls:", n, "(triangles allowed)" if allow3 else "(no triangle)")
    print("3-adic valuation of tau:", dict(sorted(v3.items())))
    print("2-adic valuation of tau:", dict(sorted(v2t.items())))
    print("2-adic valuation of Theta:", dict(sorted(v2.items())))
