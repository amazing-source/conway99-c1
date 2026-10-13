"""Lab session, 2026-10-13. Mission "C2 without computation", step 2: generators with one vector h.
Builds tables (heptad1.table) for random patterns (y1, y2, h) in Z^j and i = 0, 1, 2, appends them to
h1_tables_<DMAX>.pkl, and prints the rank (modulo a 61-bit prime) of everything accumulated so far.
Run it several times with different seeds until the rank stops growing.
python heptad1_gen.py <DMAX> <number of patterns> <seed> <max seconds>       one process, < 1 GB."""
import sys, os, time, pickle
import heptad1 as H

DMAX, npat, seed, tmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
fn = "h1_tables_%d.pkl" % DMAX
desc, tabs = pickle.load(open(fn, "rb")) if os.path.exists(fn) else ([], [])
have = {(tuple(d[0]), d[1]) for d in desc}
t0 = time.time()
for p in H.random_patterns(npat, seed):
    for i in range(0, (24 - len(p)) // 8 + 1):
        if (tuple(p), i) in have:
            continue
        if time.time() - t0 > tmax:
            break
        tabs.append(H.table(p, i, DMAX))
        desc.append((p, i))
        have.add((tuple(p), i))
pickle.dump((desc, tabs), open(fn, "wb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
P = (1 << 61) - 1


def rank_mod(Mat):
    A = [[int(x) % P for x in row] for row in Mat]
    rows = len(A)
    r = 0
    for c in range(len(A[0])):
        pr = next((i for i in range(r, rows) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], P - 2, P)
        A[r] = [(x * inv) % P for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(x - f * y) % P for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


print("%d generators in %s, %d non-zero table entries with D <= %d (integral %d, shadow %d); rank %d   (%.0f s)" % (
    len(tabs), fn, len(keys), DMAX, sum(1 for k in keys if k[0] == "I"), sum(1 for k in keys if k[0] == "S"),
    rank_mod([[t.get(k, 0) for k in keys] for t in tabs]), time.time() - t0), flush=True)
