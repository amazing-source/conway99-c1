"""R8 route (LAB, 20/10/2026): independent re-implementation of the local model around a vertex.

Setting (srg(v,k,1,2), here k = K letters).  Fix a vertex v.  Its k neighbours ("letters") are paired into k/2 lines
{2i, 2i+1} (lambda = 1).  Every non-neighbour w of v is adjacent to exactly two letters (mu = 2), which are not mates;
w <-> its pair {i, j} ("label") is a bijection onto the non-matching pairs (each non-matching pair {i,j} has exactly one
common neighbour besides v).  Gamma = graph induced on the labels.  L_y = labels containing the letter y.

Necessary conditions (proved in NOTE_R8_ROUTE.md, section 1):
  (C1)  for every label l and letter y: |N(l) n L_y| = c(l,y), with c(l,y) = 1 if y in l or mate(y) in l, else 2.
  (C2)  for every two labels l != l': |l n l'| + |N(l) n N(l')| + [l ~ l'] = 2.
Restricted to a label set S:
  (C1)  exact for the letters y with L_y contained in S ("exact letters");
  (C1') upper bound |N(l) n L_y n S| <= c(l,y) for the other letters;
  (C2') cap |l n l'| + |N(l) n N(l') n S| + [l ~ l'] <= 2.

R8 (K = 14): stars 0,1,2,3 exact; S = L_0 u L_1 u L_2 u L_3 u X, X = {{4,t}: t = 6..13}; letter 4 only bounded.
The edge variable of the pair (i, j), i < j indices in S, is number 1 + position of (i, j) in
itertools.combinations(range(n), 2)  (same numbering as stars_rank_2026-10-14/five_cnf.py, so models can be compared).

This file does NOT import the archive code.  Encoding differences with five_cnf.py (deliberate, for independence):
cardinality constraints of (C1)/(C1') by a totalizer-free direct form (binomial at-most, complementary at-least), (C2')
by a k-bounded TOTALIZER on reified products (five_cnf uses a sequential counter)."""
import itertools

MATE = lambda y: y ^ 1


def c_need(l, y):
    return 1 if (y in l or MATE(y) in l) else 2


def all_labels(K):
    return [frozenset((a, b)) for a, b in itertools.combinations(range(K), 2) if b != MATE(a)]


class Model:
    """Label set and constraint lists (pure combinatorics, no CNF)."""

    def __init__(self, K=14, stars=(0, 1, 2, 3), xl=4, nx=None, exact_extra=()):
        self.K = K
        self.stars = tuple(stars)
        self.xl = xl
        base = [l for l in all_labels(K) if any(y in l for y in stars)]
        outer = [t for t in range(K) if t not in stars and t not in (xl, MATE(xl))]
        X = [frozenset((xl, t)) for t in outer if frozenset((xl, t)) not in base]
        if nx is not None:
            X = X[:nx]
        self.B = base
        self.X = X
        self.S = base + X
        self.n = len(self.S)
        self.idx = {l: i for i, l in enumerate(self.S)}
        # exact letters: the stars, plus extra letters whose star is entirely inside S (checked)
        Sset = set(self.S)
        self.exact = set(stars)
        for y in exact_extra:
            Ly = [l for l in all_labels(K) if y in l]
            assert all(l in Sset for l in Ly), "letter %d cannot be exact: L_%d not inside S" % (y, y)
            self.exact.add(y)
        self.pairs = list(itertools.combinations(range(self.n), 2))
        self.pos = {p: k for k, p in enumerate(self.pairs)}

    def var(self, i, j):
        if i > j:
            i, j = j, i
        return 1 + self.pos[(i, j)]

    # ---------- independent checker ----------
    def check(self, edges, extra_exact=(), verbose=False):
        """edges: iterable of (i, j) index pairs.  Returns list of violations of C1 (exact letters + extra_exact),
        C1' and C2' (inside S)."""
        n, S = self.n, self.S
        adj = [[0] * n for _ in range(n)]
        for i, j in edges:
            assert i != j
            adj[i][j] = adj[j][i] = 1
        ex = set(self.exact) | set(extra_exact)
        bad = []
        for i, l in enumerate(S):
            for y in range(self.K):
                cnt = sum(adj[i][j] for j in range(n) if j != i and y in S[j])
                c = c_need(l, y)
                if cnt > c or (y in ex and cnt != c):
                    bad.append(("C1", tuple(sorted(l)), y, cnt, c))
        for i, j in self.pairs:
            com = sum(1 for t in range(n) if adj[i][t] and adj[j][t])
            if len(S[i] & S[j]) + com + adj[i][j] > 2:
                bad.append(("C2", tuple(sorted(S[i])), tuple(sorted(S[j])), com, adj[i][j]))
        return bad


