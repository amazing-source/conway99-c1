"""Lab session, 2026-10-12. Direct global checks of the four lemma families used as redundant clauses in
full_ultimate.py. Each lemma says "in a non-trivial parity skeleton, at the vertex X, property Q holds". Here the
complete problem (hybrid encoding + grid layer + parity chains, NO lemma clause) is run with "some pair is split" and
"not Q at P = 0"; UNSAT confirms the lemma at P, hence at every vertex (Aut(BH) is transitive on vertices, and on the
arcs for (d)).
  a : no pair through P is of type B
  b : no inner pair of P is of type B
  c : no inner pair of P is of type A
  d : the 18 pairs {P, R} with R adjacent to a fixed neighbour u of P are flat
python lemma_checks.py <tmp dir> <seconds per check> [a b c d]"""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid, full_grid, parity_hybrid
tmp, tl = sys.argv[1], float(sys.argv[2]); which = sys.argv[3:] or ["a", "b", "c", "d"]
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
nv, base, ev, xs = full_hybrid.build([])
nv, sq, _ = full_grid.add_grid_layer(nv, base, ev, xs, False)
nvv = [nv]
def new(): nvv[0] += 1; return nvv[0]
for W in parity_hybrid.families():
    acc = xs[W[0]][0]
    for p in W[1:]:
        t = new(); a, b = acc, xs[p][0]
        base += [[-a, -b, -t], [a, b, -t], [a, -b, t], [-a, b, t]]
        acc = t
    base.append([acc])
base.append([-vs[0] for vs in xs.values()])                    # some pair is split
P = 0; farP = [r for r in range(n) if r != P and r not in nbs[P]]
inner = [(a, b) for a, b in itertools.combinations(sorted(nbs[P]), 2) if b not in nbs[a]]
typed = lambda a, b, t: [xs[key(a, b)][s] for s in range(1, 11) if state_type(a, b, s) == t]
extra = {
    "a": [[-l] for r in farP for l in typed(P, r, "B")],
    "b": [[-l] for (a, b) in inner for l in typed(a, b, "B")],
    "c": [[-l] for (a, b) in inner for l in typed(a, b, "A")],
    "d": [[xs[key(P, r)][0]] for r in nbs[sorted(nbs[P])[0]] if r != P and r not in nbs[P]],
}
label = {"a": "no pair of type B through P", "b": "no inner pair of type B at P", "c": "no inner pair of type A at P", "d": "the 18 pairs {P,R}, R ~ u, flat"}
for w in which:
    cl = base + extra[w]
    path = os.path.join(tmp, "lemchk_%d.cnf" % os.getpid())
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nvv[0], len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    t0 = time.time()
    try: out = subprocess.run([CAD, "-q", path], capture_output=True, text=True, timeout=tl).stdout
    except subprocess.TimeoutExpired: out = ""
    res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
    print("lemma (%s): a non-trivial skeleton with [%s]: %s (%.1f s)" % (w, label[w], res, time.time() - t0), flush=True)
    try: os.remove(path)
    except OSError: pass
