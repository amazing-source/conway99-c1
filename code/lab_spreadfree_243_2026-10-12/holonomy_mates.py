"""Lab session, 2026-10-12. Test of a tempting law: are the fixed points of the holonomy of a line closed under the
mate involution at the base point? (No: it fails in Gamma3, Gamma4 and the new graph.)
python -I holonomy_mates.py <directory of line_holonomy.py> <edge files ...>"""
import sys, collections
sys.path.insert(0, sys.argv[1])
import line_holonomy as LH, trade_census as TC
for path in sys.argv[2:]:
    n, adj = TC.load(path)
    lines = sorted({tuple(sorted((x, y, next(iter(adj[x] & adj[y]))))) for x in range(n) for y in adj[x] if x < y})
    closed = 0; total = 0; commute = 0; invert = 0; mixed = collections.Counter()
    for L in lines:
        for (p, u, us) in [(L[0], L[1], L[2]), (L[1], L[2], L[0]), (L[2], L[0], L[1])]:
            tau = LH.holonomy(adj, p, u, us); mate = {w: next(iter(adj[p] & adj[w])) for w in tau}
            fix = {w for w in tau if tau[w] == w}; total += 1
            if all(mate[w] in fix for w in fix): closed += 1
            if all(tau[mate[w]] == mate[tau[w]] for w in tau): commute += 1
            if all(mate[tau[mate[tau[w]]]] == w for w in tau): invert += 1
            # the two-cycles: are they mate pairs ?
            two = [(w, tau[w]) for w in tau if tau[w] != w and tau[tau[w]] == w and w < tau[w]]
            mixed[(len(two), sum(1 for a, b in two if mate[a] == b))] += 1
    print("%s: (line, base point) pairs %d; fixed points closed under mates: %d; tau commutes with the mate involution: %d; mate*tau*mate = tau^-1: %d" % (path.split("/")[-1], total, closed, commute, invert))
    print("     (number of 2-cycles of tau, how many of them are mate pairs): %s" % sorted(mixed.items()))
