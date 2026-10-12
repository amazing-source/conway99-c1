"""Parity skeleton of S3-covers of Brouwer-Haemers BH = srg(81,20,1,6), grid formulation (note 165 §6, note 175).
BH: V = F_3^4, x ~ y iff q(y-x) = 0, q = x0^2 + x1^2 + x2 x3 (elliptic quadric, 10 projective points = ovoid).
eps: Z_2 on edges, even on every line-triangle, gauge eps = 0 on a BFS tree.
For a non-adjacent pair (P,R): its 6 common neighbours come in 3 grid pairs (Z_i, Z_i'), one per 3x3 grid
P + <v,w> containing R. b(Z) = eps(PZ) + eps(ZR); s_i = b(Z_i) + b(Z_i') = holonomy of the grid square.
Condition "weight of the 6 b's in {0,3,6}" <=> (#odd s_i in {0,1,3}) and
   [no odd s]  : b(Z_1) = b(Z_2) = b(Z_3)
   [one odd s_i]: b(Z_j) != b(Z_k) for the two other grid pairs.
eps nontrivial in H^1  <=>  some pair has L = s_1+s_2+s_3 = 1 (Jorgensen form injective on H^1, note 165).
WLOG (Aut(BH) transitive on non-adjacent pairs): pair (0, R0) has L = 1; cases A: s = (1,1,1); B_i: only s_i = 1.
Usage: python3 s3grid.py CASE(A|B1|B2|B3) THREADS TIMELIMIT [cnf-out]"""
import itertools, sys, time, collections
V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
mul = lambda c, a: tuple((c * x) % 3 for x in a)
n = 81
S = [v for v in V if any(v) and q(v) == 0]; assert len(S) == 20
adj = [[I[add(V[i], s)] for s in S] for i in range(n)]
nbs = [set(a) for a in adj]
def norm(v):
    c = next(x for x in v if x); return v if c == 1 else mul(2, v)
dirs = sorted({norm(s) for s in S}); assert len(dirs) == 10
def checks():
    # srg(81,20,1,6)
    for i in range(n):
        for j in range(i + 1, n):
            c = len(nbs[i] & nbs[j]); assert c == (1 if j in nbs[i] else 6)
def grid_pairs(P, R):
    """the 3 grid pairs (Z, Z') of common neighbours of non-adjacent P, R"""
    u = sub(V[R], V[P]); out = []
    for v, w in itertools.combinations(dirs, 2):
        for a in (1, 2):
            for b in (1, 2):
                if add(mul(a, v), mul(b, w)) == u:
                    out.append((I[add(V[P], mul(a, v))], I[add(V[P], mul(b, w))]))
    return out
def unit_test():
    # weight in {0,3,6} <=> grid conditions, for every bit pattern
    for bits in itertools.product((0, 1), repeat=6):
        b = [(bits[0], bits[1]), (bits[2], bits[3]), (bits[4], bits[5])]
        s = [x ^ y for x, y in b]; w = sum(bits)
        ok1 = w in (0, 3, 6)
        o = sum(s)
        if o == 0: ok2 = b[0][0] == b[1][0] == b[2][0]
        elif o == 1:
            i = s.index(1); j, k = [t for t in range(3) if t != i]; ok2 = b[j][0] != b[k][0]
        elif o == 3: ok2 = True
        else: ok2 = False
        assert ok1 == ok2, bits
if __name__ == "__main__":
    checks(); unit_test()
    case, threads, tlim = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
    import pycryptosat
    sol = pycryptosat.Solver(threads=threads, time_limit=tlim)
    nv = 0; clauses = []; xors = []
    def new():
        global nv; nv += 1; return nv
    def cl(c): clauses.append(c); sol.add_clause(c)
    def xo(vs, rhs): xors.append((vs, rhs)); sol.add_xor_clause(vs, rhs)
    E = {}
    for i in range(n):
        for j in adj[i]:
            if i < j: E[(i, j)] = E[(j, i)] = new()
    seen, dq, tree = {0}, collections.deque([0]), []
    while dq:
        u = dq.popleft()
        for v in sorted(nbs[u]):
            if v not in seen: seen.add(v); dq.append(v); tree.append((u, v))
    for u, v in tree: cl([-E[(u, v)]])
    ntri = 0
    for d in dirs:
        for x in range(n):
            y = I[add(V[x], d)]; z = I[add(V[y], d)]
            if x < y and x < z: xo([E[(x, y)], E[(y, z)], E[(x, z)]], False); ntri += 1
    assert ntri == 270
    B = {}
    def bvar(P, Z, R):
        key = (P, Z, R)
        if key not in B:
            t = new(); xo([E[(P, Z)], E[(Z, R)], t], False); B[key] = t
        return B[key]
    npairs = 0; SQ = {}
    for P in range(n):
        for R in range(P + 1, n):
            if R in nbs[P]: continue
            gp = grid_pairs(P, R); assert len(gp) == 3 and len({z for p in gp for z in p}) == 6
            bs = [(bvar(P, Z, R), bvar(P, Z2, R)) for Z, Z2 in gp]
            s = []
            for b1, b2 in bs:
                v = new(); xo([b1, b2, v], False); s.append(v)
            SQ[(P, R)] = s; npairs += 1
            s1, s2, s3 = s
            cl([-s1, -s2, s3]); cl([-s1, s2, -s3]); cl([s1, -s2, -s3])          # never exactly two odd
            r = [bs[0][0], bs[1][0], bs[2][0]]
            for j, k in ((0, 1), (1, 2)):                                          # no odd: all equal
                cl([s1, s2, s3, -r[j], r[k]]); cl([s1, s2, s3, r[j], -r[k]])
            for i in range(3):                                                     # only s_i odd: other two differ
                j, k = [t for t in range(3) if t != i]
                base = [-s[i], s[j], s[k]]
                cl(base + [r[j], r[k]]); cl(base + [-r[j], -r[k]])
    assert npairs == 2430
    R0 = min(R for R in range(1, n) if R not in nbs[0]); s = SQ[(0, R0)]
    pat = {'A': (1, 1, 1), 'B1': (1, 0, 0), 'B2': (0, 1, 0), 'B3': (0, 0, 1)}[case]
    for v, bit in zip(s, pat): cl([v] if bit else [-v])
    print(f"case {case}: vars {nv}, clauses {len(clauses)}, xors {len(xors)}, R0={R0}", flush=True)
    if len(sys.argv) > 4:
        with open(sys.argv[4], 'w') as f:
            f.write(f"p cnf {nv} {len(clauses) + 4 * len(xors)}\n")
            for c in clauses: f.write(" ".join(map(str, c)) + " 0\n")
            for vs, rhs in xors:
                for signs in itertools.product((1, -1), repeat=len(vs)):
                    if (sum(1 for x in signs if x < 0) % 2 == 0) != rhs:   # forbid assignments with wrong parity
                        pass
                for assign in itertools.product((0, 1), repeat=len(vs)):
                    if sum(assign) % 2 != int(rhs):
                        f.write(" ".join(str(-v if a else v) for v, a in zip(vs, assign)) + " 0\n")
        print("cnf written", flush=True)
    t0 = time.time(); sat, model = sol.solve()
    st = "SAT" if sat is True else ("UNSAT" if sat is False else "UNKNOWN")
    print(f"case {case}: {st} after {time.time()-t0:.0f}s", flush=True)
    if sat:
        import pickle; pickle.dump({k: model[v] for k, v in E.items() if k[0] < k[1]}, open(f"s3grid_sol_{case}.pkl", "wb"))
