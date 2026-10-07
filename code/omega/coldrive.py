"""Driver for colsolve: planted tests, real 243 instances, random Conway-99 triangle structures C.
Usage: python3 coldrive.py planted|real243 PATH|random99 SEED COUNT MAXNODES"""
import sys, random, subprocess, time, itertools, os
sys.path.insert(0, os.path.dirname(__file__))
from colmodel import load_edges, triangle_structure, predicted
BIN = os.path.join(os.path.dirname(__file__), "colsolve")


def instance(m, mates, N01, N02, N12):
    lines = [str(m)] + [" ".join(map(str, mt)) for mt in mates]
    for N in (N01, N02, N12):
        lines += [" ".join(map(str, row)) for row in N]
    return "\n".join(lines) + "\n"


def run(inst, maxsol, maxnodes, timeout=None):
    out = subprocess.run([BIN, str(maxsol), str(maxnodes)], input=inst, capture_output=True, text=True,
                         timeout=timeout).stdout.split()
    d = dict(zip(out[0::2], out[1::2]))
    return {k: (float(v) if k == "time" else int(v)) for k, v in d.items()}


def rand_matching(m, rng):
    p = list(range(m)); rng.shuffle(p); mt = [0] * m
    for i in range(0, m, 2): mt[p[i]] = p[i + 1]; mt[p[i + 1]] = p[i]
    return mt


def planted(m, rng):
    mates = [[x ^ 1 for x in range(m)], rand_matching(m, rng), rand_matching(m, rng)]
    edges = [[(x, y) for x in range(m) for y in range(x + 1, m) if mates[L][x] != y] for L in range(3)]
    e1 = edges[1][:]; e2 = edges[2][:]; rng.shuffle(e1); rng.shuffle(e2)
    triples = list(zip(edges[0], e1, e2))
    N = [[[0] * m for _ in range(m)] for _ in range(3)]
    for p0, p1, p2 in triples:
        for (P, Q, k) in ((p0, p1, 0), (p0, p2, 1), (p1, p2, 2)):
            for u in P:
                for w in Q: N[k][u][w] += 1
    return mates, N


def local_ok_C(m, M, ta, tb, s):
    """lambda/mu inside the ball T u C (39 vertices for m=12), as in triangle_columns.rand_C"""
    n = 3 + 3 * m; A = [[0] * n for _ in range(n)]
    def e(i, j): A[i][j] = A[j][i] = 1
    e(0, 1); e(0, 2); e(1, 2)
    for x in range(m):
        e(0, 3 + x); e(1, 3 + m + x); e(2, 3 + 2 * m + x)
        e(3 + x, 3 + m + x); e(3 + x, 3 + 2 * m + x)
        if x < M[x]: e(3 + x, 3 + M[x])
        if x < ta[x]: e(3 + m + x, 3 + m + ta[x])
        if x < tb[x]: e(3 + 2 * m + x, 3 + 2 * m + tb[x])
        e(3 + m + x, 3 + 2 * m + s[x])
    for i in range(n):
        for j in range(i + 1, n):
            c = sum(A[i][t] & A[j][t] for t in range(n))
            if A[i][j]:
                if c != 1 and (i < 3 or j < 3): return False
                if c > 1: return False
            elif c > 2: return False
    return True


def random_C(m, rng):
    while True:
        M = [x ^ 1 for x in range(m)]
        ta, tb = rand_matching(m, rng), rand_matching(m, rng)
        s = list(range(m)); rng.shuffle(s)
        if local_ok_C(m, M, ta, tb, s):
            C = dict(m=m, M=M, ta=ta, tb=tb, s=s)
            N01, N02, N12 = predicted(C)
            if min(min(r) for N in (N01, N02, N12) for r in N) >= 0:
                return C, (N01, N02, N12)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "planted":
        rng = random.Random(int(sys.argv[2])); m = int(sys.argv[3]); cnt = int(sys.argv[4])
        for i in range(cnt):
            mates, N = planted(m, rng)
            r = run(instance(m, mates, *N), 10 ** 6, 10 ** 9)
            print(f"planted m={m} #{i}: {r}", flush=True)
    elif mode == "real243":
        adj = load_edges(sys.argv[2], 243); maxnodes = int(sys.argv[3])
        tri = [(v, a) for v in (0, 7, 100) for a in sorted(adj[v])[:2]]
        for v, a in tri:
            a2 = [u for u in adj[v] if u in adj[a]][0]
            C = triangle_structure(adj, v, a, a2); N = predicted(C)
            t0 = time.time(); r = run(instance(20, [C["M"], C["ta"], C["tb"]], *N), 1, maxnodes)
            print(f"real 243 triangle ({v},{a},{a2}): {r}  wall {time.time() - t0:.1f}s", flush=True)
    elif mode == "random99":
        rng = random.Random(int(sys.argv[2])); cnt = int(sys.argv[3]); maxnodes = int(sys.argv[4])
        for i in range(cnt):
            C, N = random_C(12, rng)
            r = run(instance(12, [C["M"], C["ta"], C["tb"]], *N), 10 ** 6, maxnodes)
            print(f"random C #{i}: {r}", flush=True)
