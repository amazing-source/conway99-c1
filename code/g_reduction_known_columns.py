# First move of the "reverse" step: are the fully known columns enough to constrain anything?
# In x-coordinates the rows of ANY vertex are known on the columns B1(x) = {x} u N(x) (15 columns):
# a vertex of Gamma_2(x) = pair {c,d} is adjacent exactly to c and d there.  If the ball rows already have
# rank 15 on these columns, the relation "outer rows in span of ball rows", restricted there, is empty.
import numpy as np
p = 7
def rank_mod(M, p=7):
    M = np.array(M, dtype=np.int64) % p
    r, (n, m) = 0, M.shape
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i, c]), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        for i in range(n):
            if i != r and M[i, c]: M[i] = (M[i] - M[i, c] * M[r]) % p
        r += 1
    return r
# B1(x): index 0 = x, labels 1..14 with mates (2i-1, 2i)
n = 15
A = np.zeros((n, n), dtype=np.int64)
for i in range(1, 15): A[0, i] = A[i, 0] = 1
for c in range(7): A[1 + 2*c, 2 + 2*c] = A[2 + 2*c, 1 + 2*c] = 1
Q = A - 3*np.eye(n, dtype=np.int64) + 3
print("rank_7 of Q on B1(x) x B1(x) (windmill):", rank_mod(Q))
# every vertex of Gamma_2(x) restricted to columns B1(x): 3 + [adjacent] on its two labels
pairs = [(a, b) for a in range(1, 15) for b in range(a + 1, 15) if (a + 1) // 2 != (b + 1) // 2]
assert len(pairs) == 84
R = np.full((84, 15), 3, dtype=np.int64)
for r, (a, b) in enumerate(pairs): R[r, a] += 1; R[r, b] += 1
print("rank_7 of all 99 rows on the 15 known columns:", rank_mod(np.vstack([Q, R])))
