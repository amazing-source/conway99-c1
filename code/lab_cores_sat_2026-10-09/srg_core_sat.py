"""C1, lab session, 2026-10-09. SAT encoding of 'a strongly regular graph (n, k, lambda, mu) containing a prescribed
partial adjacency' (a core with everything it forces), for the short eigenvector supports of srg(99,14,1,2).

Encoding. One variable per undetermined pair. For every pair {u, v} the number of common neighbours is lambda or mu:
    (number of w with e_uw and e_vw) + (mu - lambda) e_uv = mu,
written as an exact cardinality over the products e_uw & e_vw (a product is a constant, a literal or a new variable)
and, when e_uv is undetermined and mu = lambda + 1, the literal e_uv itself. Every vertex has degree k.
Cardinalities by sequential counters with full equivalences. Nothing else is assumed: a model is checked to be an
srg by `check_model`, an UNSAT answer means no srg contains the prescribed part (as far as the solver is trusted;
cadical can write a proof, not requested here).

Modules: CNF, encode(n, k, lam, mu, E) -> (cnf, var_of_pair), solve(cnf, seconds), controls().
One process; memory of the solver below 2 GB for the instances here."""
import subprocess, sys, time, os, itertools

CADICAL = "C:/home/researcher/Desktop/c1-codex/tools/win64/cadical.exe"


class CNF:
    def __init__(self): self.nv = 0; self.cl = []; self.empty = False
    def new(self): self.nv += 1; return self.nv
    def add(self, *lits):
        if not lits: self.empty = True
        self.cl.append(lits)
    def write(self, path):
        with open(path, "w") as f:
            f.write("p cnf %d %d\n" % (self.nv, len(self.cl)))
            f.write("".join(" ".join(map(str, c)) + " 0\n" for c in self.cl))


def b_and(cnf, a, b, cache):
    """a, b in {True, False, literal}; returns the same kind of value for a & b"""
    if a is False or b is False: return False
    if a is True: return b
    if b is True: return a
    if a == b: return a
    if a == -b: return False
    key = (a, b) if a < b else (b, a)
    p = cache.get(key)
    if p is None:
        p = cnf.new(); cache[key] = p
        cnf.add(-p, a); cnf.add(-p, b); cnf.add(p, -a, -b)
    return p


def exactly(cnf, vals, K):
    """exactly K of vals are true; vals in {True, False, literal}"""
    K -= sum(1 for v in vals if v is True)
    lits = [v for v in vals if v is not True and v is not False]
    n = len(lits)
    if K < 0 or K > n: cnf.add(); return
    if K == 0:
        for l in lits: cnf.add(-l)
        return
    if K == n:
        for l in lits: cnf.add(l)
        return
    prev = [True] + [False] * (K + 1)          # prev[j]: at least j of the literals read so far
    for x in lits:
        cur = [True]
        for j in range(1, K + 2):
            a, b = prev[j], prev[j - 1]        # cur_j = a | (x & b)
            if b is False: cur.append(a); continue
            if a is True: cur.append(True); continue
            if a is False and b is True: cur.append(x); continue
            t = cnf.new()
            if a is not False: cnf.add(-a, t)
            if b is True: cnf.add(-x, t)
            else: cnf.add(-x, -b, t)
            # t -> a | x  and  t -> a | b
            c1 = [-t, x] + ([a] if a is not False else []); cnf.add(*c1)
            if b is not True:
                c2 = [-t, b] + ([a] if a is not False else []); cnf.add(*c2)
            cur.append(t)
        prev = cur
    if prev[K] is False: cnf.add()
    elif prev[K] is not True: cnf.add(prev[K])
    if prev[K + 1] is True: cnf.add()
    elif prev[K + 1] is not False: cnf.add(-prev[K + 1])


def encode(n, k, lam, mu, E):
    """E[u][v] (symmetric) in {True, False, None}; None = undetermined. Returns cnf and the matrix of values."""
    cnf = CNF(); V = [[False] * n for _ in range(n)]
    for u in range(n):
        for v in range(u + 1, n):
            x = E[u][v]
            if x is None: x = cnf.new()
            V[u][v] = V[v][u] = x
    cache = {}
    for u in range(n): exactly(cnf, [V[u][w] for w in range(n) if w != u], k)
    assert mu - lam in (0, 1)
    for u in range(n):
        for v in range(u + 1, n):
            terms = [b_and(cnf, V[u][w], V[v][w], cache) for w in range(n) if w != u and w != v]
            e = V[u][v]
            if e is True: exactly(cnf, terms, lam)
            elif e is False: exactly(cnf, terms, mu)
            elif mu == lam + 1: exactly(cnf, terms + [e], mu)
            else: exactly(cnf, terms, mu)
    return cnf, V


