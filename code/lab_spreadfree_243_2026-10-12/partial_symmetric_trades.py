"""Lab session, 2026-10-12. TRADES WITH LESS SYMMETRY from a tri-Cayley graph over Z_3^4.

Input: a graph written by tricayley_census.py (vertex 81 i + index of g, g in F_3^4 in lexicographic order, the 81
translations are automorphisms). One of the three orbits (R, 81 vertices) is kept with ALL its adjacencies (inside R and
from R to the rest); the adjacency inside the other 162 vertices F is free, but only required to be invariant under a
subgroup S = Z_3^2 or Z_3 of the translations (given by vectors). So the completions found have a semiregular Z_3^2
(27 orbits of 9 vertices) or Z_3, and share one third of the graph with the input. Every completion is rebuilt, checked
(A^2 = 20I - A + 2J) and compared with the reference graphs by a direct isomorphism test; it is then blocked (this
exact solution only) and the search continues. UNSAT at the end = complete list of the S-invariant completions.

Model: orbits o = (i, c), c in F_3^4 / S; (o, s) ~ (o', s') iff s' - s in D_oo'; unknown D_oo' for o, o' in F.
python partial_symmetric_trades.py <tmp dir> <edge file> <kept orbit 0|1|2> <seconds per call> <max solutions> <dim of S: 1 or 2> <vectors ...> [references ...]
   vectors as 4 digits, e.g. 2 0010 0001. Environment NOTK=1: only completions NOT invariant under all 81 translations.
   Memory: dim 2: 3 million clauses, under 1 GB; dim 1: about 8 million clauses, 2 to 3 GB."""
import sys, os, subprocess, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T

H4 = list(itertools.product(range(3), repeat=4)); IDX4 = {g: i for i, g in enumerate(H4)}
neg2 = lambda a: tuple((-x) % 3 for x in a); sub2 = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b)); add2 = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))


def coordinates(bs):
    """a complement T of S = <bs> (unit vectors) and the map g -> (c, s) with g = sum c_i t_i + sum s_j b_j"""
    E = [tuple(int(i == j) for j in range(4)) for i in range(4)]; sd = len(bs)
    for ts in itertools.combinations(E, 4 - sd):
        basis = list(ts) + list(bs); tab = {}
        for c in H4: tab[tuple(sum(c[i] * basis[i][k] for i in range(4)) % 3 for k in range(4))] = (c[:4 - sd], c[4 - sd:])
        if len(tab) == 81: return tab
    raise SystemExit("the vectors are dependent")


