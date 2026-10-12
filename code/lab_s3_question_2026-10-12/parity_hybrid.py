"""Lab session, 2026-10-12. Complete parity skeleton problem on BH (hybrid encoding of full_hybrid.py) PLUS the global
parity constraints, written explicitly because resolution cannot derive them.

PARITY LEMMA (hand; checked numerically below). For a non-adjacent pair p, the number of negative edges in its bundle
(the 12 edges x-z, z-y) has the parity of its number of odd paths, so  [p is split] = L_p(eps) := sum of eps over the
bundle. Let v be non-isotropic, d isotropic with B(d, v) = 0, u = d + q(v) v, c in F_3, and
      W(v, u, c) = { {x, x + v} : B(x, u) = c }      (27 pairs).
Then the sum of the bundles of W, as a set of edges modulo 2, is a sum of lines; as eps is even on the lines, the number
of split pairs of W is even: W(v, u, c) contains an ODD number of flat pairs (at least one).
(For the whole direction, 81 pairs, this is the argument of Cesarz and Williford, arXiv:2610.05420, who prove that no
signing of BH has all pairs split.) There are 30 directions x 8 vectors u x 3 layers = 720 families.

python parity_hybrid.py <tmp dir> <seconds> <test> [noparity]
  tests: nontrivial | typeB | typeA | split | noflatP | flatpair | lineF1 | lineF3 | rect | six | allsplit
  noparity: the same without the parity constraints (for comparison)
Memory: cadical on about 75 000 variables, 460 000 clauses."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid


def families():
    fams = []
    nonis = [v for v in V if q(v) != 0]; seen = set()
    for v in nonis:
        if neg(v) in seen: continue
        seen.add(v)
        for d in S:
            if Bf(d, v) != 0: continue
            u = add(d, tuple((q(v) * t) % 3 for t in v))
            for c in range(3):
                fams.append([key(I[x], I[add(x, v)]) for x in V if Bf(x, u) == c])
    return fams


def check_families(fams):
    """sum over W of the bundles = a sum of lines (mod 2)"""
    edges = [(i, j) for i in range(n) for j in sorted(nbs[i]) if i < j]; eidx = {e: k for k, e in enumerate(edges)}
    line_of = {}
    for (i, j) in edges: line_of[(i, j)] = tuple(sorted((i, j, next(iter(nbs[i] & nbs[j])))))
    for W in fams:
        assert len(W) == 27 and len(set(W)) == 27
        cnt = {}
        for (a, b) in W:
            for z in CN[(a, b)]:
                for e in (key(a, z), key(z, b)): cnt[e] = cnt.get(e, 0) ^ 1
        odd = {e for e, t in cnt.items() if t}
        for e in odd:                                   # every odd edge comes with its whole line
            t = line_of[e]
            assert all(key(t[i], t[j]) in odd for i in range(3) for j in range(i + 1, 3)), "not a sum of lines"
    return True


if __name__ == "__main__":
    tmp, tl, test = sys.argv[1], float(sys.argv[2]), sys.argv[3]; noparity = len(sys.argv) > 4
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    opts = [test] if test in ("typeB", "typeA", "split", "rect", "six") else []
    nv, cl, ev, xs = full_hybrid.build(opts)
    nvv = [nv]
    def new(): nvv[0] += 1; return nvv[0]
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
    nfam = 0
    if not noparity:
        fams = families(); assert check_families(fams); nfam = len(fams)
        for W in fams:                                  # XOR of the 27 flat variables = 1, as a chain
            acc = xs[W[0]][0]
            for p in W[1:]:
                t = new(); a, b = acc, xs[p][0]
                cl += [[-a, -b, -t], [a, b, -t], [a, -b, t], [-a, b, t]]
                acc = t
            cl.append([acc])
    path = os.path.join(tmp, "parh_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nvv[0], len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("%s, %d parity families (checked): %s (%.1f s; %d variables, %d clauses)" % (test, nfam, res, time.time() - t0, nvv[0], len(cl)), flush=True)
    if res == "SAT":
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        types = {}
        for k, vs in xs.items():
            s = [i for i in range(11) if vs[i] in model][0]; t = state_type(k[0], k[1], s); types[t] = types.get(t, 0) + 1
        print("  pair types: %s" % types)
        if types.get("flat", 0) != len(xs):
            edges = sorted(ev); open(os.path.join(tmp, "skeleton_parity_%s.txt" % test), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
    try: os.remove(path)
    except OSError: pass
