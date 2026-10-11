"""Independent certification (pure Python, integers only, no numpy, no nauty).
  python3 certify.py GRAPH.edges
1. checks srg(243,22,1,2) on all pairs;
2. computes isomorphism-invariant vertex colours from the line geometry (grids, twisted pairs, prisms),
   refines them by colour refinement (1-WL); if the stable partition is discrete, Aut(G) = 1 is proved:
   every automorphism preserves the stable colouring, hence fixes every vertex.
3. prints the invariants used, so that two graphs can be distinguished by them."""
import sys, itertools, collections, hashlib


def load(path):
    n = 0; E = []
    for line in open(path):
        if line.strip():
            a, b = map(int, line.split()); E.append((a, b)); n = max(n, a + 1, b + 1)
    nb = [set() for _ in range(n)]
    for a, b in E:
        nb[a].add(b); nb[b].add(a)
    return n, nb


def check_srg(n, nb, k=22, lam=1, mu=2):
    bad = 0
    for x in range(n):
        if len(nb[x]) != k or x in nb[x]: bad += 1
        for y in range(x + 1, n):
            c = len(nb[x] & nb[y])
            if (y in nb[x] and c != lam) or (y not in nb[x] and c != mu):
                bad += 1
    return bad


def lines(n, nb):
    L = set()
    for x in range(n):
        for y in nb[x]:
            for z in nb[x] & nb[y]:
                L.add(tuple(sorted((x, y, z))))
    return sorted(L)


def line_invariants(n, nb, L):
    """per vertex: (#grids through it, #twisted line pairs (2 edges) through it, #prisms through it)."""
    idx = {l: i for i, l in enumerate(L)}
    at = [[] for _ in range(n)]
    for i, l in enumerate(L):
        for p in l: at[p].append(i)
    # edges between lines
    line_of_edge = {}
    for i, l in enumerate(L):
        for a, b in itertools.combinations(l, 2):
            line_of_edge[(a, b)] = line_of_edge[(b, a)] = i
    joins = collections.Counter()
    for i, l in enumerate(L):
        for p in l:
            for q in nb[p]:
                j = line_of_edge[(p, q)]
                # edge p-q lies on line j; we want edges between line i and other lines m containing q (q not in l)
                if q in l: continue
                for m in at[q]:
                    if m != i and not (set(L[m]) & set(l)):
                        joins[(min(i, m), max(i, m))] += 1
    # each edge between disjoint lines i,m counted twice (from p side: once per endpoint orientation? only from i)
    tw = [0] * n; pr = [0] * n
    for (i, m), c in joins.items():
        e = c // 2  # counted once from i-side and once from m-side
        if e == 2:
            for p in set(L[i]) | set(L[m]): tw[p] += 1
        if e == 3:
            for p in set(L[i]) | set(L[m]): pr[p] += 1
    # grids: two lines through p span a grid iff the 4 'far' corners close up
    gr = [0] * n
    seen = set()
    for p in range(n):
        for i, j in itertools.combinations(at[p], 2):
            a = [x for x in L[i] if x != p]; b = [x for x in L[j] if x != p]
            Q = {}
            ok = True
            for x in a:
                for y in b:
                    c = (nb[x] & nb[y]) - {p}
                    if len(c) != 1: ok = False; break
                    Q[(x, y)] = next(iter(c))
                if not ok: break
            if not ok: continue
            q00, q01, q10, q11 = Q[(a[0], b[0])], Q[(a[0], b[1])], Q[(a[1], b[0])], Q[(a[1], b[1])]
            if not (q01 in nb[q00] and q11 in nb[q10] and q10 in nb[q00] and q11 in nb[q01]): continue
            pts = frozenset(set(L[i]) | set(L[j]) | {q00, q01, q10, q11})
            if len(pts) != 9: continue
            if sum(len(nb[x] & pts) for x in pts) != 36: continue
            if pts not in seen:
                seen.add(pts)
                for x in pts: gr[x] += 1
    return gr, tw, pr, len(seen), sum(1 for c in joins.values() if c // 2 == 2), sum(1 for c in joins.values() if c // 2 == 3)


def refine(n, nb, col):
    col = list(col)
    while True:
        sig = [(col[x], tuple(sorted(collections.Counter(col[y] for y in nb[x]).items()))) for x in range(n)]
        keys = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [keys[s] for s in sig]
        if len(set(new)) == len(set(col)):
            return new
        col = new


def refine_with_lines(n, nb, L, col):
    """colour refinement on the incidence structure vertices + lines + adjacency (still isomorphism-invariant)."""
    at = [[] for _ in range(n)]
    for i, l in enumerate(L):
        for p in l: at[p].append(i)
    col = list(col)
    while True:
        lc = [tuple(sorted(col[p] for p in l)) for l in L]
        sig = [(col[x], tuple(sorted(collections.Counter(col[y] for y in nb[x]).items())),
                tuple(sorted(lc[i] for i in at[x]))) for x in range(n)]
        keys = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [keys[s] for s in sig]
        if len(set(new)) == len(set(col)):
            return new
        col = new


if __name__ == "__main__":
    n, nb = load(sys.argv[1])
    bad = check_srg(n, nb)
    print("vertices", n, "srg(243,22,1,2) violations:", bad)
    L = lines(n, nb)
    gr, tw, pr, ngr, ntw, npr = line_invariants(n, nb, L)
    print("lines", len(L), "grids", ngr, "twisted pairs (2 edges)", ntw, "prisms (3 edges)", npr)
    print("grid distribution", sorted(collections.Counter(gr).items()))
    col0 = [hash((gr[x], tw[x], pr[x])) for x in range(n)]
    col = refine_with_lines(n, nb, L, col0)
    cells = collections.Counter(col)
    print("stable partition: cells", len(cells), "cell sizes", sorted(collections.Counter(cells.values()).items()))
    print("CERTIFICATE Aut=1 (discrete stable partition):", len(cells) == n)
    h = hashlib.sha256(str(sorted(collections.Counter((gr[x], tw[x], pr[x]) for x in range(n)).items())).encode()).hexdigest()[:16]
    print("invariant fingerprint", h)
