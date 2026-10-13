"""Lab session, 2026-10-13. TRI-CAYLEY graphs srg(243,22,1,2) over EVERY group of order 81 (groups81.py), both types.

Model: a group K of order 81 acting semiregularly with three orbits; vertices (i, g); (i, g) ~ (j, h) iff g^-1 h in
D_ij, D_ji = D_ij^-1, D_ii = D_ii^-1 without the identity. For all i <= j and d:
    sum_k #{a in D_ik : a^-1 d in D_kj} + [d in D_ij] = 2,
type I: |D_ii| = 10, |D_ij| = 6; type II: |D_ii| = 4, |D_ij| = 9 (the only two possibilities, group-independent).
Normalisation: the identity is in D_01 and in D_02 (right translation of the orbits 1 and 2).
Redundant global constraint (environment NORATIONAL to switch it off): rationality of the eigenspaces, i.e. conjugacy
classes in the same rational class contain the same total number of elements of D_00, D_11, D_22.
For each group and type, cadical is called with a new seed and a shuffled clause order; each solution is rebuilt,
checked (A^2 = 20I - A + 2J), compared with the reference graphs (invariants, then isomorphism), and blocked together
with its images under the permutations of the orbits, the inner automorphisms of K and the renormalisations, up to a
given number of solutions. UNSAT at the first call = no graph of that type over that group
(a complete statement); otherwise the output is a SAMPLE, not a census. New graphs are written to the output directory.

python tricayley_groups.py <out dir> <seconds per call> <solutions per case> <first group> <last group> <types: 1, 2 or 12> [references ...]
Memory: about one million clauses per call."""
import sys, os, subprocess, time, random, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import aut_tools as T, trade_bfs as B, groups81 as G81
CAD = os.environ.get("CADICAL", "C:/home/researcher/Desktop/Recherche_Conway/c1-codex/tools/win64/cadical.exe")
n = 243


