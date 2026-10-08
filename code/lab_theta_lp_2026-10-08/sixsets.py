"""C1, lab session, 2026-10-08. The 6-subsets W with 7, 8 or 9 edges in a graph with lambda = 1, mu = 2: types and counts.

  python -I sixsets.py abstract                 the admissible abstract graphs on 6 vertices with 7, 8, 9 edges
  python -I sixsets.py rook                     all 6-subsets of the 3 x 3 rook's graph, srg(9,4,1,2)
  python -I sixsets.py <edge file> [n_edges_tested]   srg(v,k,1,2): the 6-subsets containing a fixed edge (first edges of
                                                the file), N = (#edges) * count / e if the graph is edge-transitive

Why: for a hypothetical srg(99,14,1,2), psi = 1_W with |W| = 6 has Q(psi) = 22 - 2 e(W) in M (class s = 6), and two distinct
6-sets give the same vector of M only if they are disjoint prisms (a 0/+-1 integer 3-eigenvector needs minimum degree 3 on
its positive support). So the numbers N(6,e) of 6-sets with e <= 8 edges are lower bounds: b_(11-e) >= 2 N(6,e) + (classes
s = 0, +-3). The formulas in (v, k, P), P = number of prisms, are derived by hand in NOTE.md; this script tests them on the
only available graphs of the family (k = 4 and k = 22). Memory: a few MB. One process."""
import sys, itertools
from math import comb


def inv(S, adj):
    S = list(S); deg = {v: len(adj[v] & set(S)) for v in S}; Sset = set(S)
    e = sum(deg.values()) // 2
    tri = sum(1 for a, b, c in itertools.combinations(S, 3) if b in adj[a] and c in adj[a] and c in adj[b])
    return e, tri, tuple(sorted((deg[v], tuple(sorted(deg[u] for u in adj[v] & Sset))) for v in S))


def name(S, adj):
    e, tri, prof = inv(S, adj); degs = tuple(sorted((d for d, _ in prof), reverse=True)); Sset = set(S)
    if e == 7:
        if degs == (5, 2, 2, 2, 2, 1): return "T1 bowtie + pendant at the centre"
        if degs == (4, 3, 2, 2, 2, 1): return "T2 bowtie + pendant elsewhere" if tri == 2 else "T6 house + pendant at the shared edge"
        if degs == (4, 2, 2, 2, 2, 2) and tri == 1: return "T3 triangle and 4-cycle sharing a vertex"
        if degs == (3, 3, 2, 2, 2, 2):
            if tri == 2: return "T4 two triangles joined by an edge"
            if tri == 1: return "T8 triangle and 5-cycle sharing an edge"
            a, b = [v for v in S if len(adj[v] & Sset) == 3]
            return "T9 two 4-cycles sharing an edge" if b in adj[a] else "T10 4-cycle and 5-cycle sharing a 2-path"
        if degs == (3, 3, 3, 2, 2, 1) and tri == 1:
            (p,) = [v for v in S if len(adj[v] & Sset) == 1]; (q,) = adj[p] & Sset
            intri = any(b in adj[a] for a, b in itertools.combinations(sorted(adj[q] & Sset), 2))
            return "T5 house + pendant at the apex" if intri else "T7 house + pendant at the far side"
    if e == 8:
        if degs == (3, 3, 3, 3, 2, 2) and tri == 2: return "U1 two triangles joined by two edges"
        if degs == (4, 3, 3, 2, 2, 2) and tri == 2: return "U2 bowtie + common neighbour of two outer vertices"
        if degs == (3, 3, 3, 3, 2, 2) and tri == 1: return "U3 triangle with 4-cycles on two of its edges, sharing an edge"
    if e == 9 and degs == (3,) * 6 and tri == 2: return "prism"
    return "OTHER %s" % (inv(S, adj),)


