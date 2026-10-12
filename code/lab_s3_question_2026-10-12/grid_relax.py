"""Lab session, 2026-10-12. The GRID-LEVEL RELAXATION of the parity skeleton problem.

Unknown: the set O of odd grid squares (3645 grid squares = 405 grids x 9). Necessary conditions for a skeleton:
  (R) in every grid, each pair of rows and each pair of columns carries an even number of odd squares;
  (K) for three independent isotropic directions, the six faces of every cube carry an even number of odd squares;
  (D) every non-adjacent pair is a diagonal of 0, 1 or 3 odd grid squares (never exactly 2) - flat, type B, type A.
A non-trivial skeleton has an odd grid square. The non-grid squares are ignored here.
Graph picture: the pairs are the 2430 vertices of a cubic graph G whose 3645 edges are the grid squares (a square
joins its two diagonals); O is a set of edges with all degrees in {0, 1, 3}.

1. rank of the relations (R) and (R)+(K) on F_2^3645, to be compared with 3645 - 460 (the codimension of the space of
   the curvatures of the line-even edge functions);
2. cadical on (R) + (D) + [K] + "a given square is odd" (Aut(BH) is transitive on the grid squares: checked by the
   orbit of one square under translations and the stabiliser of a point... see the note; here simply every square of
   one grid is tried when the option all9 is given).
python grid_relax.py <tmp dir> <seconds> [nocubes] [rankonly]"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
tmp, tl = sys.argv[1], float(sys.argv[2]); opts = sys.argv[3:]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
sq = {}
def S(*pts):
    k = frozenset(pts)
    if k not in sq: sq[k] = len(sq) + 1
    return sq[k]
for (a, b), c in sorted(CN.items()):
    for z in c: S(a, b, z, gridpartner(a, b, z))
assert len(sq) == 3645
rel = []                                                  # XOR relations (lists of variables, sum = 0)
for d1, d2 in itertools.combinations(ISO, 2):
    seen = set()
    for x in V:
        pt = lambda i, j: I[tuple((x[t] + i * d1[t] + j * d2[t]) % 3 for t in range(4))]
        pts = frozenset(pt(i, j) for i in range(3) for j in range(3))
        if pts in seen: continue
        seen.add(pts); pr = list(itertools.combinations(range(3), 2))
        G = {(r, c): S(pt(r[0], c[0]), pt(r[1], c[0]), pt(r[1], c[1]), pt(r[0], c[1])) for r in pr for c in pr}
        for r in pr: rel.append([G[(r, c)] for c in pr])
        for c in pr: rel.append([G[(r, c)] for r in pr])
nR = len(rel)
cubes = []
for d1, d2, d3 in itertools.combinations(ISO, 3):
    for x in V:
        p = lambda i, j, k: I[tuple((x[t] + i * d1[t] + j * d2[t] + k * d3[t]) % 3 for t in range(4))]
        cubes.append([S(p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0)), S(p(0, 0, 1), p(1, 0, 1), p(1, 1, 1), p(0, 1, 1)),
                      S(p(0, 0, 0), p(1, 0, 0), p(1, 0, 1), p(0, 0, 1)), S(p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1)),
                      S(p(0, 0, 0), p(0, 1, 0), p(0, 1, 1), p(0, 0, 1)), S(p(1, 0, 0), p(1, 1, 0), p(1, 1, 1), p(1, 0, 1))])
def rank(rows):
    piv = {}; r = 0
    for vs in rows:
        v = 0
        for t in vs: v ^= 1 << t
        while v:
            b = v.bit_length() - 1
            if b in piv: v ^= piv[b]
            else: piv[b] = v; r += 1; break
    return r
rR = rank(rel); rRK = rank(rel + cubes)
print("rank of the row/column relations: %d; with the cube relations: %d; 3645 - 460 = %d" % (rR, rRK, 3645 - 460), flush=True)
print("dimension of the space of square patterns allowed by (R): %d, by (R)+(K): %d (the curvatures of edge functions: 460)" % (3645 - rR, 3645 - rRK), flush=True)
if "rankonly" in opts: sys.exit()
cl = []
def xor_clauses(vs, rhs):
    m = len(vs)
    for bits in itertools.product((0, 1), repeat=m):
        if sum(bits) % 2 != rhs: cl.append([vs[i] * (-1 if bits[i] else 1) for i in range(m)])
for vs in rel: xor_clauses(vs, 0)
if "nocubes" not in opts:
    for vs in cubes: xor_clauses(vs, 0)
for (a, b), c in CN.items():
    gs = sorted({S(a, b, z, gridpartner(a, b, z)) for z in c}); assert len(gs) == 3
    for g1, g2 in itertools.combinations(gs, 2):
        g3 = [g for g in gs if g not in (g1, g2)][0]; cl.append([-g1, -g2, g3])
cl.append([1])                                            # the first grid square is odd
path = os.path.join(tmp, "grelax_%d.cnf" % os.getpid())
with open(path, "w", newline="\n") as f:
    f.write("p cnf %d %d\n" % (len(sq), len(cl)))
    for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
t0 = time.time()
try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
except subprocess.TimeoutExpired: out = ""
res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
print("grid-level relaxation%s, one square odd: %s (%.1f s; %d variables, %d clauses)" % ("" if "nocubes" not in opts else " without the cubes", res, time.time() - t0, len(sq), len(cl)), flush=True)
if res == "SAT":
    model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
    deg = {}
    for (a, b), c in CN.items():
        gs = {S(a, b, z, gridpartner(a, b, z)) for z in c}; d = sum(1 for g in gs if g in model); deg[d] = deg.get(d, 0) + 1
    print("  odd squares: %d; pairs by number of odd grid squares: %s" % (len([v for v in model if v <= len(sq)]), sorted(deg.items())))
    open(os.path.join(tmp, "grid_relax_solution.txt"), "w").write(" ".join(str(v) for v in sorted(model)) + "\n")
try: os.remove(path)
except OSError: pass
