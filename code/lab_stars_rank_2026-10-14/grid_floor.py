"""Grid floor from a cap on mixed relations (14/10/2026, LAB).
If every admissible four-star structure with T, U >= 0 has at most M mixed relations, then by G9 (exact in a Conway graph:
mixed = 12 - c(l) - c(m) + [l, m span a grid] + delta, delta >= 0) every pair of lines at every vertex has
c(l) + c(m) >= 12 - M + [grid].  G_v = graph on the 7 lines at v (l ~ m iff they span a 3x3 grid), deg(l) = g(l) = number of
mu = 1 components of H_l (P8, P9); the other 6 - g lines form components of size >= 2, so c(l) <= g + floor((6 - g)/2)
and g != 5.  Exhaustive over the 2^21 graphs G_v: minimum number of grids through a vertex, hence rho >= 99 min / 9."""
import itertools
pairs = list(itertools.combinations(range(7), 2))
cmax = {0: 3, 1: 3, 2: 4, 3: 4, 4: 5, 6: 6}
for M in (2, 3, 4, 5, 6):
    best = None
    for mask in range(1 << 21):
        deg = [0] * 7
        E = set()
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                deg[i] += 1
                deg[j] += 1
                E.add((i, j))
        if 5 in deg:
            continue
        c = [cmax[d] for d in deg]
        if all(c[i] + c[j] >= 12 - M + ((i, j) in E) for (i, j) in pairs):
            if best is None or len(E) < best[0]:
                best = (len(E), deg, c)
    print("M = %d: min grids through a vertex = %s (degrees %s, c %s), rho >= %s"
          % (M, best[0], best[1], best[2], 11 * best[0]))


# Same with the known local grid lemmas added: L8 (no K7: no Hamming point), L10 (at most 18 grids through a vertex),
# kk6 (no K6 in G_v) and kk5 (a K5 forces the edge between the two remaining lines); kk5/kk6 are SAT/DRAT results.
print("with L8, L10, kk5, kk6:")
for M in (2, 3, 4):
    best = None
    for mask in range(1 << 21):
        deg = [0] * 7
        E = set()
        for b, (i, j) in enumerate(pairs):
            if mask >> b & 1:
                deg[i] += 1
                deg[j] += 1
                E.add((i, j))
        if 5 in deg or len(E) > 18:
            continue
        adj = lambda i, j: (min(i, j), max(i, j)) in E
        bad = False
        for six in itertools.combinations(range(7), 6):
            if all(adj(i, j) for i, j in itertools.combinations(six, 2)):
                bad = True
                break
        if not bad:
            for five in itertools.combinations(range(7), 5):
                if all(adj(i, j) for i, j in itertools.combinations(five, 2)):
                    rest = [x for x in range(7) if x not in five]
                    if not adj(rest[0], rest[1]):
                        bad = True
                        break
        if bad:
            continue
        c = [cmax[d] for d in deg]
        if all(c[i] + c[j] >= 12 - M + ((i, j) in E) for (i, j) in pairs):
            if best is None or len(E) < best[0]:
                best = (len(E), deg, c)
    print("M = %d: %s" % (M, "INFEASIBLE (no admissible grid graph at a vertex)" if best is None else
                          "min grids through a vertex = %d (degrees %s, c %s), rho >= %d" % (best[0], best[1], best[2], 11 * best[0])))
