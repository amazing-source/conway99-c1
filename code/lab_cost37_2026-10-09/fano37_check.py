"""C1, lab session, 2026-10-10. Independent check of fano37.c (numpy, explicit vectors), base by base, for the two
ranks of the base (36: the base spans W; 35: one residual coordinate).

For a base given by its 15 edges on B0: the candidates of the ten members of B1 are built as explicit coordinate
vectors (c, t) in V + <n> (c = coordinates on the independent base vertices, t = coefficient of n, <n,n> = nu), all the
products are taken with the explicit Gram matrix diag(K_I, nu), and the search of the pilot (forward checking on every
remaining member) is run. The numbers of candidates and of nodes at every depth must be those printed by
"fano37 base ... fc" with the same node cap.

python fano37_check.py <first seed> <number of random bases> <node cap> [rank]   (rank 35 or 36: only such bases)
One process, below 1 GB."""
import sys, os, itertools, random, subprocess, re, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fano37_pilot import LINES, INC, inv_mod, independent_rows, cell, flag_lines, random_cubic
P7 = 7

def search_python(C, cap):
    """returns (rank, det, nu, sizes, nodes, nodes by depth, found) for the base C; nu = None when the rank is 36"""
    B0 = cell(0); B1 = cell(1); FL = flag_lines(); forb = set(FL) | {(4, 5), (6, 7), (8, 9)}
    quota1 = [1 + (0 in LINES[j]) for j, s in B1]; quota0 = [1 + (1 in LINES[j]) for j, s in B0]
    adj1 = np.zeros((10, 10), dtype=np.int64)
    for a, b in FL: adj1[a][b] = adj1[b][a] = 1
    triples = list(itertools.combinations(range(15), 3))
    A = np.zeros((39, 39), dtype=np.int64)
    for x in range(7):
        for y in range(7):
            if INC[x][y]: A[x][7 + y] = A[7 + y][x] = 1
    for t, (j, s) in enumerate(B0): A[29 + t][0] = A[0][29 + t] = 1; A[29 + t][7 + j] = A[7 + j][29 + t] = 1
    for a, b in FL: A[29 + a][29 + b] = A[29 + b][29 + a] = 1
    blk0 = [set() for _ in range(10)]
    for k, (a, b) in enumerate(C): A[14 + k][29 + a] = A[29 + a][14 + k] = 1; A[14 + k][29 + b] = A[29 + b][14 + k] = 1; blk0[a].add(k); blk0[b].add(k)
    K = (1 - np.eye(39, dtype=np.int64) - 2 * A) % P7
    I = independent_rows(K); rk = len(I)
    if rk not in (35, 36): return rk, None, None, None, 0, None, 0
    Kinv, det = inv_mod(K[np.ix_(I, I)])
    if rk == 36:
        if det in (1, 2, 4): return rk, det, None, None, 0, None, 0
        nu = 0                                                 # no residual coordinate
    else: nu = 3 if det in (1, 2, 4) else 1
    cands = []
    for m, (j, s) in enumerate(B1):
        lst = []
        for Pset in itertools.combinations(range(10), quota1[m]):
            if any(B0[t][0] == j and j != 0 for t in Pset): continue
            if len(Pset) == 2:
                a, b = Pset
                if (a, b) in forb or (blk0[a] & blk0[b]) or B0[a][0] == B0[b][0]: continue
            for tri in triples:
                T = set(tri)
                if any((B0[t][0] == j) + len(T & blk0[t]) > (1 if t in Pset else 2) for t in range(10)): continue
                if any(C[k][0] in Pset and C[k][1] in Pset for k in tri): continue
                a = np.zeros(39, dtype=np.int64); a[1] = 1; a[7 + j] = 1
                for t in Pset: a[29 + t] = 1
                for k in tri: a[14 + k] = 1
                sv = (1 - 2 * a) % P7                          # products with the 39 base vertices
                c = Kinv.dot(sv[I]) % P7                       # coordinates of the component in the span of the base
                if ((K[:, I].dot(c) - sv) % P7).any(): continue  # the dependent base vertices must agree too
                q = int(sv[I].dot(c)) % P7
                if rk == 36:
                    if q: continue
                    ts = [0]
                else:
                    tsq = (-q) * pow(nu, P7 - 2, P7) % P7
                    r = {0: 0, 1: 1, 2: 3, 4: 2}.get(tsq)
                    if r is None: continue
                    ts = [0] if r == 0 else [r, P7 - r]
                for t in ts: lst.append((c, t, sum(1 << k for k in tri), sum(1 << t2 for t2 in Pset)))
        cands.append(lst)
    sizes = [len(l) for l in cands]; order = sorted(range(10), key=lambda m: sizes[m])
    KI = K[np.ix_(I, I)]; pop = np.array([bin(i).count("1") for i in range(1 << 15)], dtype=np.int64)
    CM = [np.array([u[0] for u in l], dtype=np.int64).reshape(len(l), rk) for l in cands]      # coordinates
    TM = [np.array([u[1] for u in l], dtype=np.int64) for l in cands]                           # residual coefficients
    FM = [np.array([u[2] for u in l], dtype=np.int64) for l in cands]; BM = [np.array([u[3] for u in l], dtype=np.int64) for l in cands]
    comp = {}
    def compatible(x, i, y):
        """boolean vector over the candidates of the member in position y: compatible with candidate i of position x"""
        key = (x, i, y)
        if key not in comp:
            a, b = order[x], order[y]; u = cands[a][i]; want = 6 if adj1[a][b] else 1; lim = 0 if (adj1[a][b] or B1[a][0] == B1[b][0]) else 1
            G = (CM[b].dot(KI.dot(u[0]) % P7) + u[1] * nu * TM[b]) % P7        # explicit Gram matrix diag(K_I, nu)
            comp[key] = (G == want) & (pop[FM[b] & u[2]] + pop[BM[b] & u[3]] <= lim)
        return comp[key]
    nodes = 0; found = 0; lvl = [0] * 11
    def rec(x, alive, fcnt, bcnt):
        nonlocal nodes, found
        if x == 10:
            if all(v == 2 for v in fcnt) and all(bcnt[t] == quota0[t] for t in range(10)): found += 1
            return
        m = order[x]
        for i in np.nonzero(alive[x])[0]:
            nodes += 1; lvl[x + 1] += 1
            if nodes > cap: return
            f2 = list(fcnt); b2 = list(bcnt)
            for k in range(15):
                if (cands[m][i][2] >> k) & 1: f2[k] += 1
            for t in range(10):
                if (cands[m][i][3] >> t) & 1: b2[t] += 1
            fullf = sum(1 << k for k in range(15) if f2[k] == 2); fullb = sum(1 << t for t in range(10) if b2[t] == quota0[t])
            new = list(alive); dead = False
            for y in range(x + 1, 10):
                my = order[y]
                a = alive[y] & compatible(x, i, y) & ((FM[my] & fullf) == 0) & ((BM[my] & fullb) == 0)
                if not a.any(): dead = True; break
                new[y] = a
            if dead: continue
            rec(x + 1, new, f2, b2)
            if nodes > cap: return
    if min(sizes) > 0: rec(0, [np.ones(sizes[order[x]], dtype=bool) for x in range(10)], [0] * 15, [0] * 10)
    return rk, det, nu, sizes, nodes, lvl[1:], found