class CNF:
    """Clause container.  With stream=<path>, clauses are written to the file at once (not kept in memory) and
    close() rewrites the fixed-width header; len_clauses() gives the count in both modes."""

    def __init__(self, nvars=0, stream=None):
        self.n = nvars
        self.clauses = []
        self.count = 0
        self.fh = None
        if stream:
            self.fh = open(stream, "w")
            self.fh.write("p cnf %-12d %-12d\n" % (0, 0))

    def new(self):
        self.n += 1
        return self.n

    def add(self, c):
        self.count += 1
        if self.fh:
            self.fh.write(" ".join(map(str, c)) + " 0\n")
        else:
            self.clauses.append(list(c))

    def len_clauses(self):
        return self.count

    def close(self):
        if self.fh:
            self.fh.seek(0)
            self.fh.write("p cnf %-12d %-12d\n" % (self.n, self.count))
            self.fh.close()
            self.fh = None

    def write(self, path, comments=()):
        with open(path, "w") as fh:
            for cm in comments:
                fh.write("c %s\n" % cm)
            fh.write("p cnf %d %d\n" % (self.n, len(self.clauses)))
            for c in self.clauses:
                fh.write(" ".join(map(str, c)) + " 0\n")


def at_most(F, lits, c):
    for sub in itertools.combinations(lits, c + 1):
        F.add([-x for x in sub])


def at_least(F, lits, c):
    # at least c of m literals  <=>  every (m - c + 1)-subset contains a true literal
    m = len(lits)
    if c <= 0:
        return
    if c > m:
        F.add([])
        return
    for sub in itertools.combinations(lits, m - c + 1):
        F.add(list(sub))


def totalizer_upper(F, lits, kmax):
    """Totalizer (Bailleux-Boufkhad) truncated at kmax+1, only the 'sum >= j  =>  o_j' direction.
    Returns outputs o[1..kmax+1] (o[j] is forced true whenever at least j inputs are true)."""
    K1 = kmax + 1

    def build(ls):
        if len(ls) == 1:
            return [ls[0]]
        h = len(ls) // 2
        a, b = build(ls[:h]), build(ls[h:])
        m = min(len(a) + len(b), K1)
        out = [F.new() for _ in range(m)]
        # a_i (sum >= i) and b_j (sum >= j)  =>  out_{i+j}
        for i in range(0, len(a) + 1):
            for j in range(0, len(b) + 1):
                s = i + j
                if s == 0:
                    continue
                s = min(s, m)
                cl = []
                if i > 0:
                    cl.append(-a[i - 1])
                if j > 0:
                    cl.append(-b[j - 1])
                cl.append(out[s - 1])
                F.add(cl)
        return out

    return build(list(lits))


