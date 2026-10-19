"""C1, lab session, 2026-10-08. An INDEPENDENT census of induced subgraphs of a srg(v,k,1,2), by recursion instead of
elimination. Written without Codex's code; used to audit its census (notes 181, 182, 184) and to go one order further
on a few targeted types.

  python -I census2.py types <max order>                 number of admissible types per order (expect 2 4 9 21 62 208 916 5311)
  python -I census2.py census <max order> [v k] [out.json] [nocheck]   all type counts as affine forms; self-checks
      ("nocheck": the C(v, n) check and the automorphism orders are skipped at the top order, to stay within the time bound;
       the JSON then stores the EMBEDDING counts x_H of the top order with aut = null)

Graphs: n <= 10 vertices, adjacency rows as bit masks. Admissible = adjacent vertices have at most 1 common neighbour,
non-adjacent ones at most 2 (inside the subgraph).
Unknowns: x_H = number of EMBEDDINGS (injective maps preserving adjacency and non-adjacency) of the type H = N_H |Aut H|.
Identities (exact double counts), for a labelled graph G on m vertices and a set S of at most two of its vertices:
    sum over admissible S' containing S of x_(G + S') = c(S) x_G,
    c(empty) = v - m,  c({i}) = k - deg_G(i),  c({i,j}) = (1 if i ~ j else 2) - |N_G(i) cap N_G(j)|,
where G + S' is G plus one new vertex adjacent exactly to S'.
Recursion: a type H with a vertex u of degree <= 2 is written H = G + S with G = H - u, S = N(u), and
    x_H = c(S) x_G - sum over admissible S' strictly containing S of x_(G + S');
every term on the right has fewer vertices or more edges. Types of minimum degree >= 3 are left as parameters (their
unlabelled counts N_H). Only one identity per type is used; the others are consistency checks (some are run below).
Canonical form: colour refinement, then individualisation of the first non-singleton cell with a twin shortcut; the
key is the smallest upper-triangular adjacency string over the leaves. One process; memory well below 1 GB."""
import sys, json, time, itertools
from fractions import Fraction as Fr


def refine(n, rows, colour):
    while True:
        sig = [(colour[v], tuple(sorted(colour[u] for u in range(n) if rows[v] >> u & 1))) for v in range(n)]
        rank = {s: i for i, s in enumerate(sorted(set(sig)))}; new = [rank[s] for s in sig]
        if len(rank) == len(set(colour)): return new
        colour = new


def canon(n, rows):
    """(key, perm): key = canonical adjacency string as an int; perm[p] = original vertex placed at position p."""
    best = [None, None]
    def rec(colour):
        colour = refine(n, rows, colour); cnt = {}
        for c in colour: cnt[c] = cnt.get(c, 0) + 1
        if len(cnt) == n:
            perm = sorted(range(n), key=lambda v: colour[v]); code = 0
            for i in range(n):
                ri = rows[perm[i]]
                for j in range(i + 1, n): code = code << 1 | (ri >> perm[j] & 1)
            if best[0] is None or code < best[0]: best[0] = code; best[1] = perm
            return
        target = min(c for c, m in cnt.items() if m > 1); cell = [v for v in range(n) if colour[v] == target]; seen = []
        for v in cell:
            if any((rows[v] & ~(1 << w)) == (rows[w] & ~(1 << v)) for w in seen): continue   # the transposition (v w) is an automorphism
            seen.append(v); rec([2 * colour[u] + (0 if u == v else 1) for u in range(n)])
    rec([0] * n); return best[0], best[1]


def relabel(n, rows, perm):
    pos = [0] * n
    for p, v in enumerate(perm): pos[v] = p
    out = [0] * n
    for v in range(n):
        r = rows[v]; acc = 0
        while r:
            low = r & -r; r ^= low; acc |= 1 << pos[low.bit_length() - 1]
        out[pos[v]] = acc
    return tuple(out)


def aut_order(n, rows):
    colour = refine(n, rows, [0] * n); img = [0] * n; cnt = [0]
    def rec(t, used):
        if t == n: cnt[0] += 1; return
        for w in range(n):
            if used >> w & 1 or colour[w] != colour[t]: continue
            ok = True
            for s in range(t):
                if (rows[t] >> s & 1) != (rows[w] >> img[s] & 1): ok = False; break
            if ok: img[t] = w; rec(t + 1, used | 1 << w)
    rec(0, 0); return cnt[0]


def admissible_sets(m, rows, base=0):
    """all S' (bit masks over the m vertices) containing base such that G + S' is admissible."""
    cn = [[bin(rows[i] & rows[j]).count("1") for j in range(m)] for i in range(m)]; out = []
    def ok(S):
        for j in range(m):
            c = bin(S & rows[j]).count("1")
            if c > (1 if S >> j & 1 else 2): return False
        mem = [i for i in range(m) if S >> i & 1]
        for a in range(len(mem)):
            for b in range(a + 1, len(mem)):
                i, j = mem[a], mem[b]
                if cn[i][j] + 1 > (1 if rows[i] >> j & 1 else 2): return False
        return True
    free = [i for i in range(m) if not base >> i & 1]
    def rec(idx, S):
        if not ok_partial(S): return
        if idx == len(free):
            if ok(S): out.append(S)
            return
        rec(idx + 1, S); rec(idx + 1, S | 1 << free[idx])
    def ok_partial(S):                                                   # necessary conditions that only get worse when S grows
        for j in range(m):
            if bin(S & rows[j]).count("1") > 2: return False
        return True
    rec(0, base); return out


