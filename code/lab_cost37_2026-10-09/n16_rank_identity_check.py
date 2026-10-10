"""C1, lab session, 2026-10-10. Control of the algebra used by n16_cell_test.py / n16cell.c:
for random sets S of candidate columns of a typed world of norm 16 and random adjacencies inside S,
    rank_7( Seidel matrix of base + S )  =  33 + rank_7( R ),      R[a][b] = t_ab - <v_a, v_b>,
where the left side is computed directly on the (35 + |S|) x (35 + |S|) matrix. The script also checks that every
column of the domains satisfies the two true relations (the dependent base vertices agree).

python n16_rank_identity_check.py <typed world json> <number of random sets> <seed>"""
import sys, json, random
from n16_cell_test import rank_mod7, independent_rows, inverse, P7
D = json.load(open(sys.argv[1])); trials = int(sys.argv[2]); rng = random.Random(int(sys.argv[3]))
A = D["base_adjacency"]; n = len(A)
K = [[0 if i == j else (6 if A[i][j] else 1) for j in range(n)] for i in range(n)]
I = independent_rows(K); assert len(I) == 33
Kinv = inverse([[K[i][j] for j in I] for i in I])
masks = [m for d in D["domains"] for m in d["neighbour_masks"]]
bad_rel = 0
def comp(m):
    s = [6 if (m >> j) & 1 else 1 for j in range(n)]; sI = [s[i] for i in I]
    c = [sum(Kinv[a][b] * sI[b] for b in range(33)) % P7 for a in range(33)]
    return s, sI, c
for m in masks:
    s, sI, c = comp(m)
    if any(sum(K[x][I[a]] * c[a] for a in range(33)) % P7 != s[x] for x in range(n)): bad_rel += 1
print("columns in the domains: %d; columns contradicting the two relations: %d" % (len(masks), bad_rel))
mismatch = 0; hist = {}
for _ in range(trials):
    k = rng.randint(1, 8); S = [rng.choice(masks) for _ in range(k)]
    T = [[0] * k for _ in range(k)]
    for a in range(k):
        for b in range(a + 1, k): T[a][b] = T[b][a] = rng.choice((6, 1))
    cs = [comp(m) for m in S]
    R = [[(T[a][b] - sum(x * y for x, y in zip(cs[a][1], cs[b][2]))) % P7 for b in range(k)] for a in range(k)]
    big = [row[:] + [cs[b][0][i] for b in range(k)] for i, row in enumerate(K)] + [cs[a][0] + T[a] for a in range(k)]
    r1 = rank_mod7(big); r2 = 33 + rank_mod7(R); hist[(k, r2 - 33)] = hist.get((k, r2 - 33), 0) + 1
    if r1 != r2: mismatch += 1
print("random sets %d: mismatches between the direct rank and 33 + rank(R): %d" % (trials, mismatch))
print("(size of S, rank of R): count ->", sorted(hist.items()))
