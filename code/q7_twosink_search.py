"""Two full-pivot sib blocks c, d (notes/131 sec. 6): search Sigma (10x10, entries 0/+-1, exactly two +1 and two -1 in
every row and column) minimising rank_7(M_D(Sigma)) + rank_7(M_C(Sigma^T)), where
M_D = I - J + 2P_pi + Rm^T (5I + 4P_pi) Rm,  Rm = Sigma + 2(I - P_pi)  (mod 7).
Necessary for the configuration: both ranks <= 2.  Simulated annealing with count-preserving switches."""
import random, sys, math
import numpy as np
P = 7
n = 10
Ppi = np.zeros((n, n), int)
for i in range(n):
    Ppi[i, i ^ 1] = 1
I = np.eye(n, dtype=int)
J = np.ones((n, n), int)
A0 = (I - J + 2 * Ppi) % P
W = (5 * I + 4 * Ppi) % P
D2 = 2 * (I - Ppi)


def rank_mod(M):
    M = [[int(x) % P for x in r] for r in M]
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, n) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [x * inv % P for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        r += 1
    return r


def cost(S):
    RmD = S + D2
    RmC = S.T + D2
    MDm = (A0 + RmD.T @ W @ RmD) % P
    MCm = (A0 + RmC.T @ W @ RmC) % P
    return rank_mod(MDm) + rank_mod(MCm)


def init(rng):
    while True:
        perms, used = [], set()
        ok = True
        for _ in range(4):
            for _t in range(500):
                p = list(range(n))
                rng.shuffle(p)
                if all((i, p[i]) not in used for i in range(n)):
                    break
            else:
                ok = False
                break
            perms.append(p)
            used |= {(i, p[i]) for i in range(n)}
        if ok:
            S = np.zeros((n, n), int)
            for k, p in enumerate(perms):
                for i in range(n):
                    S[i, p[i]] = 1 if k < 2 else -1
            return S


def move(S, rng):
    T = S.copy()
    for _ in range(100):
        i, i2 = rng.sample(range(n), 2)
        j, j2 = rng.sample(range(n), 2)
        a, b, c, d = T[i, j], T[i, j2], T[i2, j], T[i2, j2]
        # rectangle move: add (x, -x; -x, x) keeping entries in {-1,0,1} and row/col +/- counts
        for x in (1, -1):
            na, nb, nc, nd = a + x, b - x, c - x, d + x
            if all(v in (-1, 0, 1) for v in (na, nb, nc, nd)):
                # counts of +1 and -1 per row/col preserved iff the multiset {a,b} -> {na,nb} same and {c,d},{a,c},{b,d}
                if sorted((a, b)) == sorted((na, nb)) and sorted((c, d)) == sorted((nc, nd)) and \
                        sorted((a, c)) == sorted((na, nc)) and sorted((b, d)) == sorted((nb, nd)):
                    T[i, j], T[i, j2], T[i2, j], T[i2, j2] = na, nb, nc, nd
                    return T
    return T


def check(S):
    for M in (S, S.T):
        for r in M:
            if sorted(r.tolist()) != [-1, -1] + [0] * 6 + [1, 1]:
                return False
    return True


seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
rng = random.Random(seed)
best_all = 99
for restart in range(int(sys.argv[2]) if len(sys.argv) > 2 else 40):
    S = init(rng)
    c = cost(S)
    temp = 2.0
    for it in range(4000):
        T = move(S, rng)
        ct = cost(T)
        if ct <= c or rng.random() < math.exp((c - ct) / temp):
            S, c = T, ct
        temp = max(0.05, temp * 0.999)
        if c < best_all:
            best_all = c
            assert check(S)
            print('restart', restart, 'iter', it, 'new best rank sum', c, flush=True)
        if c <= 4:
            print('FOUND rank sum <= 4:\n', S)
            sys.exit(0)
print('best rank sum found', best_all)
