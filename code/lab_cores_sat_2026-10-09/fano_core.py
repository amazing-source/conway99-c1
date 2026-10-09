"""C1, lab session, 2026-10-09. Does an srg(99,14,1,2) contain an integral (-4)-eigenvector of norm 14?

Such a vector is 1_X - 1_Y with X, Y independent 7-sets whose bipartite graph is the 2-(7,4,2) biplane (x ~ y iff the
point x is not on the Fano line y). Everything it forces (hand derivation, section 'Fano world' of the note):
  * an outside vertex has the same number t of neighbours in X and in Y, t <= 1;
  * 70 'boundary' vertices with t = 1: one for each adjacent pair (x, y) (the third point of the line xy) and two
    for each non-adjacent pair (their two common neighbours);
  * 15 'far' vertices with t = 0, pairwise non-adjacent, each adjacent to 14 boundary vertices; every boundary
    vertex has exactly 3 far neighbours (so X + far and Y + far are two 22-cocliques meeting in 15 points).
Only the last item is not imposed below as a fixed adjacency: the far vertices are fixed pairwise non-adjacent and
non-adjacent to X and Y (which is forced), and the solver decides the 1050 pairs boundary-far and the 2415 pairs
boundary-boundary. Symmetry breaking: the 15 far columns of the incidence matrix boundary x far in lexicographic
order, and the two twins of each non-adjacent pair (x, y) in lexicographic order of their rows.

python fano_core.py <tmp dir> <seconds> [nosym]        One process (cadical), below 2 GB."""
import sys, os, time
from srg_core_sat import CNF, encode, solve, exactly, model_graph, check_model

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]


def build():
    n = 99; X = list(range(7)); Y = list(range(7, 14)); F = list(range(14, 29)); B = []
    inc = [[x not in LINES[y] for y in range(7)] for x in range(7)]
    assert all(sum(r) == 4 for r in inc) and all(sum(inc[x][y] for x in range(7)) == 4 for y in range(7))
    E = [[None] * n for _ in range(n)]
    def fix(u, v, val): E[u][v] = E[v][u] = val
    for a in range(29):
        for b in range(a + 1, 29): fix(a, b, False)
    for x in range(7):
        for y in range(7): fix(X[x], Y[y], inc[x][y])
    twins = []
    for x in range(7):
        for y in range(7):
            ids = []
            for _ in range(1 if inc[x][y] else 2):
                o = 29 + len(B); B.append((x, y)); ids.append(o)
                for a in range(14): fix(o, a, a == X[x] or a == Y[y])
            if len(ids) == 2: twins.append(tuple(ids))
    assert len(B) == 70
    return n, E, X, Y, F, list(range(29, 99)), B, twins


def lex_ge(cnf, a, b):
    """a >=_lex b for two equal-length lists of literals"""
    eq = True
    for x, y in zip(a, b):
        # under eq: x >= y, i.e. not (not x and y)
        if eq is True: cnf.add(x, -y)
        else: cnf.add(-eq, x, -y)
        ne = cnf.new()                       # ne = eq and (x == y)   (one direction is enough: eq & x==y -> ne)
        if eq is True: cnf.add(-x, -y, ne); cnf.add(x, y, ne)
        else: cnf.add(-eq, -x, -y, ne); cnf.add(-eq, x, y, ne)
        eq = ne


if __name__ == "__main__":
    tmp = sys.argv[1]; seconds = int(sys.argv[2]); nosym = len(sys.argv) > 3
    t0 = time.time()
    n, E, X, Y, F, Bv, B, twins = build()
    cnf, V = encode(n, 14, 1, 2, E)
    base_vars, base_clauses = cnf.nv, len(cnf.cl)
    for o in Bv: exactly(cnf, [V[o][f] for f in F], 3)                         # redundant: three far neighbours
    if not nosym:
        for i in range(14): lex_ge(cnf, [V[o][F[i]] for o in Bv], [V[o][F[i + 1]] for o in Bv])
        for o1, o2 in twins: lex_ge(cnf, [V[o1][f] for f in F], [V[o2][f] for f in F])
    print("instance: %d variables and %d clauses (%d and %d before the redundant and symmetry clauses), built in %.0f s"
          % (cnf.nv, len(cnf.cl), base_vars, base_clauses, time.time() - t0), flush=True)
    st, model, dt = solve(cnf, seconds, os.path.join(tmp, "fano.cnf"))
    print("cadical: %s after %.0f s" % (st, dt), flush=True)
    if st == "SAT":
        A = model_graph(V, model); ok = check_model(A, 14, 1, 2)
        print("model is an srg(99,14,1,2):", ok)
        if ok:
            with open(os.path.join(tmp, "fano_model.txt"), "w") as f:
                for u in range(n): f.write("".join("1" if A[u][v] else "0" for v in range(n)) + "\n")
