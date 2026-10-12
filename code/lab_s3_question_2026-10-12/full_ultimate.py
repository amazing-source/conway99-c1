"""Lab session, 2026-10-12. The remaining question as ONE instance: "some pair of BH is of type B in a parity skeleton".

Reduction (NOTE_S3.md): a non-trivial parity skeleton has a pair of type B at every vertex. Aut(BH) is transitive on the
(ordered non-adjacent pair, type B state) triples (checked below by an orbit computation), so one may assume that the
pair {P, R0} is in one fixed type B state. UNSAT of this instance = every parity skeleton on BH is trivial.

Encoding: full_hybrid.py (810 edge variables, one-hot states of the 2430 pairs) with
  * the grid layer of full_grid.py (grid squares, row and column relations, optional cube relations),
  * the 720 parity chains of parity_hybrid.py,
  * the proven local lemmas as redundant clauses, at every vertex X:
      (a) X has a pair of type B;                       (C1 + C2 + D)
      (b) X has an inner pair of type B;                (C3 + D)
      (c) X has an inner pair of type A;                (C4 with (a))
      (d) for every neighbour u of X some pair {X, R}, R adjacent to u, is split.   (D, local form)
  * at P: some block outside Omega_25(R0) is of type B (C5).
The redundant clauses are consequences of the constraints in a non-trivial skeleton; they only help the search.

python full_ultimate.py <tmp dir> <seconds, 0 = only write the CNF> [cubes] [nolemmas] [noparity] [split] [out=<file>] [args for cadical ...]
  split: the cube is "the pair {P, R0} is split" (no lemma used at all; lemma clauses off)
Memory: cadical on about 80 000 variables and 1 000 000 clauses: under 2 GB."""
import sys, os, subprocess, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from local_lib import *
import full_hybrid, full_grid, parity_hybrid


def orbit_check():
    """Aut(BH) is transitive on (ordered non-adjacent pair, type B state): the stabiliser of (P, R0) is transitive on
    the six type B states of {P, R0}."""
    def mat_apply(M, v): return tuple(sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4))
    def mat_mul(A, B): return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(4)) % 3 for j in range(4)) for i in range(4))
    E4 = [tuple(int(i == j) for j in range(4)) for i in range(4)]; ident = tuple(E4)
    gens = [tuple(tuple((E4[j][i] - Bf(E4[j], w) * q(w) * w[i]) % 3 for j in range(4)) for i in range(4)) for w in V if q(w) != 0]
    gens.append(((1, 1, 0, 0), (1, 2, 0, 0), (0, 0, 1, 0), (0, 0, 0, 2)))
    group = {ident}; frontier = [ident]
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                k = mat_mul(h, g)
                if k not in group: group.add(k); new.append(k)
        frontier = new
    assert len(group) == 2880
    P = 0; R0 = [r for r in range(n) if r != P and r not in nbs[P]][0]; c = CN[key(P, R0)]
    stab = [g for g in group if I[mat_apply(g, V[R0])] == R0]; assert len(stab) == 48
    sB = [s for s in range(1, 11) if state_type(P, R0, s) == "B"]
    orb = set()
    for g in stab:
        side = {I[mat_apply(g, V[z])] for i, z in enumerate(c) if (MASKS[sB[0]] >> i) & 1}
        m = sum(1 << i for i, z in enumerate(c) if z in side)
        if m & 1: m ^= 63
        orb.add(MASKS.index(m))
    assert orb == set(sB), (orb, sB)
    return True


