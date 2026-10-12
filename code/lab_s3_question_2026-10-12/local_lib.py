"""Lab session, 2026-10-12. Local problem of a parity skeleton at an arbitrary vertex X of the Brouwer-Haemers graph, as a
CNF with state variables (same encoding as local_cnf2.py, but for any base vertex, so that the local problems at several
vertices can be glued through the states of the pairs they share).

BH: V = F_3^4, x ~ y iff q(y - x) = 0, q = x0^2 + x1^2 + x2 x3.
The STATE of a non-adjacent pair {x, y} is "flat" or a partition 3+3 of its six common neighbours C(x,y); it is the same
object from wherever it is seen. Grid pairs of C(x,y): {z, x + y - z}. Type A: the three grid pairs are separated;
type B: exactly one is.
Local problem at X: the pairs {X, R} (R far from X; "blocks") and the pairs {a, b} inside N(X); the square (X, a, R, b)
is odd iff the state of {X, R} separates a from b iff the state of {a, b} separates X from R."""
import itertools

V = list(itertools.product(range(3), repeat=4)); I = {v: i for i, v in enumerate(V)}; n = 81
q = lambda x: (x[0] * x[0] + x[1] * x[1] + x[2] * x[3]) % 3
Bf = lambda x, y: (2 * x[0] * y[0] + 2 * x[1] * y[1] + x[2] * y[3] + x[3] * y[2]) % 3
add = lambda a, b: tuple((x + y) % 3 for x, y in zip(a, b))
sub = lambda a, b: tuple((x - y) % 3 for x, y in zip(a, b))
neg = lambda a: tuple((-x) % 3 for x in a)
S = [v for v in V if any(v) and q(v) == 0]
nbs = [set(I[add(V[i], s)] for s in S) for i in range(n)]
ISO = []                                                    # one representative of each of the ten isotropic directions
for s in S:
    if neg(s) not in ISO: ISO.append(s)
key = lambda x, y: (x, y) if x < y else (y, x)
CN = {}                                                     # common neighbours of a non-adjacent pair, sorted
for x in range(n):
    for y in range(x + 1, n):
        if y not in nbs[x]: CN[(x, y)] = sorted(nbs[x] & nbs[y])
# the ten partitions of six positions: masks of weight 3 with bit 0 = 0; state 0 = flat
MASKS = [0] + [m for m in range(64) if not (m & 1) and bin(m).count("1") == 3]


def gridpartner(x, y, z): return I[sub(add(V[x], V[y]), V[z])]


def state_of(x, y, side):
    """index of the state of the pair {x, y} whose partition has `side` (a set of three common neighbours) as one class"""
    c = CN[key(x, y)]; m = sum(1 << i for i, z in enumerate(c) if z in side)
    if m & 1: m ^= 63
    return MASKS.index(m)


def state_type(x, y, s):
    if s == 0: return "flat"
    c = CN[key(x, y)]; m = MASKS[s]
    sep = sum(1 for i, z in enumerate(c) if ((m >> i) ^ (m >> c.index(gridpartner(x, y, z)))) & 1) // 2
    assert sep in (1, 3); return "A" if sep == 3 else "B"


class Problem:
    """CNF over the states of non-adjacent pairs; add_local(X) adds the local problem at the vertex X."""
    def __init__(self):
        self.nv = 0; self.cl = []; self.x = {}; self.done = set()
    def new(self):
        self.nv += 1; return self.nv
    def pair(self, a, b):
        k = key(a, b)
        if k not in self.x:
            vs = [self.new() for _ in MASKS]; self.x[k] = vs
            self.cl.append(list(vs))
            for s, t in itertools.combinations(range(11), 2): self.cl.append([-vs[s], -vs[t]])
        return self.x[k]
    def sepstates(self, a, b, u, w):
        """states of the pair {a, b} that separate its common neighbours u and w"""
        c = CN[key(a, b)]; pu, pw = c.index(u), c.index(w)
        return [s for s in range(11) if ((MASKS[s] >> pu) ^ (MASKS[s] >> pw)) & 1]
    def add_local(self, X, pairfilter=None):
        """pairfilter(a, b) = False leaves out the constraints of the inner pair {a, b} (a sub-problem: a relaxation)"""
        if X in self.done: return
        self.done.add(X)
        NX = sorted(nbs[X])
        for a, b in itertools.combinations(NX, 2):
            if b in nbs[a]: continue
            if pairfilter is not None and not pairfilter(a, b): continue
            xs = self.pair(a, b)
            for R in CN[key(a, b)]:
                if R == X: continue
                # square (X, a, R, b): odd iff {X,R} separates a,b iff {a,b} separates X,R
                xr = self.pair(X, R); s1 = self.sepstates(X, R, a, b); s2 = self.sepstates(a, b, X, R)
                t = self.new()
                for s in range(11):
                    self.cl.append([-xr[s], t] if s in s1 else [-xr[s], -t])
                    self.cl.append([-xs[s], t] if s in s2 else [-xs[s], -t])
    def fix(self, a, b, s): self.cl.append([self.pair(a, b)[s]])
    def forbid_type(self, a, b, typ):
        for s in range(1, 11):
            if state_type(a, b, s) == typ: self.cl.append([-self.pair(a, b)[s]])
    def write(self, path):
        with open(path, "w", newline="\n") as f:
            f.write("p cnf %d %d\n" % (self.nv, len(self.cl)))
            for c in self.cl: f.write(" ".join(map(str, c)) + " 0\n")


def line_solution(Pv, d):
    """states prescribed by the line solution at the vertex Pv in the isotropic direction d (a vector):
    returns {pair: state} for the 60 pairs {Pv, R} and the 180 pairs inside N(Pv)."""
    out = {}
    rel = lambda x: sub(V[x], V[Pv])
    for R in range(n):
        if R == Pv or R in nbs[Pv]: continue
        c = CN[key(Pv, R)]
        if Bf(rel(R), d) == 0: out[key(Pv, R)] = state_of(Pv, R, {z for z in c if Bf(rel(z), d) == 1})
        else: out[key(Pv, R)] = 0
    NX = sorted(nbs[Pv])
    for a, b in itertools.combinations(NX, 2):
        if b in nbs[a]: continue
        fa, fb = Bf(rel(a), d), Bf(rel(b), d)
        if fa and fb and fa != fb: out[key(a, b)] = state_of(a, b, {R for R in CN[key(a, b)] if R != Pv and Bf(rel(R), d) == 0})
        else: out[key(a, b)] = 0
    return out
