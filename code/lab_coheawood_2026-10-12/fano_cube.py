"""C1, lab session, 2026-10-12. The co-Heawood branch (two 22-cocliques meeting in 15 points = an integral
(-4)-eigenvector of norm 14) of a hypothetical srg(99,14,1,2), WITHOUT any hypothesis on the rank modulo 7, cut
into 33 508 cases by the exact catalogue of bases of work/c1_cost37_2026-10-09/fano37.c.

One case ("cube") = one orbit of bases: the simple cubic graph on the ten boundary neighbours B0 of the core point
x_0 whose 15 edges are the 15 far vertices. A cube fixes
  * the 150 pairs B0 - far (this also names the far vertices: no symmetry of the far set is left),
  * the perfect matching inside N(x) for every core point x (three edges among the six "twin" vertices; the eight
    matchings are one orbit under the swaps of the twins, which act freely, so a standard one is fixed in every row;
    the base catalogue uses the same standard matching in row 0).
Everything else (the triples of the 60 other boundary vertices and the 2415 pairs boundary - boundary) is left to
the solver, with the whole srg(99,14,1,2) encoded (srg_core_sat.encode: every degree, every pair of vertices).
Redundant cardinalities added to help propagation (all are consequences of the equations, see the note):
  * a boundary vertex has 3 far neighbours; a far vertex has 2 neighbours in every row and in every column;
  * a boundary vertex in cell (x', y') has 2 - [x in block y'] neighbours in the row x != x' and
    2 - [x' in block y] neighbours in the column y != y'; in its own column it has no neighbour if it is single,
    one neighbour (not its twin) if it is double.

python fano_cube.py <bases_orbits.txt> <index> <tmp dir> <seconds> [plain]
"plain": no redundant cardinality (the cube and the matchings only).     One process (cadical), below 2 GB."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "c1_cores_sat_2026-10-09"))
import srg_core_sat
from srg_core_sat import CNF, encode, solve, exactly, model_graph, check_model
# the solver moved on the lab PC since 09/10 (Desktop/c1-codex -> Desktop/Recherche_Conway/c1-codex)
srg_core_sat.CADICAL = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")

LINES = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]


def build(edges):
    n = 99; X = list(range(7)); Y = list(range(7, 14)); F = list(range(14, 29))
    inc = [[x not in LINES[y] for y in range(7)] for x in range(7)]
    E = [[None] * n for _ in range(n)]
    def fix(u, v, val):
        assert E[u][v] is None or E[u][v] == val
        E[u][v] = E[v][u] = val
    for x in range(7):
        for y in range(7): fix(X[x], Y[y], inc[x][y])
    for a in range(29):
        for b in range(a + 1, 29):
            if E[a][b] is None: fix(a, b, False)
    cellv = {}; B = []
    for x in range(7):
        for y in range(7):
            ids = []
            for _ in range(1 if inc[x][y] else 2):
                o = 29 + len(B); B.append((x, y)); ids.append(o)
                for a in range(14): fix(o, a, a == X[x] or a == Y[y])
            cellv[(x, y)] = ids
    assert len(B) == 70
    row = [[o for o in range(29, 99) if B[o - 29][0] == x] for x in range(7)]
    col = [[o for o in range(29, 99) if B[o - 29][1] == y] for y in range(7)]
    # the matching inside every row: twins (a,a'), (b,b'), (c,c') of the three lines through x, edges a-b, a'-c, b'-c'
    for x in range(7):
        dl = [y for y in range(7) if not inc[x][y]]; assert len(dl) == 3
        (a, a2), (b, b2), (c, c2) = [cellv[(x, y)] for y in dl]
        match = {(a, b), (a2, c), (b2, c2)}
        for i, u in enumerate(row[x]):
            for v in row[x][i + 1:]: fix(u, v, (u, v) in match or (v, u) in match)
    # positions 0..9 of the catalogue on the row of x_0: the four singles (lines not through 0, increasing), then the twins
    pos = [cellv[(0, y)][0] for y in range(7) if inc[0][y]]
    for y in range(7):
        if not inc[0][y]: pos += cellv[(0, y)]
    assert len(pos) == 10
    for (p, q) in ((4, 6), (5, 8), (7, 9)): assert E[pos[p]][pos[q]] is True
    for k, (p, q) in enumerate(edges):
        for t in range(10): fix(pos[t], F[k], t == p or t == q)
    return n, E, X, Y, F, B, inc, row, col, cellv


def main():
    lines = open(sys.argv[1]).read().split("\n"); idx = int(sys.argv[2]); tmp = sys.argv[3]; seconds = int(sys.argv[4])
    plain = len(sys.argv) > 5
    w = [int(t) for t in lines[idx].split()]; size = w[0]; edges = [(w[1 + 2 * k], w[2 + 2 * k]) for k in range(15)]
    t0 = time.time()
    n, E, X, Y, F, B, inc, row, col, cellv = build(edges)
    cnf, V = encode(n, 14, 1, 2, E)
    base_vars, base_clauses = cnf.nv, len(cnf.cl)
    if not plain:
        for o in range(29, 99): exactly(cnf, [V[o][f] for f in F], 3)
        for f in F:
            for x in range(7): exactly(cnf, [V[f][o] for o in row[x]], 2)
            for y in range(7): exactly(cnf, [V[f][o] for o in col[y]], 2)
        for o in range(29, 99):
            x1, y1 = B[o - 29]
            for x in range(7):
                if x != x1: exactly(cnf, [V[o][u] for u in row[x]], 2 - (1 if inc[x][y1] else 0))
            for y in range(7):
                if y != y1: exactly(cnf, [V[o][u] for u in col[y]], 2 - (1 if inc[x1][y] else 0))
            own = [u for u in col[y1] if u != o and B[u - 29] != (x1, y1)]
            exactly(cnf, [V[o][u] for u in own], 0 if inc[x1][y1] else 1)
    free = sum(1 for u in range(n) for v in range(u + 1, n) if E[u][v] is None)
    print("base %d (orbit of %d labelled bases): %s" % (idx, size, " ".join("%d-%d" % e for e in edges)))
    print("instance: %d undetermined pairs, %d variables, %d clauses (%d, %d before the redundant cardinalities), built in %.0f s"
          % (free, cnf.nv, len(cnf.cl), base_vars, base_clauses, time.time() - t0), flush=True)
    st, model, dt = solve(cnf, seconds, os.path.join(tmp, "cube_%d.cnf" % idx))
    print("cadical: %s after %.0f s" % (st, dt), flush=True)
    if st == "SAT":
        A = model_graph(V, model); ok = check_model(A, 14, 1, 2)
        print("model is an srg(99,14,1,2):", ok)
        with open(os.path.join(tmp, "cube_%d_model.txt" % idx), "w") as f:
            for u in range(n): f.write("".join("1" if A[u][v] else "0" for v in range(n)) + "\n")


if __name__ == "__main__":
    main()
