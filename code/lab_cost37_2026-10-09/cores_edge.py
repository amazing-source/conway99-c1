"""C1, lab session, 2026-10-10. Cores of the integral (-4)-eigenvectors of norm 2m (m = 9, 10) with ONE EDGE in each
support (Codex's notes 171, 176: the supports P, Q are independent or contain exactly one edge each, the same number).

P has the edge p1 p2, Q the edge q1 q2. Degrees towards the other support: 5 for the four ends, 4 otherwise.
The third vertex of the triangle on p1 p2 lies in Q and that of q1 q2 in P (|x(T)| <= 1 for every triangle, note 176).
Conditions on the 2m core vertices (lambda = 1, mu = 2 inside the core): an adjacent pair has at most one common
neighbour in the core, a non-adjacent pair at most two; p1, p2 have exactly one common neighbour in Q; q1, q2 exactly
one in P.
As a block system: points = P, blocks = the neighbourhoods in P of the vertices of Q: m blocks, two of size 5 (q1, q2)
and m - 2 of size 4; the points p1 = 0, p2 = 1 lie in 5 blocks, the others in 4; the pair {0,1} lies in exactly one
block, any other pair in at most two; two blocks share at most 2 points, the two blocks of size 5 exactly one; and the
conditions on the mixed pairs are checked on the explicit core graph at the leaves.

Method: as in cores1820.py. Blocks in lexicographic order through the least unsaturated point; the five blocks through
the point 0 are restricted to one representative of every type (the type of the link: which pairs of the five blocks
share a point, their sizes, which one contains the point 1), which loses no isomorphism class because the points
2..m-1 can be renamed freely. Leaves are classified by an invariant and an explicit isomorphism test.

python cores_edge.py <m> [output json]        One process."""
import sys, itertools, json, time
from collections import defaultdict
from cores1820 import popc, pair_matrix, isomorphisms, dual

def link_representatives(m):
    """one representative (5 blocks through the point 0) of every type"""
    reps = {}; pairs5 = list(itertools.combinations(range(5), 2))
    for emask in range(1 << 10):
        H = [pairs5[i] for i in range(10) if (emask >> i) & 1]; deg = [sum(1 for e in H if v in e) for v in range(5)]
        for big in [()] + [(a,) for a in range(5)] + list(itertools.combinations(range(5), 2)):
            size = [5 if v in big else 4 for v in range(5)]
            if len(big) == 2 and tuple(sorted(big)) in H: pass          # two blocks of size 5 through 0 sharing another point: they would share 2 points
            for marked in range(5):
                singles = [size[v] - 1 - deg[v] - (1 if v == marked else 0) for v in range(5)]
                if min(singles) < 0: continue
                if len(big) == 2 and tuple(sorted(big)) in H: continue  # the two 5-blocks must share exactly one point (the point 0 here)
                used = 1 + len(H) + sum(singles)
                if used > m - 1: continue
                best = None
                for perm in itertools.permutations(range(5)):
                    key = (tuple(sorted(tuple(sorted((perm[a], perm[b]))) for a, b in H)), tuple(sorted(perm[v] for v in big)), perm[marked])
                    if best is None or key < best: best = key
                if best in reps: continue
                # explicit representative: point 1 in the marked block, then the shared points, then the single points
                blocks = [1 for _ in range(5)]; nxt = 2
                blocks[marked] |= 1 << 1
                for a, b in H: blocks[a] |= 1 << nxt; blocks[b] |= 1 << nxt; nxt += 1
                for v in range(5):
                    for _ in range(singles[v]): blocks[v] |= 1 << nxt; nxt += 1
                assert nxt <= m and all(popc(blocks[v]) == size[v] for v in range(5))
                reps[best] = tuple(blocks)
    return list(reps.values())

def core_ok(sysm, m):
    """the conditions on the 2m core vertices; sysm = blocks (neighbourhoods in P of the vertices of Q)"""
    big = [j for j, b in enumerate(sysm) if popc(b) == 5]
    if len(big) != 2: return False
    n = 2 * m; A = [[0] * n for _ in range(n)]
    A[0][1] = A[1][0] = 1; A[m + big[0]][m + big[1]] = A[m + big[1]][m + big[0]] = 1
    for j, b in enumerate(sysm):
        for p in range(m):
            if (b >> p) & 1: A[p][m + j] = A[m + j][p] = 1
    for u in range(n):
        for v in range(u + 1, n):
            c = sum(1 for w in range(n) if A[u][w] and A[v][w])
            if c > (1 if A[u][v] else 2): return False
    if sum(1 for j in range(m) if A[0][m + j] and A[1][m + j]) != 1: return False
    if sum(1 for p in range(m) if A[p][m + big[0]] and A[p][m + big[1]]) != 1: return False
    return True

