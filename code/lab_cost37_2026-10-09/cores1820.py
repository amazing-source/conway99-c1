"""C1, lab session, 2026-10-10. Cores of the integral (-4)-eigenvectors of norm 2m with INDEPENDENT supports, m = 8, 9, 10.

f = 1_P - 1_Q, |P| = |Q| = m, both independent: the incidence B between P and Q has row and column sums 4, two rows
share at most 2 columns and two columns at most 2 rows (lambda = 1, mu = 2; Codex's notes 166, 171, 176).
Equivalently: m blocks of size 4 on m points, every point in 4 blocks, every pair of points in at most 2 blocks, two
blocks meeting in at most 2 points. The script lists these systems up to permutations of the points and of the blocks
(NOT up to the exchange of P and Q, which is reported separately as "dual").

Method. Blocks are added in lexicographic order, always through the least point whose degree is below 4, so every
labelled system is produced once; the first block is {0,1,2,3} and the four blocks through the point 0 are restricted
to one representative of each orbit of the permutations of the other points (their "link": four triples pairwise
sharing at most one point, every point in at most two). Since every system can be relabelled so that the link of its
point 0 is one of the representatives, no isomorphism class is lost. The leaves are then sorted into isomorphism
classes by an invariant and an explicit isomorphism test (backtracking on the points, checked on the block sets).
Control: m = 8 must give the five cores of Codex's note 166, with defect cycles 8, 6+2, 4+4, 4+2+2, 2+2+2+2.

python cores1820.py <m> [output json]        One process; m = 9 about a minute, m = 10 longer (see the output)."""
import sys, itertools, json, time
from collections import defaultdict

def popc(x): return bin(x).count("1")

def links(m):
    """orbit representatives of the triples {T1..T4} (as 4 blocks through the point 0) under permutations of 1..m-1"""
    pts = list(range(1, m)); seen = {}; reps = []
    triples = list(itertools.combinations(pts, 3))
    def canon(ts):
        # the structure is a simple graph on the 4 triples (edges = shared points) plus free points: invariant = sorted degree pattern
        inter = sorted(popc(a & b) for a, b in itertools.combinations(ts, 2)); deg = defaultdict(int)
        for t in ts:
            for p in pts:
                if (t >> p) & 1: deg[p] += 1
        shared = tuple(sorted(tuple(sorted(i for i, t in enumerate(ts) if (t >> p) & 1)) for p in pts if deg[p] == 2))
        # graph on 4 vertices given by its edge list up to relabelling of the 4 triples
        best = None
        for perm in itertools.permutations(range(4)):
            e = tuple(sorted(tuple(sorted((perm[a], perm[b]))) for a, b in shared))
            if best is None or e < best: best = e
        return best
    masks = [sum(1 << p for p in t) for t in triples]
    first = masks[0]                                   # {1,2,3}
    for a in range(1, len(masks)):
        if popc(masks[a] & first) > 1: continue
        for b in range(a + 1, len(masks)):
            if popc(masks[b] & first) > 1 or popc(masks[b] & masks[a]) > 1: continue
            for c in range(b + 1, len(masks)):
                if popc(masks[c] & first) > 1 or popc(masks[c] & masks[a]) > 1 or popc(masks[c] & masks[b]) > 1: continue
                ts = (first, masks[a], masks[b], masks[c])
                if any(sum((t >> p) & 1 for t in ts) > 2 for p in pts): continue
                key = canon(ts)
                if key not in seen: seen[key] = ts; reps.append(ts)
    return reps

def enumerate_systems(m):
    blocks = [sum(1 << p for p in c) for c in itertools.combinations(range(m), 4)]
    blocks.sort(key=lambda b: [p for p in range(m) if (b >> p) & 1])
    by_min = defaultdict(list)
    for b in blocks: by_min[min(p for p in range(m) if (b >> p) & 1)].append(b)
    order = {b: i for i, b in enumerate(blocks)}
    leaves = []; nodes = [0]
    def pairs_ok(b, pair):
        ps = [p for p in range(m) if (b >> p) & 1]
        return all(pair[x][y] < 2 for x, y in itertools.combinations(ps, 2)), ps
    def rec(chosen, deg, pair, last):
        nodes[0] += 1
        x = next((p for p in range(m) if deg[p] < 4), None)
        if x is None:
            if len(chosen) == m: leaves.append(tuple(chosen))
            return
        if len(chosen) == m: return
        full = sum(1 << p for p in range(m) if deg[p] == 4)
        for b in by_min[x]:
            if b & full: continue
            if last is not None and min(p for p in range(m) if (last >> p) & 1) == x and order[b] <= order[last]: continue
            if any(popc(b & c) > 2 for c in chosen): continue
            ok, ps = pairs_ok(b, pair)
            if not ok: continue
            for p in ps: deg[p] += 1
            for u, v in itertools.combinations(ps, 2): pair[u][v] += 1; pair[v][u] += 1
            rec(chosen + [b], deg, pair, b)
            for p in ps: deg[p] -= 1
            for u, v in itertools.combinations(ps, 2): pair[u][v] -= 1; pair[v][u] -= 1
    L = links(m)
    for ts in L:
        chosen = sorted((t | 1 for t in ts), key=lambda b: order[b]); deg = [0] * m; pair = [[0] * m for _ in range(m)]
        for b in chosen:
            ps = [p for p in range(m) if (b >> p) & 1]
            for p in ps: deg[p] += 1
            for u, v in itertools.combinations(ps, 2): pair[u][v] += 1; pair[v][u] += 1
        rec(chosen, deg, pair, None)
    return leaves, len(L), nodes[0]