if __name__ == "__main__":
    tmp, path, keep = sys.argv[1], sys.argv[2], int(sys.argv[3])
    tl = float(sys.argv[4]); maxsol = int(sys.argv[5]); sd = int(sys.argv[6]); bs = [tuple(int(ch) for ch in a) for a in sys.argv[7:7 + sd]]
    S2 = list(itertools.product(range(3), repeat=sd)); Z2 = (0,) * sd; REPS2 = [g for g in S2 if g != Z2 and g < neg2(g)]
    CS = list(itertools.product(range(3), repeat=4 - sd))
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    A0 = T.load(path); refs = [(os.path.basename(p), T.load(p)) for p in [path] + sys.argv[7 + sd:]]
    co = coordinates(bs)
    orbits = [(i, c) for i in range(3) for c in CS]; r = len(orbits); OI = {o: k for k, o in enumerate(orbits)}
    vert = {}                                                           # (orbit index, s) -> vertex of the input graph
    for i in range(3):
        for g in H4:
            c, s = co[g]; vert[(OI[(i, c)], s)] = 81 * i + IDX4[g]
    inR = [o[0] == keep for o in orbits]
    def given(a, b, d): return bool(A0[vert[(a, Z2)], vert[(b, d)]])      # d in D_ab of the input graph
    # check that the input is S-invariant in this model
    assert all(A0[vert[(a, s)], vert[(b, add2(s, d))]] == A0[vert[(a, Z2)], vert[(b, d)]] for a in range(r) for b in range(r) for s in S2 for d in S2)
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    U = [dict() for _ in range(r)]; V = {}; fixed = {}
    for a in range(r):
        for g in REPS2:
            v = new(); U[a][g] = v; U[a][neg2(g)] = v
            if inR[a]: fixed[v] = given(a, a, g)
    for a in range(r):
        for b in range(a + 1, r):
            V[(a, b)] = {g: new() for g in S2}
            if inR[a] or inR[b]:
                for g in S2: fixed[V[(a, b)][g]] = given(a, b, g)
    def mm(a, k, g):
        if a == k: return None if g == Z2 else U[a][g]
        return V[(a, k)][g] if a < k else V[(k, a)][neg2(g)]
    cache = {}
    def AND(a, b):
        if a is None or b is None: return None
        fa, fb = fixed.get(a), fixed.get(b)
        if fa is False or fb is False: return None
        if fa is True and fb is True: return "T"
        if fa is True: return b
        if fb is True: return a
        if a == b: return a
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            t = new(); cl.extend([[-t, a], [-t, b], [t, -a, -b]]); cache[k] = t
        return cache[k]
    def exactly(lits, k):
        k -= sum(1 for l in lits if l == "T"); l2 = []
        for l in lits:
            if l is None or l == "T": continue
            f = fixed.get(l)
            if f is True: k -= 1
            elif f is None: l2.append(l)
        lits = l2
        if k < 0 or k > len(lits): cl.append([]); return
        if not lits: return
        prev = None
        for l in lits:
            cur = [None] + [new() for _ in range(k + 1)]
            for j in range(1, k + 2):
                pj = prev[j] if prev else None
                if pj is not None: cl.append([-pj, cur[j]])
                if j == 1: cl.append([-l, cur[j]])
                elif prev: cl.append([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                cl.append(c + [l])
                if j > 1: cl.append(c + ([prev[j - 1]] if prev else []))
            prev = cur
        if k >= 1: cl.append([prev[k]])
        cl.append([-prev[k + 1]])
    free = [v for a in range(r) if not inR[a] for v in sorted(set(U[a].values()))] + [v for (a, b), d in V.items() if not inR[a] and not inR[b] for v in d.values()]
    for a in range(r):
        if inR[a]: continue
        exactly([U[a][g] for g in REPS2] * 2 + [mm(a, b, g) for b in range(r) if b != a for g in S2], 22)
    for a in range(r):
        for b in range(a, r):
            if inR[a] and inR[b]: continue
            for d in (REPS2 if a == b else S2):
                lits = [AND(mm(a, k, g), mm(k, b, sub2(d, g))) for k in range(r) for g in S2]
                exactly(lits + [mm(a, b, d)], 2)
    if os.environ.get("NOTK"):
        # the completion must NOT be invariant under all 81 translations: some adjacency differs from its translate
        # by one of the two basis vectors of the complement (orbit (i, c) -> (i, c + delta))
        zs = []
        for delta in [tuple(int(i == j) for j in range(4 - sd)) for i in range(4 - sd)]:
            sh = [OI[(orbits[a][0], add2(orbits[a][1], delta))] for a in range(r)]
            for a in range(r):
                if inR[a]: continue
                for b in range(a, r):
                    if inR[b]: continue
                    for d in (REPS2 if a == b else S2):
                        x, y = mm(a, b, d), mm(sh[a], sh[b], d)
                        if x == y: continue
                        z = new(); cl.extend([[-z, x, y], [-z, -x, -y], [z, -x, y], [z, x, -y]]); zs.append(z)
        cl.append(zs)
    print("kept orbit %d, S = <%s>%s: %d free variables, %d variables, %d clauses" % (keep, ", ".join(sys.argv[7:7 + sd]), ", completions NOT invariant under the 81 translations" if os.environ.get("NOTK") else "", len(free), nv[0], len(cl)), flush=True)
    block = []; tally = collections.Counter(); cnf = os.path.join(tmp, "pst_%d.cnf" % os.getpid()); status = "limit reached"
    for it in range(maxsol):
        with open(cnf, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (nv[0], len(cl) + len(block)))
            for c in cl: f.write(" ".join(map(str, c)) + " 0\n")
            for c in block: f.write(" ".join(map(str, c)) + " 0\n")
        t1 = time.time()
        try: out = subprocess.run([CAD, "-q", cnf], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
        if res != "SAT": status = "%s after %d solutions (%.0f s)" % (res, it, time.time() - t1); break
        model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
        val = lambda v: fixed[v] if v in fixed else (v in model)
        A = np.zeros((243, 243), dtype=np.int64)
        for a in range(r):
            for s in S2:
                x = vert[(a, s)]
                for d in S2:
                    if d != Z2 and val(U[a][d]): A[x, vert[(a, add2(s, d))]] = 1
                for b in range(a + 1, r):
                    for d in S2:
                        if val(V[(a, b)][d]): y = vert[(b, add2(s, d))]; A[x, y] = A[y, x] = 1
        ok = bool((A @ A == 20 * np.eye(243, dtype=np.int64) - A + 2).all()); same = bool((A == A0).all())
        name = next((nm for nm, R in refs if T.find_iso(A, R) is not None), None) if ok else "NOT STRONGLY REGULAR"
        if name is None:
            name = "new_pst_%d_%d.edges" % (os.getpid(), it); refs.append((name, A))
            with open(os.path.join(tmp, name), "w", newline="\n") as f:
                for x in range(243):
                    for y in range(x + 1, 243):
                        if A[x, y]: f.write("%d %d\n" % (x, y))
            o, gens, base, sizes = T.aut_group(A)
            print("   NEW GRAPH written to %s: |Aut| = %d, vertex orbits %s" % (name, o, [len(x) for x in T.vertex_orbits(243, gens)]), flush=True)
        tally[name + (" (the input itself)" if same else "")] += 1
        print("solution %d (%.0f s): strongly regular %s; changed pairs %d; graph: %s%s" % (it + 1, time.time() - t1, ok, int(np.abs(A - A0).sum()) // 2, name, " = the input itself" if same else ""), flush=True)
        block.append([(-v if v in model else v) for v in free])
    print("end: %s; tally %s" % (status, tally.most_common()), flush=True)
    try: os.remove(cnf)
    except OSError: pass
