# Hand claim: for a ball with d(L) = 1, rank_7(A_B - 3I) = 37 (the quotient's -4 part is a Jordan block mod 7,
# not extra kernel), rank_7 Q_BB = 36, and ker_7 Q_BB = <quotient 3-eigenvectors (2-dim), 1_T - 1_{N(L)}>.
import sys, random, numpy as np
sys.path.insert(0, '.')
src = open('x29e_schur_line_check.py').read().split('rng = random.Random(3)')[0]
exec(src)
rng = random.Random(11)
labs = list(range(12)); mate = {i: i ^ 1 for i in labs}
def rand_tau():
    while True:
        perm = labs[:]; rng.shuffle(perm); t = {}; ok = True
        for i in range(0, 12, 2):
            a, b = perm[i], perm[i + 1]
            if mate[a] == b: ok = False; break
            t[a], t[b] = b, a
        if ok: return t
done = 0
while done < 8:
    tu, tub = rand_tau(), rand_tau(); sig = labs[:]
    while True:
        rng.shuffle(sig)
        if all(sig[v] != v for v in labs): break
    B = np.zeros((39, 39), dtype=int); X = lambda v: 3 + v; Y = lambda v: 15 + v; Z = lambda v: 27 + v
    for a, b in ((0, 1), (0, 2), (1, 2)): B[a, b] = B[b, a] = 1
    for v in labs:
        B[0, X(v)] = B[X(v), 0] = 1; B[1, Y(v)] = B[Y(v), 1] = 1; B[2, Z(v)] = B[Z(v), 2] = 1
        B[X(v), X(mate[v])] = 1; B[Y(v), Y(tu[v])] = 1; B[Z(v), Z(tub[v])] = 1
        B[X(v), Y(v)] = B[Y(v), X(v)] = 1; B[X(v), Z(v)] = B[Z(v), X(v)] = 1
        B[Y(v), Z(sig[v])] = B[Z(sig[v]), Y(v)] = 1
    LG = (3 * np.eye(36, dtype=int) - B[3:, 3:]) % 7
    d = 36 - rank_mod(LG.tolist())
    if d != 1: continue
    AB3 = (B - 3 * np.eye(39, dtype=int)) % 7
    QBB = (B - 3 * np.eye(39, dtype=int) + 3) % 7
    h = np.array([1] * 3 + [-1] * 36)
    g1 = np.array([3, -3, 0] + [1] * 12 + [-1] * 12 + [0] * 12)   # b = (1,-1,0), a = 3b
    g2 = np.array([0, 3, -3] + [0] * 12 + [1] * 12 + [-1] * 12)
    ok = all(((QBB @ w) % 7 == 0).all() for w in (h, g1, g2))
    print(f'd(L)=1: rank7(A_B-3I) = {rank_mod(AB3.tolist())}, rank7 Q_BB = {rank_mod(QBB.tolist())}, '
          f'h = 1_T - 1_N and the two quotient vectors in ker Q_BB: {ok}')
    done += 1
