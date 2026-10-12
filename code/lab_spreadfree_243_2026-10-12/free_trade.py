"""Lab session, 2026-10-12. TRADE WITHOUT IMPOSED SYMMETRY: keep a set R of vertices of a srg(243,22,1,2) with all its
adjacencies (inside R and from R to the rest F), and ask for any strongly regular completion inside F.

Unknowns: one variable per pair of F. Constraints:
  r in R, f in F : #(F-neighbours of r adjacent to f) = (1 if r ~ f else 2) - #(common neighbours of r, f in R);
  f in F         : degree 22;
  f, g in F      : #(common F-neighbours) + [f ~ g] = 2 - #(common neighbours in R).
Optional (argument notrans=<k>): the input must be a tri-Cayley graph over Z_3^4 written by tricayley_census.py and the
completion must NOT be invariant under the translation by t, for the first k of the 40 directions t (k = 40: no
translation at all is an automorphism).
The CNF is streamed to disk (about 25 million clauses for |F| = 162); cadical; each completion is checked
(A^2 = 20I - A + 2J), compared with the references by a direct isomorphism test, and its automorphism group is computed.

python free_trade.py <tmp dir> <edge file> <R: first:<n> | list:a,b,...> <seconds per call> <max solutions> [notrans=<k>] [sym] [references ...]
  sym: block each solution together with its images under the automorphisms of the input that preserve R
Memory: Python about 1 GB, cadical 3 to 4 GB for |F| = 162."""
import sys, os, subprocess, time, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T