def encode(M, implied=(), five=False, stream=None):
    """CNF of the model M.  implied: subset of
         'L4B'   letter-4 exactness on the base B (PROVED consequence of R8, capacity lemma);
         'XPAIR' cardinality form of the X-pair bound (PROVED consequence of the C2' caps; see note);
       five=True adds the exactness of the X letter on X (the five-star problem; sound for Conway, NOT implied by R8).
    stream=<path>: write the clauses to that file directly (call F.close() afterwards).
    Returns (F, info)."""
    n, S = M.n, M.S
    F = CNF(len(M.pairs), stream=stream)
    e = M.var
    xl = M.xl
    exact = set(M.exact)
    # (C1) / (C1')
    for i, l in enumerate(S):
        for y in range(M.K):
            lits = [e(i, j) for j in range(n) if j != i and y in S[j]]
            if not lits:
                continue
            c = c_need(l, y)
            at_most(F, lits, c)
            if y in exact:
                at_least(F, lits, c)
    # (C2') caps with reified products and a truncated totalizer
    for i, j in M.pairs:
        s = len(S[i] & S[j])
        prods = []
        for t in range(n):
            if t in (i, j):
                continue
            p = F.new()
            F.add([-e(i, t), -e(j, t), p])
            F.add([-p, e(i, t)])
            F.add([-p, e(j, t)])
            prods.append(p)
        eij = e(i, j)
        if s == 1:
            # edge: no common label neighbour (direct triangle clauses); non-edge: at most one
            for t in range(n):
                if t not in (i, j):
                    F.add([-eij, -e(i, t), -e(j, t)])
            o = totalizer_upper(F, prods, 1)
            F.add([eij, -o[1]])            # not edge  =>  not (>= 2)
        else:
            o = totalizer_upper(F, prods, 2)
            F.add([-eij, -o[1]])           # edge      =>  not (>= 2)
            F.add([eij, -o[2]])            # not edge  =>  not (>= 3)
    info = {"edge_vars": len(M.pairs)}
    full_X = all(frozenset((xl, t)) in set(S) for t in range(M.K) if t != xl and t != MATE(xl))
    if "L4B" in implied:
        assert full_X and xl not in exact
        for i, l in enumerate(M.B):
            lits = [e(i, j) for j in range(n) if j != i and xl in S[j]]
            at_least(F, lits, c_need(l, xl))
    if "XPAIR" in implied:
        assert full_X
        # B' = base labels avoiding xl and mate(xl); C4 = base labels containing xl.  For y in B' let z_y <-> (y has no
        # neighbour in C4).  Claim (PROVED in the note, uses L4B): sum_y z_y + #edges inside X <= C(|X|, 2).
        Bp = [i for i, l in enumerate(S[:len(M.B)]) if xl not in l and MATE(xl) not in l]
        C4 = [i for i, l in enumerate(S[:len(M.B)]) if xl in l]
        Xi = list(range(len(M.B), n))
        zs = []
        for y in Bp:
            z = F.new()
            # z -> no C4 neighbour ; (no C4 neighbour) -> z
            for c in C4:
                F.add([-z, -e(y, c)])
            F.add([z] + [e(y, c) for c in C4])
            zs.append(z)
        xe = [e(a, b) for a, b in itertools.combinations(Xi, 2)]
        bound = len(Xi) * (len(Xi) - 1) // 2
        o = totalizer_upper(F, zs + xe, bound)
        F.add([-o[bound]])                 # o[j-1] <=> 'at least j'; forbid 'at least bound+1'
    if five:
        assert full_X
        for i in range(len(M.B), n):
            lits = [e(i, j) for j in range(n) if j != i and xl in S[j]]
            at_least(F, lits, c_need(S[i], xl))
    info["vars"], info["clauses"] = F.n, F.len_clauses()
    return F, info


# ---------- the letter group of R8 (K = 14) ----------
def r8_group(K=14):
    """All letter permutations that preserve the lines, map {0,1,2,3} onto itself, fix 4 and 5, and permute the outer
    lines {6,7}, ..., {K-2, K-1} (hyperoctahedral group).  Order 8 * 2^m m! (3072 for K = 14)."""
    star_maps = []
    for sl in (False, True):
        for s0 in (False, True):
            for s1 in (False, True):
                g = {0: 0, 1: 1, 2: 2, 3: 3}
                if s0:
                    g[0], g[1] = 1, 0
                if s1:
                    g[2], g[3] = 3, 2
                if sl:
                    g = {a: {0: 2, 1: 3, 2: 0, 3: 1}[b] for a, b in g.items()}
                star_maps.append(g)
    outer = [(a, a + 1) for a in range(6, K, 2)]
    m = len(outer)
    group = []
    for s_ in star_maps:
        for perm in itertools.permutations(range(m)):
            for flips in itertools.product((0, 1), repeat=m):
                g = dict(s_)
                g[4], g[5] = 4, 5
                for q, (a, b) in enumerate(outer):
                    c, d = outer[perm[q]]
                    if flips[q]:
                        c, d = d, c
                    g[a], g[b] = c, d
                group.append(g)
    return group


def label_perm(M, g):
    """Permutation of label indices induced by the letter map g (must preserve S)."""
    return [M.idx[frozenset(g[y] for y in l)] for l in M.S]


def var_perm(M, g):
    """sigma on edge variables: sigma[v] = variable of the image pair."""
    lp = label_perm(M, g)
    sig = [0] * (len(M.pairs) + 1)
    for (i, j) in M.pairs:
        sig[M.var(i, j)] = M.var(lp[i], lp[j])
    return sig