def formulas(v, k, P):
    T = v * k // 6; E = v * k // 2; H = E * (k - 2); B = v * comb(k // 2, 2); NA = v * (v - k - 1) // 2
    return {"T1": B * (k - 4), "T2": 4 * B * (k - 4), "T3": v * (k // 2) * (comb(k - 2, 2) - (k - 2) // 2),
            "T4": T * 3 * (k - 2) * (k - 6) // 4 + 3 * P, "T5": H * (k - 4) + 6 * P, "T6": 2 * H * (k - 4),
            "T7": 2 * H * (k - 5) + 12 * P, "T8": T * 3 * (k - 2) * (2 * k - 9) + 6 * P, "T9": E * (k - 2) * (k - 5) // 2 + 3 * P,
            "T10": NA * (2 * k - 10) + 6 * P, "U1": T * 3 * (k - 2) // 2 - 3 * P, "U2": 4 * B, "U3": H - 6 * P, "prism": P}


def load(arg):
    if arg == "rook":
        V = [(i, j) for i in range(3) for j in range(3)]; E = [(a, b) for a in range(9) for b in range(a + 1, 9) if (V[a][0] == V[b][0]) != (V[a][1] == V[b][1])]
    else: E = [tuple(int(x) for x in l.split()[:2]) for l in open(arg) if l.strip()]
    n = 1 + max(max(e) for e in E); adj = [set() for _ in range(n)]
    for a, b in E: adj[a].add(b); adj[b].add(a)
    k = len(adj[0]); assert all(len(s) == k for s in adj)
    for a in range(n):
        for b in range(a + 1, n): assert len(adj[a] & adj[b]) == (1 if b in adj[a] else 2)
    tris = {frozenset((a, b, c)) for a, b in E for c in adj[a] & adj[b]}; assert len(tris) == n * k // 6
    P2 = 0                                                               # ordered pairs of triangles forming a prism
    for T in tris:
        a, b, c = sorted(T)
        for x in adj[a] - T:
            for y in adj[x] & adj[b]:
                if y in T: continue
                for z in adj[x] & adj[y] & adj[c]: P2 += 1
    assert P2 % 2 == 0
    return n, k, E, adj, P2 // 2


def report(tally, scale, v, k, P):
    F = formulas(v, k, P); ok = True
    for nm in sorted(tally, key=lambda s: (s[0] != "T", s)):
        key = nm.split()[0]; val = tally[nm] * scale
        exp = F.get(key); flag = "" if exp is None else ("  formula %d  %s" % (exp, "OK" if exp == val else "MISMATCH")); ok = ok and (exp is None or exp == val)
        print("  %-55s %s%s" % (nm, val, flag))
    for key, exp in F.items():
        if exp and not any(nm.split()[0] == key for nm in tally): print("  %-55s 0  formula %d  MISMATCH" % (key, exp)); ok = False
    return ok


if __name__ == "__main__":
    what = sys.argv[1]
    if what == "abstract":
        pairs = list(itertools.combinations(range(6), 2)); seen = {}
        for e in (7, 8, 9):
            for es in itertools.combinations(pairs, e):
                adj = [set() for _ in range(6)]
                for a, b in es: adj[a].add(b); adj[b].add(a)
                if any(len(adj[a] & adj[b]) > (1 if b in adj[a] else 2) for a, b in pairs): continue
                nm = name(range(6), adj); seen[(e, nm)] = seen.get((e, nm), 0) + 1
        for (e, nm), c in sorted(seen.items()): print("e = %d: %-60s labelled copies %d (720/%d)" % (e, nm, c, 720 // c))
    elif what == "rook":
        n, k, E, adj, P = load("rook"); tally = {}
        for S in itertools.combinations(range(n), 6):
            e = sum(1 for a, b in itertools.combinations(S, 2) if b in adj[a])
            if e >= 7: nm = name(S, adj); tally[nm] = tally.get(nm, 0) + 1
        print("rook 3 x 3: v = %d, k = %d, prisms P = %d; 6-sets with >= 7 edges by type:" % (n, k, P)); print("all formulas agree" if report(tally, 1, n, k, P) else "DISAGREEMENT")
    else:
        n, k, E, adj, P = load(what); ne = int(sys.argv[2]) if len(sys.argv) > 2 else 2
        mask = [sum(1 << u for u in adj[v]) for v in range(n)]; results = []
        for (a, b) in [E[0], E[len(E) // 2], E[-1], E[len(E) // 3]][:ne]:
            tally = {}; total = [0]
            def rec(S, Sm, e, ext, forb):
                if len(S) == 6:
                    total[0] += 1
                    if e >= 7: nm = name(S, adj); tally[nm] = tally.get(nm, 0) + 1
                    return
                while ext:
                    low = ext & -ext; ext ^= low; v = low.bit_length() - 1
                    e2 = e + bin(mask[v] & Sm).count("1")
                    if e2 + 3 * (5 - len(S)) >= 7:                        # a new vertex brings at most 3 edges (no K4, no K_{2,3})
                        rec(S + [v], Sm | low, e2, ext | (mask[v] & ~Sm & ~forb & ~low), forb | low)
                    forb |= low
            Sm = (1 << a) | (1 << b); rec([a, b], Sm, 1, (mask[a] | mask[b]) & ~Sm, Sm)
            results.append((a, b, dict(tally), total[0])); print("edge (%d,%d): connected 6-sets visited %d; with >= 7 edges: %s" % (a, b, total[0], sorted(tally.items())), flush=True)
        assert all(r[2] == results[0][2] for r in results), "the tested edges give different counts: not edge-transitive"
        print("v = %d, k = %d, prisms P = %d; N(type) = (#edges) * count / e (edge-transitive graph):" % (n, k, P)); tally = results[0][2]; ok = True
        scaled = {}
        for nm, c in tally.items():
            e = 7 if nm[0] == "T" else 8 if nm[0] == "U" else 9 if nm == "prism" else int(nm.split("(")[1].split(",")[0])
            assert (len(E) * c) % e == 0; scaled[nm] = len(E) * c // e
        print("all formulas agree" if report(scaled, 1, n, k, P) else "DISAGREEMENT")
