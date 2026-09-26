# Hand claim (refined L21): for a line L with ball B (39 pts), Q = A - 3I + 3J mod 7,
#   E_L = {phi in U^perp (layer sums 0) : L_G phi = 0 mod 7}  (dim d(L) - 1),  r(L) = rank_7(M^T restricted to E_L),
#   then rank Q = rank Q_BB + 2 r(L) + rho(L), rho >= 0, and the 3 trivial radical vectors of Q_BB are killed by Q_FB.
# Check on random degenerate balls (d >= 2) with a random far part (2 shadow points per layer, random far adjacency).
import sys, random, numpy as np
sys.path.insert(0, '.')
exec(open('x29e_schur_line_check.py').read().split('rng = random.Random(3)')[0])
def nullspace_mod(Mx, p=7):
    Mx = [[v % p for v in r] for r in Mx]; n, m = len(Mx), len(Mx[0]); r = 0; piv = []
    for c in range(m):
        pr = next((i for i in range(r, n) if Mx[i][c]), None)
        if pr is None: continue
        Mx[r], Mx[pr] = Mx[pr], Mx[r]; inv = pow(Mx[r][c], p - 2, p); Mx[r] = [(v * inv) % p for v in Mx[r]]
        for i in range(n):
            if i != r and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [(a - f * b) % p for a, b in zip(Mx[i], Mx[r])]
        piv.append(c); r += 1
    free = [c for c in range(m) if c not in piv]; basis = []
    for fc in free:
        v = [0] * m; v[fc] = 1
        for i, pc in enumerate(piv): v[pc] = (-Mx[i][fc]) % p
        basis.append(v)
    return basis
rng = random.Random(5)
labs = list(range(12)); mate = {i: i ^ 1 for i in labs}
def rand_tau():
    while True:
        perm = labs[:]; rng.shuffle(perm); t = {}; ok = True
        for i in range(0, 12, 2):
            a, b = perm[i], perm[i + 1]
            if mate[a] == b: ok = False; break
            t[a], t[b] = b, a
        if ok: return t
found = 0; tries = 0
while found < 10 and tries < 20000:
    tries += 1
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
    AG = B[3:, 3:]
    LG = (3 * np.eye(36, dtype=int) - AG) % 7
    # E_L: L_G phi = 0 and layer sums 0
    rows = LG.tolist() + [[1 if 12 * p <= j < 12 * p + 12 else 0 for j in range(36)] for p in range(3)]
    E = nullspace_mod(rows)
    d = 1 + len(E)
    if d < 2: continue
    nF = 60; N = np.zeros((36, nF), dtype=int)
    for w in range(nF):
        for base in (0, 12, 24):
            for v in rng.sample(range(12), 2): N[base + v, w] = 1
    AF = np.zeros((nF, nF), dtype=int)
    for i in range(nF):
        for j in range(i + 1, nF):
            if rng.random() < 0.13: AF[i, j] = AF[j, i] = 1
    n = 99; A = np.zeros((n, n), dtype=int); A[:39, :39] = B; A[3:39, 39:] = N; A[39:, 3:39] = N.T; A[39:, 39:] = AF
    Q = (A - 3 * np.eye(n, dtype=int) + 3) % 7
    rQ, rB = rank_mod(Q.tolist()), rank_mod(Q[:39, :39].tolist())
    # trivial radical: two quotient vectors and h = 1_L - 1_N
    g1 = np.array([3, -3, 0] + [1] * 12 + [-1] * 12 + [0] * 12); g2 = np.array([0, 3, -3] + [0] * 12 + [1] * 12 + [-1] * 12)
    h = np.array([1] * 3 + [-1] * 36)
    triv_ok = all(((Q[39:, :39] @ w) % 7 == 0).all() and ((Q[:39, :39] @ w) % 7 == 0).all() for w in (g1, g2, h))
    Emat = np.array(E).T                      # 36 x (d-1)
    r = rank_mod(((N.T @ Emat) % 7).tolist())  # rank of M^T on E_L
    comps = None
    print(f'd(L)={d}  rank Q_BB={rB} (=37-d: {rB == 37 - d})  r(L)={r}  rank Q={rQ}  rho={rQ - rB - 2 * r} (>=0)  trivial radical killed by Q_FB: {triv_ok}')
    found += 1
print('tries', tries)