if __name__ == "__main__":
    tmp, path, rspec, tl, maxsol = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5])
    rest = sys.argv[6:]; notrans = next((int(a[8:]) for a in rest if a.startswith("notrans=")), 0)
    CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
    A0 = T.load(path); n = len(A0); refs = [(os.path.basename(p), T.load(p)) for p in [path] + [a for a in rest if not a.startswith("notrans=") and a != "sym"]]
    R = list(range(int(rspec[6:]))) if rspec.startswith("first:") else sorted(int(t) for t in rspec[5:].split(","))
    Rs = set(R); F = [v for v in range(n) if v not in Rs]; adj = [set(np.nonzero(A0[v])[0].tolist()) for v in range(n)]
    nbF = {v: sorted(adj[v] - Rs) for v in range(n)}; nbR = {v: adj[v] & Rs for v in range(n)}
    t0 = time.time(); nv = [0]; nc = [0]
    cnf = os.path.join(tmp, "free_%d.cnf" % os.getpid()); out = open(cnf, "w", newline="\n"); HEAD = "p cnf %12d %12d\n"; out.write(HEAD % (0, 0))
    def new(): nv[0] += 1; return nv[0]
    def emit(c): out.write(" ".join(map(str, c)) + " 0\n"); nc[0] += 1
    X = {}
    for i, a in enumerate(F):
        for b in F[i + 1:]: X[(a, b)] = new()
    x = lambda a, b: X[(a, b)] if a < b else X[(b, a)]
    cache = {}
    def AND(a, b):
        k = (a, b) if a < b else (b, a)
        t = cache.get(k)
        if t is None:
            t = new(); cache[k] = t; emit([-t, a]); emit([-t, b]); emit([t, -a, -b])
        return t
    def exactly(lits, k):
        if k < 0 or k > len(lits): emit([]); return
        if not lits: return
        prev = None
        for l in lits:
            cur = [None] + [new() for _ in range(k + 1)]
            for j in range(1, k + 2):
                pj = prev[j] if prev else None
                if pj is not None: emit([-pj, cur[j]])
                if j == 1: emit([-l, cur[j]])
                elif prev: emit([-l, -prev[j - 1], cur[j]])
                c = [-cur[j]] + ([pj] if pj is not None else [])
                emit(c + [l])
                if j > 1: emit(c + ([prev[j - 1]] if prev else []))
            prev = cur
        if k >= 1: emit([prev[k]])
        emit([-prev[k + 1]])
    for r in R:
        for f in F:
            exactly([x(g, f) for g in nbF[r] if g != f], (1 if f in adj[r] else 2) - len(nbR[r] & nbR[f]))
    for f in F: exactly([x(f, g) for g in F if g != f], 22 - len(nbR[f]))
    for i, f in enumerate(F):
        for g in F[i + 1:]:
            tgt = 2 - len(nbR[f] & nbR[g])
            if tgt == 0:
                emit([-x(f, g)])
                for h in F:
                    if h != f and h != g: emit([-x(f, h), -x(g, h)])
            else:
                exactly([AND(x(f, h), x(g, h)) for h in F if h != f and h != g] + [x(f, g)], tgt)
    if notrans:
        H4 = list(itertools.product(range(3), repeat=4)); IDX4 = {g: i for i, g in enumerate(H4)}
        dirs = [g for g in H4 if any(g) and g < tuple((-c) % 3 for c in g)][:notrans]
        for t in dirs:
            pi = [81 * (v // 81) + IDX4[tuple((a + b) % 3 for a, b in zip(H4[v % 81], t))] for v in range(n)]
            assert all(A0[pi[a], pi[b]] == A0[a, b] for a in range(0, n, 7) for b in range(n)), "the translation is not an automorphism of the input"
            zs = []
            for (a, b), v in X.items():
                w = x(pi[a], pi[b])
                if w == v: continue
                z = new(); emit([-z, v, w]); emit([-z, -v, -w]); emit([z, -v, w]); emit([z, v, -w]); zs.append(z)
            emit(zs)
    free = sorted(X.values())
    sym = []
    if "sym" in rest:
        # automorphisms of the input that preserve R: they map completions to completions, so every solution is
        # blocked together with all its images under them (the list then has one completion per class)
        import regular_subgroups as RS
        o, gens, base, sizes = T.aut_group(A0); ident = tuple(range(n))
        if o <= 20000:
            G = RS.generate([tuple(g) for g in gens], ident); sym = [g for g in G if g != ident and all(g[v] in Rs for v in R)]
        print("symmetries used for blocking: %d automorphisms of the input (order %d) preserve R" % (len(sym), o), flush=True)
    print("R: %d vertices kept, F: %d vertices, %d free pairs, %d variables, %d clauses (written in %.0f s)%s" % (len(R), len(F), len(free), nv[0], nc[0], time.time() - t0, "; no invariance under %d translation directions" % notrans if notrans else ""), flush=True)
    tally = collections.Counter(); status = "limit reached"
    for it in range(maxsol):
        out.flush(); out.seek(0); out.write(HEAD % (nv[0], nc[0])); out.flush(); out.seek(0, 2)
        t1 = time.time()
        try: res_out = subprocess.run([CAD, "-q", cnf], capture_output=True, text=True, timeout=tl).stdout
        except subprocess.TimeoutExpired: res_out = ""
        res = "UNSAT" if "s UNSATISFIABLE" in res_out else "SAT" if "s SATISFIABLE" in res_out else "NO DECISION"
        if res != "SAT": status = "%s after %d solutions (%.0f s)" % (res, it, time.time() - t1); break
        model = set(int(t) for line in res_out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0 and int(t) <= len(free))
        A = A0.copy()
        for (a, b), v in X.items(): A[a, b] = A[b, a] = 1 if v in model else 0
        ok = bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all()); same = bool((A == A0).all())
        name = next((nm for nm, Rm in refs if T.find_iso(A, Rm) is not None), None) if ok else "NOT STRONGLY REGULAR"
        if name is None:
            name = "new_free_%d_%d.edges" % (os.getpid(), it); refs.append((name, A))
            with open(os.path.join(tmp, name), "w", newline="\n") as f:
                for a in range(n):
                    for b in range(a + 1, n):
                        if A[a, b]: f.write("%d %d\n" % (a, b))
            o, gens, base, sizes = T.aut_group(A)
            print("   NEW GRAPH written to %s: |Aut| = %d, vertex orbits %s" % (name, o, [len(q) for q in T.vertex_orbits(n, gens)] if o > 1 else "all trivial"), flush=True)
        tally[name] += 1
        print("solution %d (%.0f s): strongly regular %s; changed pairs %d; graph: %s%s" % (it + 1, time.time() - t1, ok, int(np.abs(A - A0).sum()) // 2, name, " = the input itself" if same else ""), flush=True)
        emit([(-v if v in model else v) for v in free])
        true_pairs = [k for k, v in X.items() if v in model]
        for g in sym: emit([-x(g[a], g[b]) for (a, b) in true_pairs])
    out.close()
    print("end: %s; tally %s" % (status, tally.most_common()), flush=True)
    try: os.remove(cnf)
    except OSError: pass