def pair_matrix(sysm, m):
    C = [[0] * m for _ in range(m)]
    for b in sysm:
        ps = [p for p in range(m) if (b >> p) & 1]
        for u, v in itertools.combinations(ps, 2): C[u][v] += 1; C[v][u] += 1
    return C

def invariant(sysm, m):
    C = pair_matrix(sysm, m)
    rows = tuple(sorted(tuple(sorted(r)) for r in C))
    # second-order: for every point, the multiset of (C value, number of common "2-neighbours") with the others
    two = [[sum(1 for z in range(m) if C[x][z] == 2 and C[y][z] == 2) for y in range(m)] for x in range(m)]
    one = [[sum(1 for z in range(m) if C[x][z] >= 1 and C[y][z] >= 1) for y in range(m)] for x in range(m)]
    prof = tuple(sorted(tuple(sorted((C[x][y], two[x][y], one[x][y]) for y in range(m) if y != x)) for x in range(m)))
    bi = tuple(sorted(tuple(sorted(popc(a & b) for b in sysm if b != a)) for a in sysm))
    return rows, prof, bi

def isomorphisms(s1, s2, m, count_all=False):
    """point bijections pi with pi(s1) = s2 (as sets of blocks); returns the first one, or the number if count_all"""
    C1 = pair_matrix(s1, m); C2 = pair_matrix(s2, m); set2 = set(s2); pi = [-1] * m; used = [False] * m; found = [0]; first = [None]
    r1 = [tuple(sorted(r)) for r in C1]; r2 = [tuple(sorted(r)) for r in C2]
    def rec(i):
        if i == m:
            img = set(sum(1 << pi[p] for p in range(m) if (b >> p) & 1) for b in s1)
            if img == set2:
                found[0] += 1
                if first[0] is None: first[0] = list(pi)
            return
        for y in range(m):
            if used[y] or r1[i] != r2[y]: continue
            if any(C1[i][j] != C2[y][pi[j]] for j in range(i)): continue
            pi[i] = y; used[y] = True
            rec(i + 1)
            used[y] = False; pi[i] = -1
            if found[0] and not count_all: return
    rec(0)
    return found[0] if count_all else first[0]

def dual(sysm, m):
    """the system with points and blocks exchanged"""
    return tuple(sorted(sum(1 << j for j, b in enumerate(sysm) if (b >> p) & 1) for p in range(m)))

def defect_type(sysm, m):
    C = pair_matrix(sysm, m); M = [[0 if i == j else 2 - C[i][j] for j in range(m)] for i in range(m)]
    doubles = sum(1 for i in range(m) for j in range(i + 1, m) if M[i][j] == 2)
    # connected components of the defect multigraph
    comp = []; seen = set()
    for s in range(m):
        if s in seen: continue
        st = [s]; cc = {s}
        while st:
            x = st.pop()
            for y in range(m):
                if M[x][y] and y not in cc: cc.add(y); st.append(y)
        seen |= cc; comp.append(len(cc))
    return M, doubles, sorted(comp, reverse=True)

def main():
    m = int(sys.argv[1]); t0 = time.time()
    leaves, nl, nodes = enumerate_systems(m)
    print("m = %d: links of the point 0: %d types; search nodes %d; labelled leaves %d  [%.0f s]" % (m, nl, nodes, len(leaves), time.time() - t0), flush=True)
    buckets = defaultdict(list); classes = []
    for s in leaves:
        key = invariant(s, m)
        for c in buckets[key]:
            if isomorphisms(s, classes[c]["sys"], m) is not None: classes[c]["leaves"] += 1; break
        else:
            buckets[key].append(len(classes)); classes.append({"sys": s, "leaves": 1})
    print("isomorphism classes (points and blocks permuted independently): %d; invariant buckets %d  [%.0f s]" % (len(classes), len(buckets), time.time() - t0), flush=True)
    import numpy as np
    out = []; selfdual = 0; dual_of = {}
    for i, c in enumerate(classes):
        s = c["sys"]; M, doubles, comp = defect_type(s, m); aut = isomorphisms(s, s, m, count_all=True)
        d = dual(s, m); kd = invariant(d, m); j = next((k for k in buckets.get(kd, []) if isomorphisms(d, classes[k]["sys"], m) is not None), None)
        dual_of[i] = j; selfdual += (j == i)
        ev = np.linalg.eigvalsh(np.array(M, dtype=float)); Md, dd, compd = defect_type(d, m)
        B = [[int((b >> p) & 1) for b in s] for p in range(m)]
        out.append({"index": i, "incidence_rows_points_columns_blocks": B, "automorphisms": aut, "dual_class": j, "defect_double_edges_P": doubles, "defect_double_edges_Q": dd,
                    "defect_components_P": comp, "defect_components_Q": compd, "defect_eigenvalues_P": [round(float(x), 6) for x in ev], "leaves": c["leaves"]})
    print("self-dual classes %d; classes up to duality %d" % (selfdual, (len(classes) + selfdual) // 2 if all(v is not None for v in dual_of.values()) else -1))
    print("largest defect eigenvalue below the degree, over the classes: max %.4f (must be <= 2)" % max(o["defect_eigenvalues_P"][-2] for o in out))
    hist = defaultdict(int)
    for o in out: hist[(o["defect_double_edges_P"], tuple(o["defect_components_P"]), o["automorphisms"])] += 1
    print("classes by (double defect edges on P, components of the defect multigraph on P, automorphisms):")
    for k in sorted(hist): print("   %s: %d" % (k, hist[k]))
    if len(sys.argv) > 2: json.dump({"m": m, "scope": "incidence of the two independent supports only; no extension to 99 vertices is claimed", "classes": out}, open(sys.argv[2], "w")); print("written", sys.argv[2])

if __name__ == "__main__":
    main()