def solve(cnf, seconds, path, extra=()):
    if cnf.empty: return "UNSAT (empty clause while encoding)", None, 0.0
    cnf.write(path); t0 = time.time()
    try:
        r = subprocess.run([CADICAL, "-q", path] + list(extra), capture_output=True, text=True, timeout=seconds)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", None, time.time() - t0
    out = r.stdout; dt = time.time() - t0
    if "s UNSATISFIABLE" in out: return "UNSAT", None, dt
    if "s SATISFIABLE" in out:
        model = set()
        for line in out.split("\n"):
            if line.startswith("v "): model.update(int(t) for t in line[2:].split() if int(t) > 0)
        return "SAT", model, dt
    return "UNKNOWN (%s)" % out[-200:], None, dt


def model_graph(V, model):
    n = len(V)
    return [[(V[u][v] is True) or (V[u][v] is not False and V[u][v] in model) if u != v else False for v in range(n)] for u in range(n)]


def check_model(A, k, lam, mu):
    n = len(A)
    for u in range(n):
        if sum(A[u]) != k: return False
        for v in range(u + 1, n):
            c = sum(1 for w in range(n) if A[u][w] and A[v][w])
            if c != (lam if A[u][v] else mu): return False
    return True


def controls(tmp):
    """positive and negative controls of the encoder on srg(9,4,1,2) and srg(16,6,2,2), srg(10,3,0,1)"""
    res = []
    E = [[None] * 9 for _ in range(9)]
    def fix(u, v, x): E[u][v] = E[v][u] = x
    for u, v in ((0, 1), (1, 2), (2, 3), (3, 0)): fix(u, v, True)
    fix(0, 2, False); fix(1, 3, False)
    cnf, V = encode(9, 4, 1, 2, E); st, model, dt = solve(cnf, 60, os.path.join(tmp, "c1.cnf"))
    ok = st == "SAT" and check_model(model_graph(V, model), 4, 1, 2)
    res.append("rook graph with an induced 4-cycle fixed: %s, model is an srg(9,4,1,2): %s" % (st, ok))
    E = [[None] * 9 for _ in range(9)]
    for u, v in ((0, 1), (0, 2), (1, 2), (0, 3), (1, 3)): E[u][v] = E[v][u] = True      # an edge in two triangles
    cnf, V = encode(9, 4, 1, 2, E); st, model, dt = solve(cnf, 60, os.path.join(tmp, "c2.cnf"))
    res.append("srg(9,4,1,2) with an edge in two triangles fixed: %s (expected UNSAT)" % st)
    E = [[None] * 10 for _ in range(10)]
    cnf, V = encode(10, 3, 0, 1, E); st, model, dt = solve(cnf, 60, os.path.join(tmp, "c3.cnf"))
    ok = st == "SAT" and check_model(model_graph(V, model), 3, 0, 1)
    res.append("srg(10,3,0,1), nothing fixed: %s, model is the Petersen graph parameters: %s" % (st, ok))
    E = [[None] * 16 for _ in range(16)]
    cnf, V = encode(16, 6, 2, 2, E); st, model, dt = solve(cnf, 60, os.path.join(tmp, "c4.cnf"))
    ok = st == "SAT" and check_model(model_graph(V, model), 6, 2, 2)
    res.append("srg(16,6,2,2), nothing fixed: %s, model checked: %s" % (st, ok))
    E = [[None] * 21 for _ in range(21)]
    cnf, V = encode(21, 10, 4, 5, E); st, model, dt = solve(cnf, 120, os.path.join(tmp, "c5.cnf"))
    res.append("srg(21,10,4,5) (does not exist: conference graph on 21 points), nothing fixed: %s in %.1f s" % (st, dt))
    return res


if __name__ == "__main__":
    tmp = sys.argv[1]
    for line in controls(tmp): print(line, flush=True)