def encode(Tb, e, typ):
    N = 81; inv = G81.inverse(Tb, e); dsize, osize = (10, 6) if typ == 1 else (4, 9)
    nv = [0]; cl = []
    def new(): nv[0] += 1; return nv[0]
    reps = [g for g in range(N) if g != e and g < inv[g]]
    U = [dict() for _ in range(3)]
    for i in range(3):
        for g in reps: v = new(); U[i][g] = v; U[i][inv[g]] = v
    V = {p: {g: new() for g in range(N)} for p in [(0, 1), (0, 2), (1, 2)]}
    fixed = {V[(0, 1)][e]: True, V[(0, 2)][e]: True}
    def m(i, k, g):
        if i == k: return None if g == e else U[i][g]
        return V[(i, k)][g] if i < k else V[(k, i)][inv[g]]
    cache = {}
    def AND(a, b):
        if a is None or b is None: return None
        fa, fb = fixed.get(a), fixed.get(b)
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
            if fixed.get(l) is True: k -= 1
            else: l2.append(l)
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
    for v in fixed: cl.append([v])
    for i in range(3): exactly([U[i][g] for g in reps], dsize // 2)
    for p in V: exactly(list(V[p].values()), osize)
    for i in range(3):
        for j in range(i, 3):
            for d in (reps if i == j else range(N)):
                lits = [AND(m(i, k, a), m(k, j, Tb[inv[a]][d])) for k in range(3) for a in range(N)]
                exactly(lits + [m(i, j, d)], 2)
    # RATIONALITY (redundant, global): the eigenspaces are defined over Q, so the number of vertices x with x ~ g x is
    # the same for g and g^k (k prime to the order of g). For a semiregular K this number is |C(g)| * sum_i |cl(g) & D_ii|,
    # hence the conjugacy classes inside one rational class carry the same total number of elements of D_00, D_11, D_22.
    if os.environ.get("NORATIONAL") is None:
        cls_of = {}
        for g in range(N):
            if g == e or g in cls_of: continue
            c = frozenset(Tb[Tb[h][g]][inv[h]] for h in range(N))
            for x in c: cls_of[x] = c
        def power(g, k):
            y = e
            for _ in range(k): y = Tb[y][g]
            return y
        def unary(lits, top):
            """outputs o[j] <-> at least j of lits, j = 1..top"""
            prev = None
            for l in lits:
                cur = [None] + [new() for _ in range(top)]
                for j in range(1, top + 1):
                    pj = prev[j] if prev else None
                    if pj is not None: cl.append([-pj, cur[j]])
                    if j == 1: cl.append([-l, cur[j]])
                    elif prev: cl.append([-l, -prev[j - 1], cur[j]])
                    c = [-cur[j]] + ([pj] if pj is not None else [])
                    cl.append(c + [l])
                    if j > 1: cl.append(c + ([prev[j - 1]] if prev else []))
                prev = cur
            return prev
        done = set(); counters = {}
        def cnt(c):
            if c not in counters: counters[c] = unary([U[i][x] for i in range(3) for x in sorted(c)], min(3 * len(c), 3 * dsize) )
            return counters[c]
        for g in range(N):
            if g == e: continue
            og = G81.order(Tb, e, g); c0 = cls_of[g]
            for k in range(2, og):
                if k % 3 == 0: continue
                c1 = cls_of[power(g, k)]
                if c1 == c0 or (c0, c1) in done or (c1, c0) in done: continue
                done.add((c0, c1)); a, b = cnt(c0), cnt(c1)
                for j in range(1, min(len(a), len(b))): cl.extend([[-a[j], b[j]], [a[j], -b[j]]])
    free = sorted(set(v for i in range(3) for v in U[i].values()) | set(v for p in V for v in V[p].values()))
    return nv[0], cl, U, V, free, inv


if __name__ == "__main__":
    outdir, tl, nsol, g0, g1, types = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
    known = [(os.path.basename(p), T.load(p)) for p in sys.argv[7:]]; keys = {nm: B.invariant(A) for nm, A in known}
    groups = G81.tables(); print("%d groups of order 81" % len(groups), flush=True)
    for gi, (gname, Tb, e) in enumerate(groups):
        if gi < g0 or gi > g1: continue
        for typ in (1, 2):
            if str(typ) not in types: continue
            nv, cl, U, V, free, inv = encode(Tb, e, typ); block = []; tally = collections.Counter(); status = "sample of %d" % nsol; t1 = time.time()
            path = os.path.join(outdir, "tcg_%d.cnf" % os.getpid())
            for it in range(nsol):
                rnd = random.Random(1000 * gi + 10 * typ + it); order = list(range(len(cl))); rnd.shuffle(order)
                with open(path, "w", newline="\n") as f:
                    f.write("p cnf %d %d\n" % (nv, len(cl) + len(block)))
                    for c in block: f.write(" ".join(map(str, c)) + " 0\n")
                    for t in order: f.write(" ".join(map(str, cl[t])) + " 0\n")
                try: out = subprocess.run([CAD, "-q", "--seed=%d" % it, path], capture_output=True, text=True, timeout=tl).stdout
                except subprocess.TimeoutExpired: out = ""
                res = "UNSAT" if "s UNSATISFIABLE" in out else "SAT" if "s SATISFIABLE" in out else "NO DECISION"
                if res != "SAT":
                    status = ("NONE: no graph of this type over this group" if it == 0 else "complete list of the normalised solutions (%d)" % it) if res == "UNSAT" else "NO DECISION at call %d" % (it + 1)
                    break
                model = set(int(t) for line in out.split("\n") if line.startswith("v ") for t in line[2:].split() if int(t) > 0)
                A = np.zeros((n, n), dtype=np.int64)
                for i in range(3):
                    for g in range(81):
                        for d in range(81):
                            if d != e and U[i][d] in model: A[81 * i + g, 81 * i + Tb[g][d]] = 1
                        for j in range(i + 1, 3):
                            for d in range(81):
                                if V[(i, j)][d] in model: A[81 * i + g, 81 * j + Tb[g][d]] = 1; A[81 * j + Tb[g][d], 81 * i + g] = 1
                # block the solution with its images under: permutations of the orbits, conjugation by the elements of
                # K, and the choice of the elements of D_01, D_02 sent to the identity (all give isomorphic graphs)
                Dm = {}
                for i in range(3): Dm[(i, i)] = frozenset(d for d in range(81) if d != e and U[i][d] in model)
                for (i, j) in V:
                    Dm[(i, j)] = frozenset(d for d in range(81) if V[(i, j)][d] in model); Dm[(j, i)] = frozenset(inv[d] for d in Dm[(i, j)])
                imgs = set()
                import itertools as _it
                for perm in _it.permutations(range(3)):
                    Dp = {(i, j): Dm[(perm[i], perm[j])] for i in range(3) for j in range(3)}
                    for k in range(81):
                        ck = [Tb[Tb[k][x]][inv[k]] for x in range(81)]
                        Dk = {key: frozenset(ck[x] for x in val) for key, val in Dp.items()}
                        for a in Dk[(0, 1)]:
                            ai = inv[a]; n01 = frozenset(Tb[x][ai] for x in Dk[(0, 1)]); n11 = frozenset(Tb[Tb[a][x]][ai] for x in Dk[(1, 1)])
                            for b in Dk[(0, 2)]:
                                bi = inv[b]
                                imgs.add((Dk[(0, 0)], n11, frozenset(Tb[Tb[b][x]][bi] for x in Dk[(2, 2)]), n01, frozenset(Tb[x][bi] for x in Dk[(0, 2)]), frozenset(Tb[Tb[a][x]][bi] for x in Dk[(1, 2)])))
                for (m00, m11, m22, m01, m02, m12) in imgs:
                    block.append(sorted({-U[0][d] for d in m00} | {-U[1][d] for d in m11} | {-U[2][d] for d in m22}) + [-V[(0, 1)][d] for d in m01] + [-V[(0, 2)][d] for d in m02] + [-V[(1, 2)][d] for d in m12])
                if not ((A == A.T).all() and bool((A @ A == 20 * np.eye(n, dtype=np.int64) - A + 2).all())): tally["NOT STRONGLY REGULAR"] += 1; continue
                key = B.invariant(A); hit = next((nm for nm, Rm in known if keys[nm] == key and T.find_iso(A, Rm) is not None), None)
                if hit is None:
                    hit = "tcg_group%02d_type%d_%d.edges" % (gi, typ, len(known))
                    with open(os.path.join(outdir, hit), "w", newline="\n") as f:
                        for a in range(n):
                            for b in range(a + 1, n):
                                if A[a, b]: f.write("%d %d\n" % (a, b))
                    known.append((hit, A)); keys[hit] = key; o2, g2, _, _ = T.aut_group(A)
                    print("   NEW GRAPH %s: |Aut| = %d, vertex orbits %s, parallels %s, grids %s" % (hit, o2, ([len(x) for x in T.vertex_orbits(n, g2)] if o2 > 1 else "243 orbits of size 1"), key[0], key[1]), flush=True)
                tally[hit] += 1
            print("group %d (%s), type %s: %s (%.0f s): %s" % (gi, gname, "I" if typ == 1 else "II", status, time.time() - t1, dict(tally)), flush=True)
            try: os.remove(path)
            except OSError: pass
