"""C1, lab session, 2026-10-09, mandate B. Does a graph with lambda = 1, mu = 2 admit a cyclic orientation of all its
lines such that in every quadrangle the opposite sides are oriented in parallel (c = 0), or in every quadrangle
anti-parallel (c = 1)?  Linear system over F_2: one unknown per line, one equation per (quadrangle, pair of opposite
sides).   python parallel_orient.py <data folder>     One process, seconds."""
import sys, os, json, collections
D = sys.argv[1]


def solve(rows, rhs, nv):
    """Gaussian elimination over F_2 with bitmasks; returns (consistent, rank)"""
    piv = {}
    for r, b in zip(rows, rhs):
        m = r | (b << nv)
        while m & ((1 << nv) - 1):
            h = (m & ((1 << nv) - 1)).bit_length() - 1
            if h in piv: m ^= piv[h]
            else: piv[h] = m; break
        else:
            if m >> nv: return False, len(piv)
    return True, len(piv)


def study(name, n, E):
    adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    third = {}
    for a, b in E:
        t = next(iter(adj[a] & adj[b])); third[(a, b)] = third[(b, a)] = t
    lines = sorted({tuple(sorted((a, b, third[(a, b)]))) for a, b in E}); lid = {}
    for i, L in enumerate(lines):
        for x in L: lid[(x, tuple(y for y in L if y != x))] = i
    line_of = lambda a, b: lid[(a, tuple(sorted((b, third[(a, b)]))))]
    # reference direction of the arc a -> b inside its line (sorted a0 < a1 < a2, reference cycle a0 -> a1 -> a2 -> a0)
    def ref(a, b):
        L = lines[line_of(a, b)]; return 0 if (L.index(b) - L.index(a)) % 3 == 1 else 1
    rows = []; base = []
    for v in range(n):
        for w in range(v + 1, n):
            if w in adj[v] or not (adj[v] & adj[w]): continue
            a, b = sorted(adj[v] & adj[w])
            if (v, w) > (a, b): continue
            # quadrangle v-a-w-b: opposite sides (v->a, b->w) and (v->b, a->w)
            for (p, q, r, s) in ((v, a, b, w), (v, b, a, w)):
                rows.append((1 << line_of(p, q)) ^ (1 << line_of(r, s))); base.append(ref(p, q) ^ ref(r, s))
    out = []
    for c in (0, 1):
        ok, rk = solve(rows, [x ^ c for x in base], len(lines)); out.append((ok, rk))
    print("%-18s lines %4d, equations %6d | parallel orientation exists: %s | anti-parallel exists: %s | rank %d"
          % (name, len(lines), len(rows), out[0][0], out[1][0], out[0][1]))


V3 = [(i, j) for i in range(3) for j in range(3)]; ix = {v: i for i, v in enumerate(V3)}
study("grid 3x3", 9, [(ix[a], ix[b]) for a in V3 for b in V3 if a < b and ((a[0] == b[0]) != (a[1] == b[1]))])
for g in ("t2_twisted", "t2_untwisted", "t3_twisted", "t3_twisted_42"):
    A = json.load(open(os.path.join(D, g + ".json"))); m = len(A)
    study(g, m, [(i, j) for i in range(m) for j in range(i + 1, m) if A[i][j]])
for g in ("bvls243", "twin243_switched"):
    study(g, 243, [tuple(map(int, l.split())) for l in open(os.path.join(D, "srg243", g + ".edges")) if l.strip()])
