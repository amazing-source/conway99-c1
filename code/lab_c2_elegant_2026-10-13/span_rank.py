"""Lab session, 2026-10-13. Mission "C2 without computation", step 1: rank of the explicit generators.
Generators: (a) Theta_{Z^j; y} theta_3^c (16 Delta_8)^i (jacobi_tables.table);
            (b) the same with a part of y in E8 (jacobi_e8.table_e8).
Saves the tables in gen_tables_<EMAX>.pkl and prints the rank (modulo a 61-bit prime) against the dimension 61.
python span_rank.py <EMAX> <number of E8 generators> <seed>         one process, a few minutes, < 2 GB."""
import sys, time, pickle, random
import jacobi_tables as JT
import jacobi_e8 as JE

EMAX, nE8, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
emax4 = 4 * EMAX
t0 = time.time()
rnd = random.Random(seed)
tabs = []
desc = []
for p in JT.patterns():
    for i in range(0, (24 - len(p)) // 8 + 1):
        tabs.append(JT.table(list(p), i, emax4))
        desc.append(("Z", p, i))
print("Z generators: %d (%.0f s)" % (len(tabs), time.time() - t0), flush=True)
V = JE.e8_vectors()
norms = (V * V).sum(1) // 4
by = {k: V[norms == k] for k in (0, 2, 4, 6)}
tries = 0
made = 0
while made < nE8 and tries < 100000:
    tries += 1
    n1, n2 = rnd.choice((0, 2, 4, 6)), rnd.choice((2, 4, 6))
    r1 = by[n1][rnd.randrange(len(by[n1]))]
    r2 = by[n2][rnd.randrange(len(by[n2]))]
    ip = int(r1 @ r2) // 4
    pats = JE.z_patterns(7 - n1, 7 - n2, -ip)
    if not pats:
        continue
    p = rnd.choice(pats)
    if 8 + len(p) > 24:
        continue
    i = rnd.randrange(0, (24 - 8 - len(p)) // 8 + 1)
    tabs.append(JE.table_e8(tuple(int(x) for x in r1), tuple(int(x) for x in r2), list(p), i, emax4))
    desc.append(("E8", (n1, n2, ip), tuple(int(x) for x in r1), tuple(int(x) for x in r2), p, i))
    made += 1
    if made % 10 == 0:
        print("   %d E8 generators (%.0f s)" % (made, time.time() - t0), flush=True)
pickle.dump((desc, tabs), open("gen_tables_%d.pkl" % EMAX, "wb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
M = [[t.get(k, 0) for k in keys] for t in tabs]
p = (1 << 61) - 1


def rank_mod(Mat):
    A = [[int(x) % p for x in row] for row in Mat]
    rows = len(A)
    cols = len(A[0])
    r = 0
    for c in range(cols):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


nz = sum(1 for d in desc if d[0] == "Z")
print("%d generators (%d with E8), %d non-zero table entries for E <= %d" % (len(tabs), len(tabs) - nz, len(keys), EMAX))
print("rank of the Z generators alone: %d ; rank of all: %d ; dimension of the space: 61" % (rank_mod(M[:nz]), rank_mod(M)), flush=True)
