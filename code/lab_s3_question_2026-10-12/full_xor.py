"""Lab session, 2026-10-12. The COMPLETE parity skeleton problem on BH for a solver with native XOR constraints and
Gauss-Jordan elimination (CryptoMiniSat through pycryptosat). Same model as full_hybrid.py:

  edge variables e(x,y) (810; gauge: the edges at P = 0 and one edge of every far vertex are 0), even on the 270 lines;
  for every non-adjacent pair p = {x,y} with common neighbours z_0 < ... < z_5:
      rho_i = e(x,z_i) + e(z_i,y) + e(x,z_0) + e(z_0,y)   (i = 1..5; native XOR of five variables),
      exactly one state s (0 = flat, 1..10 = partitions 3+3), state s forces rho_i = bit i of its mask;
  redundant but useful for the linear algebra: flat_p + (sum of the 12 edges of the bundle of p) = 1
      (a pair is split iff its bundle has an odd number of negative edges), and, for the three grid squares of p,
      g_j = sum of the four edges of the square (j = 1..3), flat_p + g_1 + g_2 + g_3 = 1.

Why: the parity arguments (e.g. Cesarz and Williford, arXiv:2610.05420: no signing of BH with all pairs split) are
linear algebra over F_2 on the edge variables, out of reach of resolution but immediate for Gauss-Jordan.

python full_xor.py <seconds> [options]
  allsplit | noflatP | trivialP | typeB[=k] | typeA[=k] | split | rect | six      (as in full_hybrid.py / global_tests.py)
  nontrivial      some pair is split
  seed=<n>        random seed of the solver
The pycryptosat module is looked for in the directory given by the environment variable PYLIB (if set).
Memory: under 1 GB."""
import sys, os, time, itertools
if os.environ.get("PYLIB"): sys.path.insert(0, os.environ["PYLIB"])
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import pycryptosat


def build(opts, solver):
    nv = [0]
    def new(): nv[0] += 1; return nv[0]
    P = 0
    edges = [(i, j) for i in range(n) for j in sorted(nbs[i]) if i < j]; ev = {e: new() for e in edges}
    E = lambda a, b: ev[key(a, b)]
    far = [r for r in range(n) if r != P and r not in nbs[P]]
    for z in nbs[P]: solver.add_clause([-E(P, z)])
    for r in far: solver.add_clause([-E(r, CN[key(P, r)][0])])
    lines = sorted({tuple(sorted((i, j, next(iter(nbs[i] & nbs[j]))))) for (i, j) in edges})
    for t in lines: solver.add_xor_clause([E(t[0], t[1]), E(t[1], t[2]), E(t[0], t[2])], False)
    xs = {}
    for (a, b), c in CN.items():
        rho = [None]
        for i in range(1, 6):
            t = new(); rho.append(t)
            solver.add_xor_clause([t, E(a, c[i]), E(c[i], b), E(a, c[0]), E(c[0], b)], False)
        vs = [new() for _ in MASKS]; xs[(a, b)] = vs
        solver.add_clause(list(vs))
        for s, t in itertools.combinations(range(11), 2): solver.add_clause([-vs[s], -vs[t]])
        for s in range(11):
            for i in range(1, 6): solver.add_clause([-vs[s], rho[i] if (MASKS[s] >> i) & 1 else -rho[i]])
        # redundant linear relations
        bundle = [E(a, z) for z in c] + [E(z, b) for z in c]
        solver.add_xor_clause([vs[0]] + bundle, True)
        gs = []; seen = set()
        for z in c:
            if z in seen: continue
            z2 = gridpartner(a, b, z); seen |= {z, z2}
            g = new(); gs.append(g)
            solver.add_xor_clause([g, E(a, z), E(z, b), E(b, z2), E(z2, a)], False)
        solver.add_xor_clause([vs[0]] + gs, True)
        for g1, g2 in itertools.combinations(gs, 2):                 # never exactly two odd grid squares
            g3 = [g for g in gs if g not in (g1, g2)][0]
            solver.add_clause([-g1, -g2, g3])
    R0 = far[0]
    for o in opts:
        name, _, arg = o.partition("="); k = int(arg) if arg else 0
        if name in ("typeB", "typeA"):
            sts = [s for s in range(1, 11) if state_type(P, R0, s) == name[-1]]; solver.add_clause([xs[key(P, R0)][sts[k]]])
        elif name == "split": solver.add_clause([-xs[key(P, R0)][0]])
        elif name == "allsplit":
            for vs in xs.values(): solver.add_clause([-vs[0]])
        elif name == "noflatP":
            for kk in xs:
                if P in kk: solver.add_clause([-xs[kk][0]])
        elif name == "trivialP":
            for kk in xs:
                if P in kk: solver.add_clause([xs[kk][0]])
            solver.add_clause([-vs[0] for vs in xs.values()])
        elif name == "nontrivial": solver.add_clause([-vs[0] for vs in xs.values()])
        elif name in ("rect", "six"):
            a, ap = ISO[0], ISO[1]
            pt = lambda i, j: I[tuple((i * a[c] + j * ap[c]) % 3 for c in range(4))]
            for i1, i2 in itertools.combinations(range(3), 2):
                for j1, j2 in itertools.combinations(range(3), 2):
                    odd = (0 in (i1, i2) and 0 in (j1, j2)) if name == "rect" else ((3 - i1 - i2) != (3 - j1 - j2))
                    solver.add_xor_clause([E(pt(i1, j1), pt(i2, j1)), E(pt(i2, j1), pt(i2, j2)), E(pt(i2, j2), pt(i1, j2)), E(pt(i1, j2), pt(i1, j1))], bool(odd))
    return nv[0], ev, xs


if __name__ == "__main__":
    tl = float(sys.argv[1]); opts = sys.argv[2:]
    seed = next((int(o[5:]) for o in opts if o.startswith("seed=")), 0)
    solver = pycryptosat.Solver(threads=1, time_limit=tl, verbose=0)
    t0 = time.time(); nv, ev, xs = build(opts, solver)
    sat, sol = solver.solve()
    res = "SAT" if sat is True else "UNSAT" if sat is False else "NO DECISION"
    print("full problem with native XOR, options %s: %d variables: %s (%.1f s)" % (opts, nv, res, time.time() - t0), flush=True)
    if sat is True:
        types = {}
        for k, vs in xs.items():
            s = [i for i in range(11) if sol[vs[i]]][0]; t = state_type(k[0], k[1], s); types[t] = types.get(t, 0) + 1
        print("  pair types in the solution: %s" % types)
        edges = sorted(ev); out = "".join("1" if sol[ev[e]] else "0" for e in edges)
        if types.get("flat", 0) != len(xs):
            open(os.path.join(os.environ.get("OUTDIR", "."), "skeleton_found.txt"), "w").write(out + "\n"); print("  NON-TRIVIAL SKELETON written to skeleton_found.txt")
