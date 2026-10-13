"""Lab session, 2026-10-13. Mission "C2 without computation", step 2: generators with one vector h and a part in E8.
(U; y1, y2, h) with U = E8 + Z^16 (times theta_3^c (16 Delta_8)^i on the unused coordinates), y_a = (r_a, w_a),
h = (r_3, w_3), r in E8, w in Z^j. Tables as in heptad1.py; appended to h1_tables_<DMAX>.pkl.
python heptad1_e8.py <DMAX> <number of generators> <seed> <max seconds>       one process, < 1 GB."""
import sys, os, time, pickle, random
import numpy as np
import heptad1 as H
import jacobi_e8 as JE
from jacobi_tables import MMAX, TH2, TH3, TH4D, D16, mul, series_pow

DMAX, ngen, seed, tmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
fn = "h1_tables_%d.pkl" % DMAX
desc, tabs = pickle.load(open(fn, "rb")) if os.path.exists(fn) else ([], [])
rnd = random.Random(seed)
V = JE.e8_vectors()
norms = (V * V).sum(1) // 4
by = {k: V[norms == k] for k in (0, 2, 4, 6)}
mV = (V * V).sum(1)


def e8_part(r1, r2, r3):
    A = (V @ np.array(r1)) // 2
    B = (V @ np.array(r2)) // 2
    T = (V @ np.array(r3)) // 2
    P = np.zeros((MMAX + 1, H.NA, H.NA, H.NT), dtype=np.int64)
    ok = (np.abs(A) <= H.AM) & (np.abs(B) <= H.AM) & (np.abs(T) <= H.TM)
    np.add.at(P, (mV[ok], A[ok] + H.AM, B[ok] + H.AM, T[ok] + H.TM), 1)
    return P


def convolve(P, types, shadow):
    for s, t, u in types:
        Q = np.zeros_like(P)
        vals = [2 * k + 1 for k in range(-4, 4)] if shadow else [2 * k for k in range(-3, 4)]
        for w in vals:
            dm, da, db, dt = w * w, s * w, t * w, u * w
            if dm > MMAX:
                continue
            a0, a1 = max(0, -da), min(H.NA, H.NA - da)
            b0, b1 = max(0, -db), min(H.NA, H.NA - db)
            c0, c1 = max(0, -dt), min(H.NT, H.NT - dt)
            if a0 >= a1 or b0 >= b1 or c0 >= c1:
                continue
            Q[dm:, a0 + da:a1 + da, b0 + db:b1 + db, c0 + dt:c1 + dt] += P[:MMAX + 1 - dm, a0:a1, b0:b1, c0:c1]
        P = Q
    return P


def z_part(n1, n2, n3, p12, p13, p23):
    """vectors w1, w2, w3 of Z^j with norms n1, n2, n3 and inner products p12, p13, p23; None if not found"""
    for _ in range(400):
        j = rnd.randrange(1, 13)
        ws = []
        for nn in (n1, n2, n3):
            v = [0] * j
            left = nn
            pos = list(range(j))
            rnd.shuffle(pos)
            for q in pos:
                if left == 0:
                    break
                val = 2 if (left >= 4 and rnd.random() < 0.3) else 1
                v[q] = val * rnd.choice((1, -1))
                left -= val * val
            if left:
                ws = None
                break
            ws.append(v)
        if ws is None:
            continue
        ip = lambda a, b: sum(x * y for x, y in zip(a, b))
        if ip(ws[0], ws[1]) == p12 and ip(ws[0], ws[2]) == p13 and ip(ws[1], ws[2]) == p23:
            return [(ws[0][q], ws[1][q], ws[2][q]) for q in range(j) if (ws[0][q], ws[1][q], ws[2][q]) != (0, 0, 0)]
    return None


t0 = time.time()
made = 0
tries = 0
while made < ngen and time.time() - t0 < tmax and tries < 100000:
    tries += 1
    n1, n2, n3 = rnd.choice((0, 2, 4, 6)), rnd.choice((0, 2, 4, 6)), rnd.choice((0, 0, 2, 4))
    if n1 == 0 and n2 == 0 and n3 == 0:
        continue
    r = [by[n][rnd.randrange(len(by[n]))] for n in (n1, n2, n3)]
    p = [int(r[a] @ r[b]) // 4 for a, b in ((0, 1), (0, 2), (1, 2))]
    types = z_part(7 - n1, 7 - n2, 4 - n3, -p[0], -p[1], -p[2])
    if types is None or 8 + len(types) > 24:
        continue
    i = rnd.randrange(0, (24 - 8 - len(types)) // 8 + 1)
    c = 24 - 8 - len(types) - 8 * i
    base = e8_part(*[tuple(int(x) for x in v) for v in r])
    out = {}
    for kind, shadow in (("I", False), ("S", True)):
        red = H.reduce_part(convolve(base.copy(), types, shadow), shadow, DMAX)
        if shadow:
            scal = mul(series_pow(TH2, c), [((-1) ** i) * x for x in series_pow(TH4D, 8 * i)])
        else:
            scal = mul(series_pow(TH3, c), series_pow(D16, i))
        for (kd, cl, D), v in red.items():
            for dm, x in enumerate(scal):
                if x and D + 7 * dm <= DMAX:
                    out[(kd, cl, D + 7 * dm)] = out.get((kd, cl, D + 7 * dm), 0) + x * v
    tabs.append(out)
    desc.append((("E8", n1, n2, n3, tuple(p), tuple(types)), i))
    made += 1
pickle.dump((desc, tabs), open(fn, "wb"))
keys = sorted(k for k in set().union(*[set(t) for t in tabs]) if any(t.get(k, 0) for t in tabs))
P61 = (1 << 61) - 1


def rank_mod(Mat):
    A = [[int(x) % P61 for x in row] for row in Mat]
    rows = len(A)
    r_ = 0
    for c_ in range(len(A[0])):
        pr = next((q for q in range(r_, rows) if A[q][c_]), None)
        if pr is None:
            continue
        A[r_], A[pr] = A[pr], A[r_]
        inv = pow(A[r_][c_], P61 - 2, P61)
        A[r_] = [(x * inv) % P61 for x in A[r_]]
        for q in range(rows):
            if q != r_ and A[q][c_]:
                f = A[q][c_]
                A[q] = [(x - f * y) % P61 for x, y in zip(A[q], A[r_])]
        r_ += 1
        if r_ == rows:
            break
    return r_


print("added %d E8 generators (%.0f s); %d generators in all, %d non-zero entries (integral %d, shadow %d); rank %d" % (
    made, time.time() - t0, len(tabs), len(keys), sum(1 for k in keys if k[0] == "I"), sum(1 for k in keys if k[0] == "S"),
    rank_mod([[t.get(k, 0) for k in keys] for t in tabs])), flush=True)
