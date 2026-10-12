"""Lab session, 2026-10-12. SAMPLING of the strongly regular graphs (243,22,1,2) with a semiregular elementary abelian
group H = Z_3^m (m = 3: nine orbits of 27 vertices; m = 2: 27 orbits of 9; m = 4: three orbits of 81).

Model: vertices (i, g), i < r = 3^(5-m), g in H; (i, g) ~ (j, h) iff h - g in D_ij, D_ji = -D_ij, D_ii = -D_ii,
0 not in D_ii. For all i <= j and d (not (i = j, d = 0)):  sum_k #{g in D_ik : d - g in D_kj} + [d in D_ij] = 2,
and every vertex has degree 22. No normal form is imposed: this is NOT a complete census. Each cadical call uses a new
seed, a shuffled clause order and a few random decisions ("orbit 0 is / is not a coclique", a random element in or out
of some D_0j); every solution is rebuilt, checked strongly regular and compared with the reference graphs and with the
graphs found before by a direct isomorphism test (aut_tools). New graphs are written to the output directory.

python semireg_sample.py <tmp dir> <m> <seconds per call> <number of calls> <first seed> [reference edge files ...]
Memory: m = 3: about 2.7 million clauses, under 2 GB."""
import sys, os, subprocess, time, itertools, collections, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T


def encode(m):
    r = 3 ** (5 - m); H = list(itertools.product(range(3), repeat=m)); IDX = {g: i for i, g in enumerate(H)}; ZERO = (0,) * m
    neg = lambda a: tuple((-x) % 3 for x in a); sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
    REPS = [g for g in H if g != ZERO and g < neg(g)]
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    U = [dict() for _ in range(r)]
    for i in range(r):
        for g in REPS: v = new(); U[i][g] = v; U[i][neg(g)] = v
    V = {(i, j): {g: new() for g in H} for i in range(r) for j in range(i + 1, r)}
    def mm(i, k, g):
        if i == k: return None if g == ZERO else U[i][g]
        return V[(i, k)][g] if i < k else V[(k, i)][neg(g)]
    cache = {}
    def AND(a, b):
        if a is None or b is None: return None
        if a == b: return a
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            t = new(); cl.extend([[-t, a], [-t, b], [t, -a, -b]]); cache[k] = t
        return cache[k]
    def exactly(lits, k):
        lits = [l for l in lits if l is not None]
        if k < 0 or k > len(lits): cl.append([]); return
        prev = None
        for l in lits:
            cur = [None] + [new() for _ in range(k + 1)]
            for j in range(1, k + 2):
                pj = prev[j] if prev else None
                if pj is not None: cl.append([-pj, cur[j]])
                if j == 1: cl.append([-l, cur[j]])
                elif prev: cl.append([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cl.append(c + [l])
                if j > 1: cl.append(c + ([prev[j - 1]] if prev else []))
            prev = cur
        if k >= 1: cl.append([prev[k]])
        cl.append([-prev[k + 1]])
    for i in range(r):                                               # degree 22 (the diagonal pairs count twice)
        lits = [U[i][g] for g in REPS] * 2 + [mm(i, j, g) for j in range(r) if j != i for g in H]
        exactly(lits, 22)
    if os.environ.get("DIAG"):                                       # prescribed sizes |D_ii| (comma separated)
        for i, a in enumerate(map(int, os.environ["DIAG"].split(","))): exactly([U[i][g] for g in REPS], a // 2)
    for i in range(r):
        for j in range(i, r):
            for d in (REPS if i == j else H):
                lits = [AND(mm(i, k, g), mm(k, j, sub(d, g))) for k in range(r) for g in H]
                exactly(lits + [mm(i, j, d)], 2)
    return nv[0], cl, U, V, H, REPS, r


if __name__ == "__main__":
    tmp, m, tl, ncalls, seed0 = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    refs = [(os.path.basename(p), T.load(p)) for p in sys.argv[6:]]
    t0 = time.time(); nv, cl, U, V, H, REPS, r = encode(m); nH = len(H); ZERO = (0,) * m
    neg = lambda a: tuple((-x) % 3 for x in a); add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b)); IDX = {g: i for i, g in enumerate(H)}
    print("semiregular Z_3^%d, %d orbits: %d variables, %d clauses (built in %.0f s)" % (m, r, nv, len(cl), time.time() - t0), flush=True)
    tally = collections.Counter(); path = os.path.join(tmp, "semireg_%d_%d.cnf" % (m, os.getpid()))
    for call in range(ncalls):
        rnd = random.Random(seed0 + call); extra = []
        if rnd.random() < 0.5: extra.append([rnd.choice([1, -1]) * U[0][rnd.choice(REPS)]])
        for _ in range(rnd.randrange(0, 4)):
            j = rnd.randrange(1, r); extra.append([rnd.choice([1, -1]) * V[(0, j)][rnd.choice(H)]])
        order = list(range(len(cl))); rnd.shuffle(order)
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv, len(cl) + len(extra)))
            for c in extra: f.write(" ".join(map(str, c)) + " 0\n")
            for t in order: f.write(" ".join(map(str, cl[t])) + " 0\n")
        t1 = time.time()
        try: out = subprocess.run([CAD, "-q", "--seed=%d" % (seed0 + call), path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
        if res != "SAT":
            print("call %d (seed %d, %d random decisions): %s (%.0f s)" % (call, seed0 + call, len(extra), res, time.time() - t1), flush=True); tally[res] += 1; continue
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        A = np.zeros((243, 243), dtype=np.int64)
        for i in range(r):
            for g in H:
                x = nH * i + IDX[g]
                for d in H:
                    if d != ZERO and U[i][d] in model: A[x, nH * i + IDX[add(g, d)]] = 1
                for j in range(i + 1, r):
                    for d in H:
                        if V[(i, j)][d] in model: y = nH * j + IDX[add(g, d)]; A[x, y] = A[y, x] = 1
        ok = bool((A @ A == 20 * np.eye(243, dtype=np.int64) - A + 2).all())
        diag = tuple(int(sum(1 for d in H if d != ZERO and U[i][d] in model)) for i in range(r))
        name = next((nm for nm, R in refs if T.find_iso(A, R) is not None), None) if ok else "NOT STRONGLY REGULAR"
        if name is None:
            name = "new_Z3x%d_seed%d.edges" % (m, seed0 + call); refs.append((name, A))
            with open(os.path.join(tmp, name), "w", newline="\n") as f:
                for a in range(243):
                    for b in range(a + 1, 243):
                        if A[a, b]: f.write("%d %d\n" % (a, b))
            o, gens, base, sizes = T.aut_group(A)
            print("   NEW GRAPH written to %s: |Aut| = %d, vertex orbits %s" % (name, o, [len(x) for x in T.vertex_orbits(243, gens)]), flush=True)
        tally[name] += 1
        print("call %d (seed %d, %d random decisions): SAT in %.0f s; strongly regular %s; sizes |D_ii| %s; graph: %s" % (call, seed0 + call, len(extra), time.time() - t1, ok, diag, name), flush=True)
    print("tally: %s" % tally.most_common(), flush=True)
    try: os.remove(path)
    except OSError: pass
