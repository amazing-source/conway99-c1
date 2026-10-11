"""Alternative encoding of the parity skeleton: triangle-evenness is built in.
Every line-triangle uses one direction class v, so eps restricted to direction v is the coboundary of a function
f_v : F_3^4 -> Z_2 (defined modulo constants on v-lines).  eps(x, x+s) = f_v(x) + f_v(x+s), v = [s].
Gauge: f_v fixed to 0 at the first point of every v-line; global coboundary g removed by also fixing ... (not needed
for UNSAT).  Pair (0,R0) forced 3/3 with a pattern given up to complement; we encode 'pattern OR complement'."""
import itertools, sys, numpy as np
V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
S = [v for v in V if any(v) and q(v) == 0]
norm = lambda v: v if next(x for x in v if x) == 1 else tuple((2 * x) % 3 for x in v)
dirs = sorted({norm(s) for s in S}); D = {d: i for i, d in enumerate(dirs)}
assert len(S) == 20 and len(dirs) == 10
nv = 0; cls = []
def new():
    global nv; nv += 1; return nv
F = {}
for d in dirs:
    for x in V:
        F[(d, x)] = new()
    for x in V:   # gauge: f_d = 0 at the smallest point of each d-line
        line = sorted([x, add(x, d), add(add(x, d), d)])
        if x == line[0]: cls.append([-F[(d, x)]])
def xor_eq(vs, parity):
    for signs in itertools.product((0, 1), repeat=len(vs)):
        if sum(signs) % 2 != parity:
            cls.append([(-v if s else v) for v, s in zip(vs, signs)])
Sset = set(S); zero = (0,) * 4
P0 = zero
R0 = min((d for d in V if d != zero and d not in Sset), key=lambda v: I[v])
pattern = [int(t) for t in sys.argv[2].split(",")] if len(sys.argv) > 2 else None
for P in V:
    for R in V:
        if I[P] >= I[R]: continue
        delta = tuple((r - p) % 3 for p, r in zip(P, R))
        if delta in Sset: continue
        pis = []; Zs = []
        for s1 in S:
            s2 = tuple((a - b) % 3 for a, b in zip(delta, s1))
            if s2 not in Sset: continue
            Z = add(P, s1); d1, d2 = norm(s1), norm(s2)
            p = new(); xor_eq([F[(d1, P)], F[(d1, Z)], F[(d2, Z)], F[(d2, R)], p], 0); pis.append(p); Zs.append(I[Z])
        assert len(pis) == 6
        if (P, R) == (P0, R0):
            order = sorted(range(6), key=lambda i: Zs[i])
            print("CN of (0,R0):", sorted(Zs))
            if pattern is not None:
                odd = set(pattern)
                bits = [1 if Zs[i] in odd else 0 for i in range(6)]
                # pattern or its complement (global gauge flips all six)
                a = new()
                for i in range(6):
                    cls.append([-a, pis[i] if bits[i] else -pis[i]])
                    cls.append([a, pis[i] if not bits[i] else -pis[i]])
            allowed = (3,)
        else:
            allowed = (0, 3, 6)
        for bits in itertools.product((0, 1), repeat=6):
            if sum(bits) not in allowed:
                cls.append([(-v if b else v) for v, b in zip(pis, bits)])
with open(sys.argv[1], "w") as f:
    f.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
print("vars", nv, "clauses", len(cls), "R0 index", I[R0])