if __name__ == "__main__":
    s0, ns, cap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); only = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    forb = set(flag_lines()) | {(4, 5), (6, 7), (8, 9)}
    exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fano37.exe")
    bad = 0; done = {}; t0 = time.time(); seed = s0
    while sum(done.values()) < ns:
        C = random_cubic(random.Random(seed), forb); seed += 1
        env = dict(os.environ); env["FANO37_CAP"] = str(cap)
        cout = subprocess.run([exe, "base"] + [str(v) for e in C for v in e] + ["fc"], capture_output=True, text=True, env=env).stdout
        m = re.search(r"rank (\d+), determinant (\d), nu (\d); candidates per member: (.*)\nnodes (\d+) by depth: (.*); complete cells (\d+)", cout)
        if only and not (m and int(m.group(1)) == only): continue
        rk, det, nu, sizes, nodes, lvl, found = search_python(C, cap)
        if m is None:
            ok = ("dead by the discriminant" in cout and rk == 36 and det in (1, 2, 4)) or ("below 35" in cout and rk < 35); kind = "not searched"
        else:
            cr, cd, cnu = int(m.group(1)), int(m.group(2)), int(m.group(3)); cs = [int(v) for v in m.group(4).split()]; cn = int(m.group(5)); cl = [int(v) for v in m.group(6).split()]; cf = int(m.group(7))
            ok = (cr, cd) == (rk, det) and (rk == 36 or cnu == nu) and cs == sizes and cn == nodes and cl == lvl and cf == found; kind = "rank %d" % rk
            print("seed %d rank %d det %d nu %s: %s candidates %s nodes %d by depth %s cells %d" % (seed - 1, rk, det, nu, "OK" if ok else "MISMATCH", sizes, nodes, lvl, found))
            if not ok: print("   C:", cr, cd, cnu, cs, cn, cl, cf)
        bad += not ok; done[kind] = done.get(kind, 0) + 1
    print("bases compared %s; mismatches %d; node cap %d  [%.0f s]" % (sorted(done.items()), bad, cap, time.time() - t0))