def enumerate_systems(m):
    target = [5, 5] + [4] * (m - 2)
    blocks = [sum(1 << p for p in c) for k in (4, 5) for c in itertools.combinations(range(m), k)]
    blocks.sort(key=lambda b: [p for p in range(m) if (b >> p) & 1])
    order = {b: i for i, b in enumerate(blocks)}
    by_min = defaultdict(list)
    for b in blocks: by_min[min(p for p in range(m) if (b >> p) & 1)].append(b)
    pts = {b: [p for p in range(m) if (b >> p) & 1] for b in blocks}
    leaves = []; nodes = [0]
    def cap(u, v): return 1 if (u, v) in ((0, 1), (1, 0)) else 2
    def rec(chosen, deg, pair, last, n5):
        nodes[0] += 1
        x = next((p for p in range(m) if deg[p] < target[p]), None)
        if x is None:
            if len(chosen) == m and n5 == 2 and pair[0][1] == 1 and core_ok(chosen, m): leaves.append(tuple(chosen))
            return
        if len(chosen) == m: return
        full = sum(1 << p for p in range(m) if deg[p] == target[p])
        lastmin = pts[last][0] if last is not None else -1
        for b in by_min[x]:
            if b & full: continue
            if lastmin == x and order[b] <= order[last]: continue
            ps = pts[b]; s5 = len(ps) == 5
            if s5 and n5 == 2: continue
            if any(popc(b & c) > (1 if (s5 and popc(c) == 5) else 2) for c in chosen): continue
            if any(pair[u][v] >= cap(u, v) for u, v in itertools.combinations(ps, 2)): continue
            for p in ps: deg[p] += 1
            for u, v in itertools.combinations(ps, 2): pair[u][v] += 1; pair[v][u] += 1
            rec(chosen + [b], deg, pair, b, n5 + s5)
            for p in ps: deg[p] -= 1
            for u, v in itertools.combinations(ps, 2): pair[u][v] -= 1; pair[v][u] -= 1
    L = link_representatives(m)
    for ts in L:
        chosen = sorted(ts, key=lambda b: order[b]); deg = [0] * m; pair = [[0] * m for _ in range(m)]; ok = True
        for i, b in enumerate(chosen):
            for c in chosen[:i]:
                if popc(b & c) > (1 if popc(b) == 5 and popc(c) == 5 else 2): ok = False
            for p in pts[b]: deg[p] += 1
            for u, v in itertools.combinations(pts[b], 2): pair[u][v] += 1; pair[v][u] += 1
        if not ok or any(pair[u][v] > cap(u, v) for u in range(m) for v in range(u + 1, m)) or any(deg[p] > target[p] for p in range(m)): continue
        rec(chosen, deg, pair, None, sum(1 for b in chosen if popc(b) == 5))
    return leaves, len(L), nodes[0]

def invariant(sysm, m):
    C = pair_matrix(sysm, m)
    deg = [sum((b >> p) & 1 for b in sysm) for p in range(m)]
    prof = tuple(sorted((deg[x], tuple(sorted((C[x][y], deg[y]) for y in range(m) if y != x))) for x in range(m)))
    bi = tuple(sorted((popc(a), tuple(sorted((popc(a & b), popc(b)) for b in sysm if b != a))) for a in sysm))
    return prof, bi

def main():
    m = int(sys.argv[1]); t0 = time.time()
    leaves, nl, nodes = enumerate_systems(m)
    print("m = %d, one edge in each support: link types of the point 0: %d; search nodes %d; labelled leaves %d  [%.0f s]" % (m, nl, nodes, len(leaves), time.time() - t0), flush=True)
    buckets = defaultdict(list); classes = []
    for s in leaves:
        key = invariant(s, m)
        for c in buckets[key]:
            if isomorphisms(s, classes[c]["sys"], m) is not None: classes[c]["leaves"] += 1; break
        else:
            buckets[key].append(len(classes)); classes.append({"sys": s, "leaves": 1})
    print("isomorphism classes (points and blocks permuted independently): %d; invariant buckets %d  [%.0f s]" % (len(classes), len(buckets), time.time() - t0), flush=True)
    out = []; selfdual = 0; nodual = 0; hist = defaultdict(int)
    for i, c in enumerate(classes):
        s = c["sys"]; aut = isomorphisms(s, s, m, count_all=True)
        d = dual(s, m)
        # the dual must be relabelled so that its two points of degree 5 are 0 and 1 before any comparison of invariants (they are label-free), so compare directly
        kd = invariant(d, m); j = next((k for k in buckets.get(kd, []) if isomorphisms(d, classes[k]["sys"], m) is not None), None)
        selfdual += (j == i); nodual += (j is None)
        big = [jj for jj, b in enumerate(s) if popc(b) == 5]
        qstar = next(jj for jj, b in enumerate(s) if (b & 3) == 3)                      # the block containing both ends of the edge of P
        pstar = next(p for p in range(m) if (s[big[0]] >> p) & 1 and (s[big[1]] >> p) & 1)
        typ = ("q* is an end of the edge of Q" if qstar in big else "q* is not an end", "p* is an end of the edge of P" if pstar in (0, 1) else "p* is not an end")
        hist[(typ, aut)] += 1
        B = [[int((b >> p) & 1) for b in s] for p in range(m)]
        out.append({"index": i, "incidence_rows_P_columns_Q": B, "edge_P": [0, 1], "edge_Q": big, "third_vertex_of_the_P_edge_in_Q": qstar, "third_vertex_of_the_Q_edge_in_P": pstar,
                    "automorphisms": aut, "dual_class": j, "leaves": c["leaves"]})
    print("self-dual classes %d; classes whose dual was not found (must be 0): %d; classes up to duality %d" % (selfdual, nodual, (len(classes) + selfdual) // 2))
    print("classes by (position of the third vertices, automorphisms):")
    for k in sorted(hist, key=str): print("   %s: %d" % (k, hist[k]))
    if len(sys.argv) > 2: json.dump({"m": m, "scope": "incidence of the two supports with one edge each; no extension to 99 vertices is claimed", "classes": out}, open(sys.argv[2], "w")); print("written", sys.argv[2])

if __name__ == "__main__":
    main()
