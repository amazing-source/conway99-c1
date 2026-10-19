"""Exact induced-subgraph counts of a hypothetical srg(99,14,1,2), as affine functions of free parameters (LAB 19/10).
Extension equations (Wilbrink-Brouwer / Kovacikova): for every induced copy of a (k-1)-vertex graph F and every set S
of at most 2 of its vertices, the number of outside vertices adjacent to all of S is fixed:
  |S| = 0: 99 - (k-1);  S = {x}: 14 - deg_F(x);  S = {x,y}: (1 if x~y else 2) - |N_F(x) & N_F(y)|.
Summed over labelled embeddings:  sum_{T >= S} aut(F+T) N(F+T) = c_S(F) aut(F) N(F),
where F+T adds a vertex adjacent exactly to T and N counts induced copies.  Only 'locally feasible' graphs occur:
adjacent pairs have <= 1 common neighbour, non-adjacent pairs <= 2 (lambda = 1, mu = 2).  Solved exactly level by level;
an undetermined direction becomes a new free parameter.  Every count must also be >= 0.
usage: python subgraph_counts.py <kmax> <out.json>"""
import json
import sys
from fractions import Fraction as Fr
from itertools import combinations, permutations, product

KMAX, OUT = int(sys.argv[1]), sys.argv[2]
V, DEG, LAM, MU = 99, 14, 1, 2


def adjsets(n, E):
    adj = [set() for _ in range(n)]
    for a, b in E:
        adj[a].add(b); adj[b].add(a)
    return adj


def feasible(n, E):
    adj = adjsets(n, E)
    for a, b in combinations(range(n), 2):
        c = len(adj[a] & adj[b])
        if c > (LAM if b in adj[a] else MU):
            return False
    return True


def invariants(n, adj):
    tri = [sum(1 for b, c in combinations(adj[a], 2) if c in adj[b]) for a in range(n)]
    base = [(len(adj[a]), tri[a]) for a in range(n)]
    inv = [(base[a], tuple(sorted(base[b] for b in adj[a]))) for a in range(n)]
    return inv


def canon(n, E):
    """canonical edge set (min encoding over invariant-respecting relabellings) and automorphism count."""
    adj = adjsets(n, E)
    inv = invariants(n, adj)
    order = sorted(range(n), key=lambda a: inv[a])
    cells, cur = [], [order[0]]
    for a in order[1:]:
        if inv[a] == inv[cur[0]]:
            cur.append(a)
        else:
            cells.append(cur); cur = [a]
    cells.append(cur)
    best, aut = None, 0
    for choice in product(*[permutations(c) for c in cells]):
        seq = [a for c in choice for a in c]          # new label i <- old vertex seq[i]
        pos = {a: i for i, a in enumerate(seq)}
        enc = tuple(sorted(tuple(sorted((pos[a], pos[b]))) for a, b in E))
        if best is None or enc < best:
            best, aut = enc, 1
        elif enc == best:
            aut += 1
    return best, aut


def affine_zero(n):
    return [Fr(0)] * n


class Params:
    def __init__(self):
        self.names = []

    def new(self, name):
        self.names.append(name)
        return len(self.names) - 1


params = Params()
# counts[k][enc] = affine vector [const, p0, p1, ...] (padded on demand)
levels = {1: {(): {'aut': 1, 'N': [Fr(V)]}}}


def pad(vec, n):
    return list(vec) + [Fr(0)] * (n - len(vec))


def solve_level(k):
    prev = levels[k - 1]
    cls = {}                                         # enc -> aut
    rows = []                                        # (coeff dict enc -> int, rhs affine)
    for Fenc, Fd in prev.items():
        n = k - 1
        E = list(Fenc)
        adj = adjsets(n, E)
        ext = {}
        for r in range(n + 1):
            for T in combinations(range(n), r):
                E2 = E + [(t, n) for t in T]
                if not feasible(k, E2):
                    continue
                enc, aut = canon(k, E2)
                cls[enc] = aut
                ext[T] = enc
        for size in range(3):
            for S in combinations(range(n), size):
                if size == 0:
                    c = V - n
                elif size == 1:
                    c = DEG - len(adj[S[0]])
                else:
                    x, y = S
                    c = (LAM if y in adj[x] else MU) - len(adj[x] & adj[y])
                row = {}
                for T, enc in ext.items():
                    if set(S) <= set(T):
                        row[enc] = row.get(enc, 0) + cls[enc]
                rhs = [Fr(c * Fd['aut']) * x for x in Fd['N']]
                rows.append((row, rhs))
    cols = sorted(cls)
    idx = {e: i for i, e in enumerate(cols)}
    npar = len(params.names) + 1
    A = [[Fr(r.get(e, 0)) for e in cols] + [None] for r, _ in rows]
    B = [pad(rhs, npar) for _, rhs in rows]
    m, ncol = len(A), len(cols)
    piv_cols, r0 = [], 0
    for c in range(ncol):
        p = next((r for r in range(r0, m) if A[r][c] != 0), None)
        if p is None:
            continue
        A[r0], A[p] = A[p], A[r0]; B[r0], B[p] = B[p], B[r0]
        inv = 1 / A[r0][c]
        A[r0] = [x * inv if x is not None else None for x in A[r0]]; B[r0] = [x * inv for x in B[r0]]
        for r in range(m):
            if r != r0 and A[r][c] != 0:
                f = A[r][c]
                A[r] = [A[r][i] - f * A[r0][i] if i < ncol else None for i in range(ncol + 1)]
                B[r] = [B[r][i] - f * B[r0][i] for i in range(npar)]
        piv_cols.append(c); r0 += 1
    # consistency rows (all-zero coefficients) must have zero affine rhs
    bad = [B[r] for r in range(r0, m) if any(x != 0 for x in B[r])]
    if bad:
        raise SystemExit('level %d: %d inconsistent/param-constraining rows, e.g. %s' % (k, len(bad), bad[0]))
    free = [c for c in range(ncol) if c not in piv_cols]
    newp = {}
    for c in free:
        newp[c] = params.new('N[%s]' % (cols[c],))
    npar2 = len(params.names) + 1
    sol = {}
    for c in free:
        v = affine_zero(npar2); v[newp[c] + 1] = Fr(1); sol[c] = v
    for r, c in enumerate(piv_cols):
        v = pad(B[r], npar2)
        for f in free:
            if A[r][f] != 0:
                v[newp[f] + 1] -= A[r][f]
        sol[c] = v
    levels[k] = {cols[c]: {'aut': cls[cols[c]], 'N': sol[c]} for c in range(ncol)}
    return len(cols), len(free)


def fmt(v):
    return [str(x) for x in v]


if __name__ == '__main__':
    for k in range(2, KMAX + 1):
        ncls, nfree = solve_level(k)
        print('level %d: %d feasible classes, %d new free parameters (total %d)' % (k, ncls, nfree, len(params.names)))
    out = {'params': params.names,
           'levels': {str(k): [{'edges': list(map(list, enc)), 'aut': d['aut'], 'N': fmt(pad(d['N'], len(params.names) + 1))}
                               for enc, d in lv.items()] for k, lv in levels.items()}}
    json.dump(out, open(OUT, 'w'), indent=0)
    for k in range(2, min(KMAX, 4) + 1):
        for enc, d in levels[k].items():
            print(k, enc, d['aut'], fmt(d['N']))
