"""Lab session, 2026-10-12. The COMPLETE parity skeleton problem on BH, hybrid encoding: edge variables (the signing
itself, so that every relation between cycles is present) and state variables for every non-adjacent pair (for the
propagation; see local_lib.py for the states).

  edge e(x,y) in F_2, even on the 270 lines; gauge: all edges at P = 0 are 0, and for every far vertex R the edge to its
  first common neighbour with P is 0 (a spanning tree: no loss of generality);
  for every non-adjacent pair {x,y} with common neighbours z_0 < ... < z_5: pi_i = e(x,z_i) + e(z_i,y),
  rho_i = pi_i + pi_0; exactly one state s; state s forces rho_i = bit i of its mask.

python full_hybrid.py <tmp dir> <seconds> [options]
  typeB[=k]   the pair {P, far[0]} is in its k-th type B state (default k = 0)
  typeA[=k]   the pair {P, far[0]} is in its k-th type A state
  split       the pair {P, far[0]} is split
  rect / six  the grid <a, a'> through P has the rectangle curvature with special point P / a six curvature
  lemmas      add the clauses of the proven local lemma: a vertex with a split pair has a pair of type B
  out=<file>  keep the CNF under this name (in the tmp dir) instead of deleting it
Memory: cadical on about 55 000 variables and 400 000 clauses, well under 1 GB."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *

def build(opts):
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    P = 0
    edges = [(i, j) for i in range(n) for j in sorted(nbs[i]) if i < j]; ev = {e: new() for e in edges}
    E = lambda a, b: ev[key(a, b)]
    far = [r for r in range(n) if r != P and r not in nbs[P]]
    for z in nbs[P]: cl.append([-E(P, z)])
    for r in far: cl.append([-E(r, CN[key(P, r)][0])])
    def xor3(a, b, c, rhs):                         # a + b + c = rhs (mod 2)
        for bits in itertools.product((0, 1), repeat=3):
            if sum(bits) % 2 != rhs: cl.append([v * (-1 if bt else 1) for v, bt in zip((a, b, c), bits)])
    lines = sorted({tuple(sorted((i, j, next(iter(nbs[i] & nbs[j]))))) for (i, j) in edges})
    for t in lines: xor3(E(t[0], t[1]), E(t[1], t[2]), E(t[0], t[2]), 0)
    xs = {}
    for (a, b), c in CN.items():
        pi = []
        for z in c:
            t = new(); xor3(E(a, z), E(z, b), t, 0); pi.append(t)
        rho = [None]
        for i in range(1, 6):
            t = new(); xor3(pi[i], pi[0], t, 0); rho.append(t)
        vs = [new() for _ in MASKS]; xs[(a, b)] = vs
        cl.append(list(vs))
        for s, t in itertools.combinations(range(11), 2): cl.append([-vs[s], -vs[t]])
        for s in range(11):
            for i in range(1, 6): cl.append([-vs[s], rho[i] if (MASKS[s] >> i) & 1 else -rho[i]])
    R0 = far[0]
    for o in opts:
        name, _, arg = o.partition("="); k = int(arg) if arg else 0
        if name in ("typeB", "typeA"):
            sts = [s for s in range(1, 11) if state_type(P, R0, s) == name[-1]]; cl.append([xs[key(P, R0)][sts[k]]])
        elif name == "split": cl.append([-xs[key(P, R0)][0]])
        elif name in ("rect", "six"):
            a, ap = ISO[0], ISO[1]
            pt = lambda i, j: I[tuple((i * a[c] + j * ap[c]) % 3 for c in range(4))]
            for i1, i2 in itertools.combinations(range(3), 2):
                for j1, j2 in itertools.combinations(range(3), 2):
                    odd = (0 in (i1, i2) and 0 in (j1, j2)) if name == "rect" else ((3 - i1 - i2) != (3 - j1 - j2))
                    sq = [E(pt(i1, j1), pt(i2, j1)), E(pt(i2, j1), pt(i2, j2)), E(pt(i2, j2), pt(i1, j2)), E(pt(i1, j2), pt(i1, j1))]
                    t = new(); xor3(sq[0], sq[1], t, 0); xor3(sq[2], sq[3], t, 1 if odd else 0)
        elif name == "lemmas":
            for X in range(n):
                fx = [r for r in range(n) if r != X and r not in nbs[X]]
                bl = [xs[key(X, r)][s] for r in fx for s in range(1, 11) if state_type(X, r, s) == "B"]
                for r in fx:
                    for s in range(1, 11):
                        if state_type(X, r, s) == "A": cl.append([-xs[key(X, r)][s]] + bl)
    return nv[0], cl, ev, xs

if __name__ == "__main__":
    tmp, tl = sys.argv[1], float(sys.argv[2]); opts = sys.argv[3:]
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    nv, cl, ev, xs = build(opts)
    out_name = next((o[4:] for o in opts if o.startswith("out=")), None)
    path = os.path.join(tmp, out_name or ("full_%d.cnf" % os.getpid()))
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("full problem, options %s: %d variables, %d clauses: %s (%.1f s)" % (opts, nv, len(cl), res, time.time() - t0), flush=True)
    if res == "SAT":
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        types = {}
        for k, vs in xs.items():
            s = [i for i in range(11) if vs[i] in model][0]; t = state_type(k[0], k[1], s); types[t] = types.get(t, 0) + 1
        print("  pair types in the solution: %s" % types)
    if not out_name:
        try: os.remove(path)
        except OSError: pass
