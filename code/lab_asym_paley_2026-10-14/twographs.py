"""Regular two-graphs behind a conference family (asymmetry campaign, 14/10/2026).

For a conference graph G on v = 4t+1 vertices (k = 2 mu), G + an isolated point is a graph on v+1 points whose switching
class is a regular two-graph T. The descendant T_y of T at a point y is obtained by Seidel switching with respect to
the neighbourhood of y (making y isolated) and deleting y; it is again srg(v, 2t, t-1, t). Facts used and checked here:
T_x ~ T_y (isomorphic graphs) iff x, y lie in one Aut(T)-orbit, and Aut(T_x) = stabiliser of x in Aut(T); hence
|Aut(T)| = |orbit(x)| * |Aut(T_x)| for every x.
usage: python twographs.py <spence file of srg(v,2t,t-1,t)>
Exact; prints, for each two-graph found, its orbit structure on the v+1 points and the descendants by orbit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L


def descendants(nb):
    v = len(nb)
    n = v + 1
    H = [set(x) for x in nb] + [set()]            # point v isolated
    out = []
    for y in range(n):
        S = H[y]
        # Seidel switching with respect to S: flip pairs with exactly one end in S
        K = [set() for _ in range(n)]
        for a in range(n):
            for b in range(a + 1, n):
                e = b in H[a]
                if (a in S) != (b in S):
                    e = not e
                if e:
                    K[a].add(b)
                    K[b].add(a)
        assert not K[y], "y not isolated after switching"
        keep = [u for u in range(n) if u != y]
        idx = {u: i for i, u in enumerate(keep)}
        out.append([set(idx[w] for w in K[u] if w != y) for u in keep])
    return out


if __name__ == "__main__":
    header, gs = L.read_spence(sys.argv[1])
    canon = [L.canonical_form(g) for g in gs]
    index = {c: i + 1 for i, c in enumerate(canon)}
    orders = [L.group_order(g)[0] for g in gs]
    seen = {}
    for gi, g in enumerate(gs):
        types = []
        for d in descendants(g):
            p = L.srg_params(d)
            c = L.canonical_form(d)
            types.append(index.get(c, "new%s" % (p,)))
        key = tuple(sorted(types, key=str))
        if key not in seen:
            seen[key] = gi + 1
            counts = {}
            for t in types:
                counts[t] = counts.get(t, 0) + 1
            check = {t: (m, orders[t - 1], m * orders[t - 1]) for t, m in counts.items() if isinstance(t, int)}
            print("two-graph from graph #%d: descendants (graph #: (orbit size, |Aut|, product)) %s"
                  % (gi + 1, dict(sorted(check.items()))), flush=True)
    print("number of distinct regular two-graphs:", len(seen))