def extend(m, rows, S):
    new = [rows[i] | ((1 << m) if S >> i & 1 else 0) for i in range(m)]; new.append(S); return new


class Census:
    def __init__(self, v, k):
        self.v, self.k = v, k; self.types = {1: {0: (0,)}}             # order -> key -> canonical rows
        self.x = {(1, 0): {0: Fr(v)}}                                    # (order, key) -> affine form {param id: coefficient}; param 0 is the constant
        self.params = []                                                 # (order, key) of the minimum-degree-3 types, param id = index + 1
        self.aut = {}

    def key(self, n, rows):
        code, perm = canon(n, rows); return code, relabel(n, rows, perm)

    def generate(self, n):
        out = {}
        for key, rows in self.types[n - 1].items():
            for S in admissible_sets(n - 1, rows):
                code, perm = canon(n, extend(n - 1, rows, S))
                if code not in out: out[code] = relabel(n, extend(n - 1, rows, S), perm)
        self.types[n] = out

    def autn(self, n, key):
        if (n, key) not in self.aut: self.aut[(n, key)] = aut_order(n, self.types[n][key])
        return self.aut[(n, key)]

    def solve_order(self, n):
        items = sorted(self.types[n].items(), key=lambda kv: -sum(bin(r).count("1") for r in kv[1]))   # denser first
        for key, rows in items:
            deg = [bin(r).count("1") for r in rows]; u = min(range(n), key=lambda i: deg[i])
            if deg[u] >= 3:
                self.params.append((n, key)); self.x[(n, key)] = {len(self.params): Fr(self.autn(n, key))}; continue
            self.x[(n, key)] = self.resolve(n, rows, u)

    def resolve(self, n, rows, u):
        """x of the labelled graph `rows` through its vertex u of degree <= 2."""
        keep = [i for i in range(n) if i != u]; pos = {i: p for p, i in enumerate(keep)}; m = n - 1
        g = [0] * m
        for i in keep:
            r = rows[i] & ~(1 << u); acc = 0
            while r:
                low = r & -r; r ^= low; acc |= 1 << pos[low.bit_length() - 1]
            g[pos[i]] = acc
        S = 0
        for i in keep:
            if rows[u] >> i & 1: S |= 1 << pos[i]
        mem = [i for i in range(m) if S >> i & 1]
        if len(mem) == 0: c = self.v - m
        elif len(mem) == 1: c = self.k - bin(g[mem[0]]).count("1")
        else: c = (1 if g[mem[0]] >> mem[1] & 1 else 2) - bin(g[mem[0]] & g[mem[1]]).count("1")
        gk, _ = canon(m, g); acc = {p: c * val for p, val in self.x[(m, gk)].items()}
        for S2 in admissible_sets(m, g, S):
            if S2 == S: continue
            hk, _ = canon(n, extend(m, g, S2))
            for p, val in self.x[(n, hk)].items(): acc[p] = acc.get(p, 0) - val
        return {p: val for p, val in acc.items() if val}

    def count(self, n, key):
        """unlabelled count N_H as an affine form."""
        a = self.autn(n, key); return {p: val / a for p, val in self.x[(n, key)].items()}


def show(form, names):
    return " + ".join("%s%s" % (val, "" if p == 0 else " " + names[p]) for p, val in sorted(form.items())) or "0"


if __name__ == "__main__":
    what = sys.argv[1]; nmax = int(sys.argv[2]); t0 = time.time()
    v, k = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (99, 14)
    C = Census(v, k)
    for n in range(2, nmax + 1):
        C.generate(n); print("order %d: %d admissible types  [%.0f s]" % (n, len(C.types[n]), time.time() - t0), flush=True)
    if what == "census":
        for n in range(2, nmax + 1):
            before = len(C.params); C.solve_order(n)
            print("order %d solved: %d new parameters (minimum degree >= 3)  [%.0f s]" % (n, len(C.params) - before, time.time() - t0), flush=True)
        names = {i + 1: "N%d_%d" % nk for i, nk in enumerate(C.params)}
        from math import comb
        nocheck = "nocheck" in sys.argv
        for n in range(2, nmax + (0 if nocheck else 1)):                 # check: the type counts add up to C(v, n)
            tot = {}
            for key in C.types[n]:
                for p, val in C.count(n, key).items(): tot[p] = tot.get(p, 0) + val
            tot = {p: val for p, val in tot.items() if val}
            assert tot == {0: Fr(comb(v, n))}, (n, tot)
        print("check passed: for every order the type counts sum to C(v, n) identically in the parameters")
        if nmax >= 6:
            by = {}
            for key, rows in C.types[6].items():
                e = sum(bin(r).count("1") for r in rows) // 2
                for p, val in C.count(6, key).items(): by.setdefault(e, {}); by[e][p] = by[e].get(p, 0) + val
            for e in (9, 8, 7, 6): print("  N(6,%d) = %s" % (e, show({p: val for p, val in by[e].items() if val}, names)))
        if len(sys.argv) > 5:
            out = {"v": v, "k": k, "params": [[n, key, list(C.types[n][key])] for n, key in C.params],
                   "types": {str(n): [[key, list(rows), (None if (nocheck and n == nmax) else C.autn(n, key)), {str(p): str(val) for p, val in C.x[(n, key)].items()}] for key, rows in C.types[n].items()] for n in range(2, nmax + 1)}}
            json.dump(out, open(sys.argv[5], "w")); print("written %s  [%.0f s]" % (sys.argv[5], time.time() - t0))