def build(cubes, lemmas, parity, cube="typeB"):
    """cube = "typeB": the pair {P, R0} is in its first type B state (needs the lemma: a non-trivial skeleton has a pair
    of type B). cube = "split": the pair {P, R0} is split, any state (needs nothing but the transitivity of Aut(BH) on
    the non-adjacent pairs); the lemma clauses must then be off."""
    assert cube == "typeB" or not lemmas
    nv, cl, ev, xs = full_hybrid.build([cube])
    nv, sq, ncube = full_grid.add_grid_layer(nv, cl, ev, xs, cubes)
    nvv = [nv]
    def new(): nvv[0] += 1; return nvv[0]
    if parity:
        fams = parity_hybrid.families()
        for W in fams:
            acc = xs[W[0]][0]
            for p in W[1:]:
                t = new(); a, b = acc, xs[p][0]
                cl += [[-a, -b, -t], [a, b, -t], [a, -b, t], [-a, b, t]]
                acc = t
            cl.append([acc])
    if lemmas:
        P = 0
        Bstates = lambda a, b: [xs[key(a, b)][s] for s in range(1, 11) if state_type(a, b, s) == "B"]
        Astates = lambda a, b: [xs[key(a, b)][s] for s in range(1, 11) if state_type(a, b, s) == "A"]
        for X in range(n):
            farX = [r for r in range(n) if r != X and r not in nbs[X]]
            cl.append([l for r in farX for l in Bstates(X, r)])                                   # (a)
            inner = [(a, b) for a, b in itertools.combinations(sorted(nbs[X]), 2) if b not in nbs[a]]
            cl.append([l for (a, b) in inner for l in Bstates(a, b)])                             # (b)
            cl.append([l for (a, b) in inner for l in Astates(a, b)])                             # (c)
            for u in nbs[X]:                                                                      # (d)
                cl.append([-xs[key(X, r)][0] for r in nbs[u] if r != X and r not in nbs[X]])
        # C5 at P for the fixed state of R0
        R0 = [r for r in range(n) if r != P and r not in nbs[P]][0]; c = CN[key(P, R0)]
        sB = [s for s in range(1, 11) if state_type(P, R0, s) == "B"][0]; m = MASKS[sB]
        side = {z: (m >> i) & 1 for i, z in enumerate(c)}
        farP = [r for r in range(n) if r != P and r not in nbs[P]]
        omega = {R0} | {r for r in farP if len(set(CN[key(P, r)]) & set(c)) >= 3}
        for a, b in itertools.combinations(c, 2):
            if side[a] != side[b] and gridpartner(P, R0, a) != b:
                omega |= {r for r in farP if a in CN[key(P, r)] and b in CN[key(P, r)]}
        assert len(omega) == 25
        cl.append([l for r in farP if r not in omega for l in Bstates(P, r)])
    return nvv[0], cl, ev, xs


if __name__ == "__main__":
    tmp, tl = sys.argv[1], float(sys.argv[2]); rest = sys.argv[3:]
    cubes = "cubes" in rest; lemmas = "nolemmas" not in rest; parity = "noparity" not in rest
    outname = next((a[4:] for a in rest if a.startswith("out=")), "ultimate.cnf")
    cad_args = [a for a in rest if a.startswith("--")]
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    assert orbit_check()
    cube = "split" if "split" in rest else "typeB"
    if cube == "split": lemmas = False
    nv, cl, ev, xs = build(cubes, lemmas, parity, cube)
    path = os.path.join(tmp, outname)
    with open(path, "w", newline="\n") as f:
        f.write("p cnf %d %d\n" % (nv, len(cl)))
        for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
    print("instance written: %s (%d variables, %d clauses; cubes %s, lemmas %s, parity %s); transitivity on type B states checked" % (path, nv, len(cl), cubes, lemmas, parity), flush=True)
    if tl > 0:
        t0 = time.time()
        try: out = subprocess.run([CAD, "-q"] + cad_args + [path], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
        print("a pair of type B, complete instance: %s (%.1f s)" % (res, time.time() - t0), flush=True)
        if res == "SAT":
            model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
            edges = sorted(ev); open(os.path.join(tmp, "skeleton_ultimate.txt"), "w").write("".join("1" if ev[e] in model else "0" for e in edges) + "\n")
            print("  NON-TRIVIAL SKELETON written to skeleton_ultimate.txt")
