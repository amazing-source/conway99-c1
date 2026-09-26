"""A111111 type (3,3) (TFS): Q_c = P_mu - P_tau - 2P_sigma - I = -(I + P_sigma + P_tau) (C2 letters, mu = sigma).
t_c = dim ker Q_c mod 7 = 4; q:7 forces balanced torsion (r0 >= 1) whatever g is.  Lists the projective points of ker Q_c
up to the stabilizer of (mu, tau) in the signed block permutations, flagging single-component vectors
(never balanced, notes/129 sec. 8).  Labels 0..11: block i//2, sign + if i even, sigma(i) = i^1."""
import itertools, json
import numpy as np

P = 7
mu = [i ^ 1 for i in range(12)]
tau = [None] * 12


def link(x, y):
    tau[x], tau[y] = y, x


# two 3-cycles of blocks: (0- <-> 1+, 1- <-> 2+, 2- <-> 0+) and (3- <-> 4+, 4- <-> 5+, 5- <-> 3+)
for (a, b) in [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]:
    link(2 * a + 1, 2 * b)
assert all(tau[tau[i]] == i and tau[i] != (i ^ 1) and tau[i] != i for i in range(12))
Q = np.zeros((12, 12), int)
for i in range(12):
    Q[i, i] -= 1
    Q[i, i ^ 1] -= 1
    Q[i, tau[i]] -= 1
Q %= P


def nullspace(M):
    M = [list(map(int, r)) for r in M]
    n, m = len(M), len(M[0])
    piv, r = [], 0
    for c in range(m):
        p = next((i for i in range(r, n) if M[i][c] % P), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        inv = pow(M[r][c], P - 2, P)
        M[r] = [x * inv % P for x in M[r]]
        for i in range(n):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
    free = [c for c in range(m) if c not in piv]
    basis = []
    for fc in free:
        v = [0] * m
        v[fc] = 1
        for i, pc in enumerate(piv):
            v[pc] = (-M[i][fc]) % P
        basis.append(v)
    return np.array(basis)


K = nullspace(Q)
print('dim ker Q_c mod 7 =', len(K))
# group: signed block permutations g preserving mu (automatic) and tau: g tau g^-1 = tau
G = []
for perm in itertools.permutations(range(6)):
    for flips in range(64):
        g = [2 * perm[i // 2] + ((i % 2) ^ ((flips >> (i // 2)) & 1)) for i in range(12)]
        if all(g[tau[i]] == tau[g[i]] for i in range(12)):
            G.append(g)
print('stabilizer order', len(G))


def normalize(v):
    v = [int(x) % P for x in v]
    k = next(x for x in v if x)
    inv = pow(k, P - 2, P)
    return tuple(x * inv % P for x in v)


points = set()
for coeffs in itertools.product(range(P), repeat=len(K)):
    if not any(coeffs):
        continue
    v = (np.array(coeffs) @ K) % P
    points.add(normalize(v))
print('projective points', len(points))
comp1 = set(range(6))           # labels of blocks 0,1,2
seen, reps = set(), []
for v in sorted(points):
    if v in seen:
        continue
    orb = set()
    for g in G:
        w = [0] * 12
        for i in range(12):
            w[g[i]] = v[i]          # (g.v)(g i) = v(i)
        orb.add(normalize(w))
    seen |= orb
    single = all(v[i] == 0 for i in range(6, 12)) or all(v[i] == 0 for i in range(6))
    reps.append({'phi': list(v), 'orbit_size': len(orb), 'single_component': single})
print('orbits of projective torsion points:', len(reps),
      ' mixed:', sum(1 for r in reps if not r['single_component']))
json.dump({'mu': mu, 'tau': tau, 'torsion_reps': reps}, open('A33_torsion_reps.json', 'w'), indent=1)
for r in reps:
    print(r)
