"""Conway, triangle {v,a,a'} (rooted labelling): column stage for a given triangle structure C = (tau, tau', sigma).
Far vertices = the 60 labels {x,y}, x,y in E (non-mates); each is adjacent to x,y (layer E), and to exactly 2 labels of
L_a and 2 of L_a' (mu with a, a').  Unknowns: y[w][l] for l in L_a u L_a'.
Exact pair design (lambda/mu): for C-vertices u != u', #far common neighbours = (2 - A_uu') - |common in triangle|
- |common in C|; far degree of every C-vertex = 10.  CP-SAT feasibility (necessary condition on C)."""
import itertools, random, sys, time
import numpy as np
from ortools.sat.python import cp_model

E = list(range(12)); mate = lambda x: x ^ 1


def build_C(t, tp, s):
    """vertices: 0=v,1=a,2=a'; E-layer x -> 3+x ; L_a {a,x} -> 15+x ; L_a' {a',x} -> 27+x"""
    N = 39; A = np.zeros((N, N), dtype=int)
    def e(i, j): A[i, j] = A[j, i] = 1
    e(0, 1); e(0, 2); e(1, 2)
    for x in E:
        e(0, 3 + x); e(1, 15 + x); e(2, 27 + x)
        e(3 + x, 15 + x); e(3 + x, 27 + x)
        if x < mate(x): e(3 + x, 3 + mate(x))
        if x < t[x]: e(15 + x, 15 + t[x])
        if x < tp[x]: e(27 + x, 27 + tp[x])
        e(15 + x, 27 + s[x])
    return A


def rand_C(rng):
    def rm():
        p = E[:]; rng.shuffle(p); m = {}
        for i in range(0, 12, 2): m[p[i]] = p[i + 1]; m[p[i + 1]] = p[i]
        return m
    while True:
        t, tp = rm(), rm(); s = dict(zip(E, rng.sample(E, 12)))
        A = build_C(t, tp, s)
        C2 = A @ A
        if all(C2[i, j] <= (1 if A[i, j] else 2) for i in range(39) for j in range(i + 1, 39)) and \
           all(C2[i, j] == 1 for i in range(39) for j in range(39) if i != j and A[i, j] and (i < 3 or j < 3)):
            return (t, tp, s), A


def column_model(A, tl=120, workers=3):
    far = [(x, y) for x, y in itertools.combinations(E, 2) if y != mate(x)]
    Lv = list(range(15, 39))
    m = cp_model.CpModel()
    Y = {(wi, l): m.NewBoolVar(f"y{wi}_{l}") for wi in range(60) for l in Lv}
    for wi in range(60):
        m.Add(sum(Y[wi, l] for l in range(15, 27)) == 2)
        m.Add(sum(Y[wi, l] for l in range(27, 39)) == 2)
    def inc(wi, u):
        x, y = far[wi]
        if 3 <= u < 15:
            return 1 if (u - 3) in (x, y) else 0
        return Y[wi, u]
    Cv = list(range(3, 39))
    C2 = A @ A
    for u in Cv:
        m.Add(sum(inc(wi, u) for wi in range(60)) == 10) if u >= 15 else None
    for u, u2 in itertools.combinations(Cv, 2):
        tri = sum(A[u, z] * A[u2, z] for z in range(3))
        cc = sum(A[u, z] * A[u2, z] for z in range(3, 39))
        tgt = (2 - A[u, u2]) - tri - cc
        terms = []
        const = 0
        for wi in range(60):
            p, q = inc(wi, u), inc(wi, u2)
            if isinstance(p, int) and isinstance(q, int):
                const += p * q
            elif isinstance(p, int):
                if p: terms.append(q)
            elif isinstance(q, int):
                if q: terms.append(p)
            else:
                z = m.NewBoolVar(""); m.AddMultiplicationEquality(z, [p, q]); terms.append(z)
        if tgt - const < 0:
            return "INFEASIBLE(trivial)", None
        m.Add(sum(terms) == tgt - const)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = workers
    st = s.Solve(m)
    return s.StatusName(st), (s if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None)


if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    ntr = int(sys.argv[2]) if len(sys.argv) > 2 else 5; tl = float(sys.argv[3]) if len(sys.argv) > 3 else 120
    for i in range(ntr):
        data, A = rand_C(rng)
        t = time.time(); st, _ = column_model(A, tl=tl)
        print("random C", i, "column design:", st, round(time.time() - t, 1), "s", flush=True)
