"""Lab session, 2026-10-12. Complete parity skeleton problem on BH: hybrid encoding of full_hybrid.py (edges + states of
the pairs) PLUS an explicit GRID LAYER, so that the solver can reason on the curvature of the grids:

  one variable per grid square (3645 = 405 grids x 9), equal to the sum of its four edges;
  in every grid, for each pair of rows the three squares have even sum, and the same for each pair of columns
      (the 16 curvatures: flat, rectangle, six);
  for every pair, the state separates a grid pair iff the corresponding grid square is odd, and the number of odd grid
      squares on the pair is 0, 1 or 3 (flat, type B, type A);
  option cubes: for three independent isotropic directions the six faces of every cube have even sum.
The global parity lemma of parity_hybrid.py is a consequence of the row relations, so it is not added here.

python full_grid.py <tmp dir> <seconds> <test> [cubes]
  tests: nontrivial | typeB | typeA | split | flatpair | lineF1 | lineF3 | noflatP | rect | six | allsplit
Memory: cadical on about 60 000 variables and 600 000 clauses (900 000 with the cubes), under 1 GB."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid


def add_grid_layer(nv, cl, ev, xs, cubes):
    nvv = [nv]
    def new(): nvv[0] += 1; return nvv[0]
    E = lambda a, b: ev[key(a, b)]
    def xor_clauses(vs, rhs):
        m = len(vs)
        for bits in itertools.product((0, 1), repeat=m):
            if sum(bits) % 2 != rhs: cl.append([vs[i] * (-1 if bits[i] else 1) for i in range(m)])
    sq = {}
    for (a, b), c in CN.items():
        done = set(); gs = []
        for z in c:
            if z in done: continue
            z2 = gridpartner(a, b, z); done |= {z, z2}
            k = frozenset((a, b, z, z2))
            if k not in sq:
                v = new(); sq[k] = v
                xor_clauses([v, E(a, z), E(z, b), E(b, z2), E(z2, a)], 0)
            g = sq[k]; gs.append(g)
            vs = xs[(a, b)]; iz, iz2 = c.index(z), c.index(z2)
            for s in range(11):
                cl.append([-vs[s], g] if ((MASKS[s] >> iz) ^ (MASKS[s] >> iz2)) & 1 else [-vs[s], -g])
        for g1, g2 in itertools.combinations(gs, 2):
            g3 = [g for g in gs if g not in (g1, g2)][0]; cl.append([-g1, -g2, g3])
        cl.append([xs[(a, b)][0]] + gs)                           # split => some odd grid square
    assert len(sq) == 3645
    # grids: pairs of isotropic directions
    ngrid = 0
    for d1, d2 in itertools.combinations(ISO, 2):
        seen = set()
        for x in V:
            pts = frozenset(I[tuple((x[t] + i * d1[t] + j * d2[t]) % 3 for t in range(4))] for i in range(3) for j in range(3))
            if pts in seen: continue
            seen.add(pts); ngrid += 1
            pt = lambda i, j: I[tuple((x[t] + i * d1[t] + j * d2[t]) % 3 for t in range(4))]
            S2 = {}
            for i1, i2 in itertools.combinations(range(3), 2):
                for j1, j2 in itertools.combinations(range(3), 2):
                    S2[((i1, i2), (j1, j2))] = sq[frozenset((pt(i1, j1), pt(i2, j1), pt(i2, j2), pt(i1, j2)))]
            pr = list(itertools.combinations(range(3), 2))
            for r in pr: xor_clauses([S2[(r, c2)] for c2 in pr], 0)
            for c2 in pr: xor_clauses([S2[(r, c2)] for r in pr], 0)
    assert ngrid == 405
    ncube = 0
    if cubes:
        for d1, d2, d3 in itertools.combinations(ISO, 3):
            for x in V:
                p = lambda i, j, k: I[tuple((x[t] + i * d1[t] + j * d2[t] + k * d3[t]) % 3 for t in range(4))]
                faces = [frozenset((p(0, 0, 0), p(1, 0, 0), p(1, 1, 0), p(0, 1, 0))), frozenset((p(0, 0, 1), p(1, 0, 1), p(1, 1, 1), p(0, 1, 1))),
                         frozenset((p(0, 0, 0), p(1, 0, 0), p(1, 0, 1), p(0, 0, 1))), frozenset((p(0, 1, 0), p(1, 1, 0), p(1, 1, 1), p(0, 1, 1))),
                         frozenset((p(0, 0, 0), p(0, 1, 0), p(0, 1, 1), p(0, 0, 1))), frozenset((p(1, 0, 0), p(1, 1, 0), p(1, 1, 1), p(1, 0, 1)))]
                xor_clauses([sq[f] for f in faces], 0); ncube += 1
    return nvv[0], sq, ncube


if __name__ == "__main__":
    tmp, tl, test = sys.argv[1], float(sys.argv[2]), sys.argv[3]; cubes = "cubes" in sys.argv[4:]
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    opts = [test] if test in ("typeB", "typeA", "split", "rect", "six") else []
    nv, cl, ev, xs = full_hybrid.build(opts)
    P = 0; some_split = [-vs[0] for vs in xs.values()]
    R = [r for r in range(n) if r != P and r not in nbs[P]][0]; R2 = I[neg(V[R])]
    if test == "nontrivial": cl.append(some_split)
    elif test == "noflatP":
        for k in xs:
            if P in k: cl.append([-xs[k][0]])
    elif test == "allsplit":
        for vs in xs.values(): cl.append([-vs[0]])
    elif test == "flatpair": cl += [[xs[key(P, R)][0]], some_split]
    elif test == "lineF3": cl += [[xs[key(P, R)][0]], [xs[key(P, R2)][0]], [xs[key(R, R2)][0]], some_split]
    elif test == "lineF1": cl += [[xs[key(P, R)][0]], [-xs[key(P, R2)][0]], [-xs[key(R, R2)][0]]]
    nv2, sq, ncube = add_grid_layer(nv, cl, ev, xs, cubes)
    path = os.path.join(tmp, "fgrid_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv2, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("%s with the grid layer%s: %s (%.1f s; %d variables, %d clauses)" % (test, " and %d cubes" % ncube if cubes else "", res, time.time() - t0, nv2, len(cl)), flush=True)
    if res == "SAT":
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        types = {}
        for k, vs in xs.items():
            s = [i for i in range(11) if vs[i] in model][0]; t = state_type(k[0], k[1], s); types[t] = types.get(t, 0) + 1
        print("  pair types: %s" % types)
        if types.get("flat", 0) != len(xs):
            edges = sorted(ev); open(os.path.join(tmp, "skeleton_grid_%s.txt" % test), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
    try: os.remove(path)
    except OSError: pass
