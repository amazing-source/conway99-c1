"""SAT encoding of the 3-layer column stage (notes/163).  Variables: X[e][f], Y[e][g] (permutations between the
edge sets of layers 0-1 and 0-2), A[e][z] = [z in phi01(e)], B[e][y] = [y in phi02(e)], P[e][z][y] = A and B.
Constraints: X, Y permutation matrices; sum_{e ni x} A[e][z] = N01[x][z]; sum_{e ni x} B[e][y] = N02[x][y];
sum_e P[e][z][y] = N12[z][y].  Usage: python3 colsat.py planted SEED | random SEED COUNT TIMEOUT"""
import sys, os, random, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(__file__))
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from coldrive import planted, random_C
from colmodel import predicted
KISSAT = "/tmp/solvers/kissat/build/kissat"


def encode(m, mates, N01, N02, N12):
    pool = IDPool(); cnf = CNF()
    E = [[(x, y) for x in range(m) for y in range(x + 1, m) if mt[x] != y] for mt in mates]
    X = {(e, f): pool.id(("X", e, f)) for e in range(len(E[0])) for f in range(len(E[1]))}
    Y = {(e, g): pool.id(("Y", e, g)) for e in range(len(E[0])) for g in range(len(E[2]))}
    def card_eq(lits, k):
        if k < 0 or k > len(lits): cnf.append([]); return
        enc = CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.totalizer)
        cnf.extend(enc.clauses)
    for e, (x, y) in enumerate(E[0]):           # pre-filter impossible pairs
        for f, (z, z2) in enumerate(E[1]):
            if min(N01[u][w] for u in (x, y) for w in (z, z2)) <= 0: cnf.append([-X[e, f]])
        for g, (u2, w2) in enumerate(E[2]):
            if min(N02[u][w] for u in (x, y) for w in (u2, w2)) <= 0: cnf.append([-Y[e, g]])
    n0, n1, n2 = len(E[0]), len(E[1]), len(E[2])
    for e in range(n0):
        card_eq([X[e, f] for f in range(n1)], 1); card_eq([Y[e, g] for g in range(n2)], 1)
    for f in range(n1): card_eq([X[e, f] for e in range(n0)], 1)
    for g in range(n2): card_eq([Y[e, g] for e in range(n0)], 1)
    A = {(e, z): pool.id(("A", e, z)) for e in range(n0) for z in range(m)}
    B = {(e, y): pool.id(("B", e, y)) for e in range(n0) for y in range(m)}
    for e in range(n0):
        for z in range(m):
            fs = [X[e, f] for f, p in enumerate(E[1]) if z in p]
            cnf.append([-A[e, z]] + fs)
            for v in fs: cnf.append([-v, A[e, z]])
            gs = [Y[e, g] for g, p in enumerate(E[2]) if z in p]
            cnf.append([-B[e, z]] + gs)
            for v in gs: cnf.append([-v, B[e, z]])
    for x in range(m):
        es = [e for e, p in enumerate(E[0]) if x in p]
        for z in range(m): card_eq([A[e, z] for e in es], N01[x][z]); card_eq([B[e, z] for e in es], N02[x][z])
    for z in range(m):
        for y in range(m):
            ps = []
            for e in range(n0):
                p = pool.id(("P", e, z, y)); ps.append(p)
                cnf.extend([[-p, A[e, z]], [-p, B[e, y]], [p, -A[e, z], -B[e, y]]])
            card_eq(ps, N12[z][y])
    return cnf


def solve(cnf, timeout):
    path = f"/tmp/claude-0/-home-user/899e78f1-d1e3-5aeb-b4c1-585fa11b4ff7/scratchpad/col_{os.getpid()}.cnf"
    cnf.to_file(path); t = time.time()
    try:
        out = subprocess.run([KISSAT, "-q", f"--time={timeout}", path], capture_output=True, text=True).stdout
    finally:
        os.remove(path)
    st = "SAT" if "s SATISFIABLE" in out else "UNSAT" if "s UNSATISFIABLE" in out else "UNKNOWN"
    return st, time.time() - t


if __name__ == "__main__":
    mode = sys.argv[1]; rng = random.Random(int(sys.argv[2]))
    if mode == "planted":
        for i in range(int(sys.argv[3])):
            mates, N = planted(12, rng); cnf = encode(12, mates, *N)
            st, t = solve(cnf, int(sys.argv[4]))
            print(f"planted #{i}: vars {cnf.nv} clauses {len(cnf.clauses)} -> {st} in {t:.1f}s", flush=True)
    else:
        for i in range(int(sys.argv[3])):
            C, N = random_C(12, rng); cnf = encode(12, [C["M"], C["ta"], C["tb"]], *N)
            st, t = solve(cnf, int(sys.argv[4]))
            print(f"random C #{i}: vars {cnf.nv} clauses {len(cnf.clauses)} -> {st} in {t:.1f}s", flush=True)
