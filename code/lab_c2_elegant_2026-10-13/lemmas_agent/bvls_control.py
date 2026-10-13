# Control on the Berlekamp-van Lint-Seidel graph srg(243,22,1,2) (11 blocks, eigenvalues 22, 4, -5).  Microscope only.
# 1. builds the involution "opposite corner at vertex 0" (the map of A.1), checks it is an automorphism with one fixed vertex;
# 2. builds the signed quotient S (121 x 121), checks S^2 + S = 20 I, the block shape and the row supports;
# 3. checks the analogue of Lemma 5 of the report (norm of k a - H c, H = 4I - S, H^2 = 9H) on random integer c;
# 4. finds sigma-odd (-5)-eigenfunctions with entries 0,+-1 among small combinations of the columns of H and checks the
#    analogue of the identity (I1):  sum over z outside S of C(d(z),2) = m^2 - 11 m - 9 e - Q2.
# usage: python -I bvls_control.py <path to bvls243.edges>      (reads the file only; < 1 minute, < 200 MB)
import sys, random
import numpy as np

path = sys.argv[1]
n = 243
A = np.zeros((n, n), dtype=np.int64)
for line in open(path):
    s = line.split()
    if len(s) == 2:
        a, b = int(s[0]), int(s[1])
        A[a, b] = A[b, a] = 1
assert (A.sum(axis=1) == 22).all()
A2 = A @ A
assert (A2 + A == 20 * np.eye(n, dtype=np.int64) + 2 * np.ones((n, n), dtype=np.int64)).all()
print("srg(243,22,1,2): A^2 + A = 20 I + 2 J  OK")

x = 0
nb = [v for v in range(n) if A[x, v]]
sig = [-1] * n
sig[x] = x
for a in nb:
    cn = [v for v in nb if A[a, v]]
    assert len(cn) == 1
    sig[a] = cn[0]
outer = [v for v in range(n) if v != x and not A[x, v]]
key = {}
for z in outer:
    ab = tuple(sorted(v for v in nb if A[z, v]))
    assert len(ab) == 2
    key[ab] = z
for z in outer:
    ab = tuple(sorted(v for v in nb if A[z, v]))
    img = tuple(sorted(sig[v] for v in ab))
    sig[z] = key[img]
sig = np.array(sig)
assert (sig[sig] == np.arange(n)).all() and (sig == np.arange(n)).sum() == 1
assert (A[np.ix_(sig, sig)] == A).all()
print("opposite-corner map at vertex 0: automorphism of order 2 with exactly one fixed vertex  OK")

# orbits: inner first (blocks), then outer
reps = []
seen = set([x])
for a in nb:
    if a not in seen:
        reps.append(a); seen.add(a); seen.add(int(sig[a]))
n_in = len(reps)
for z in outer:
    if z not in seen:
        reps.append(z); seen.add(z); seen.add(int(sig[z]))
N = len(reps)
reps = np.array(reps)
S = A[np.ix_(reps, reps)] - A[np.ix_(reps, sig[reps])]
assert n_in == 11 and N == 121
assert (S @ S + S == 20 * np.eye(N, dtype=np.int64)).all()
assert (S[:n_in, :n_in] == -np.eye(n_in, dtype=np.int64)).all()
assert ((S[n_in:, :n_in] != 0).sum(axis=1) == 2).all()
assert ((S[n_in:, n_in:] != 0).sum(axis=1) == 18).all() and (np.diag(S)[n_in:] == 0).all()
print("signed quotient: 121 x 121, S^2 + S = 20 I, inner block -I_11, outer rows: 2 + 18 non-zero entries  OK")

H = 4 * np.eye(N, dtype=np.int64) - S
assert (H @ H == 9 * H).all()
random.seed(1)
for trial in range(200):
    i = random.randrange(N)
    a = H[:, i].copy()
    k = random.randint(-4, 4)
    c = np.array([random.randint(-2, 2) if random.random() < 0.2 else 0 for _ in range(N)], dtype=np.int64)
    w = k * a - H @ c
    assert ((S @ w) == -5 * w).all()
    assert int(w @ w) == k * k * int(a @ a) - 18 * k * int(a @ c) + 9 * int(c @ H @ c)
    assert (int(w @ w) - k * k * int(a @ a)) % 9 == 0
print("analogue of Lemma 5: |k a - H c|^2 = k^2 |a|^2 - 18 k (a,c) + 9 c^t H c, on 200 random (a, k, c)  OK")

# 0,+-1 eigenfunctions: recover coordinates in F_3^5 from the graph (translations along lines), then use the functions
# phi_w(v) = [w.v = 1] - [w.v = 2].
def translation(s):
    t = [-1] * n
    t[x] = s
    two_s = int(sig[s])                      # the third point of the line {0, s, 2s} is the mate of s
    for a in nb:
        if a == s:
            t[a] = two_s
        elif a == two_s:
            t[a] = x
        else:
            cn = [v for v in range(n) if A[s, v] and A[a, v] and v != x]
            assert len(cn) == 1
            t[a] = cn[0]
    for z in outer:
        a, b = [v for v in nb if A[z, v]]
        cn = [v for v in range(n) if A[t[a], v] and A[t[b], v] and v != s]
        assert len(cn) == 1
        t[z] = cn[0]
    t = np.array(t)
    assert sorted(t) == list(range(n)) and (A[np.ix_(t, t)] == A).all()
    return t

coords = {x: ()}
gens = []
for s in nb:
    if s in coords:
        continue
    t = translation(s)
    gens.append(t)
    new = {}
    for v, c in coords.items():
        v1 = int(t[v]); v2 = int(t[v1])
        new[v] = c + (0,); new[v1] = c + (1,); new[v2] = c + (2,)
    assert len(new) == 3 * len(coords)
    coords = new
    if len(coords) == n:
        break
assert len(coords) == n and len(gens) == 5
X = np.array([coords[v] for v in range(n)])
print("coordinates in F_3^5 recovered from 5 translations (each checked to be an automorphism)  OK")
import itertools
cnt = {4: 0, -5: 0}
shown = 0
for w in itertools.product(range(3), repeat=5):
    if not any(w):
        continue
    val = (X @ np.array(w)) % 3
    phi = (val == 1).astype(np.int64) - (val == 2).astype(np.int64)
    Aphi = A @ phi
    if (Aphi == 4 * phi).all():
        cnt[4] += 1
    elif (Aphi == -5 * phi).all():
        cnt[-5] += 1
        assert (phi[sig] == -phi).all()
        if shown < 3:
            shown += 1
            P = np.where(phi == 1)[0]
            m = len(P)
            dP = A[:, P].sum(axis=1)
            e = int(dP[P].sum()) // 2
            Q2 = int((dP[P] ** 2).sum())
            lhs = sum(int(dP[z]) * (int(dP[z]) - 1) // 2 for z in range(n) if phi[z] == 0)
            rhs = m * m - 11 * m - 9 * e - Q2
            print(f"   w = {w}: m = {m}, e = {e}, Q2 = {Q2}: sum C(d,2) outside = {lhs}, m^2 - 11m - 9e - Q2 = {rhs}",
                  "OK" if lhs == rhs else "MISMATCH")
    else:
        raise SystemExit("not an eigenfunction")
print("functions phi_w: eigenvalue 4 for", cnt[4], "vectors w, eigenvalue -5 for", cnt[-5], "(expected 132 and 110)")
