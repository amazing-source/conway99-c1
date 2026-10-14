"""Anatomy of asymmetry in srg(25,12,5,6) (asymmetry campaign, 14/10/2026, part 2).

(1) Two-graph groups as explicit permutation groups on 26 points: Aut(T)_p = Aut(T_p) (all automorphisms of the
    descendant, found by search) and one isomorphism T_p -> T_q for each q in the orbit of p, extended by p -> q.
    Prints the group order, element orders, whether it is abelian, the orbits with their descendants.
(2) Godsil-McKay switchings of size 4: for each switching set D of G, the setwise stabiliser of D in Aut(G) and
    |Aut| of the switched graph G'. Law tested: Stab_Aut(G)(D) <= Aut(G') (an automorphism of G fixing D commutes
    with the switching), so |Stab(D)| divides |Aut(G')|; "extra" automorphisms of G' are those not coming from G.
(3) Asymmetry certificates: colour every vertex by the isomorphism type of its local graph G[N(v)], refine; if the
    refined colouring is discrete, every automorphism fixes every vertex (a proof of Aut = 1 readable by hand:
    invariant + refinement).
usage: python anatomy25.py <spence 25-12-5-6 file>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srglib as L
import twographs as TW
import gm_switch as GM


def all_isos(nb1, nb2):
    n = len(nb1)
    c1 = L.refine(nb1, [0] * n)
    c2 = L.refine(nb2, [0] * n)
    if sorted(c1) != sorted(c2):
        return
    yield from L._search_iso(nb1, c1, nb2, c2, n)


def compose(p, q):            # (p o q)(v) = p[q[v]]
    return tuple(p[q[v]] for v in range(len(p)))


def perm_order(p):
    n, e, k = len(p), tuple(range(len(p))), 1
    q = p
    while q != e:
        q = compose(p, q)
        k += 1
    return k


def two_graph_group(desc):
    """desc[y] = descendant at y (graph on the 25 points other than y, re-indexed in increasing order)."""
    n = len(desc)
    canon = [L.canonical_form(d) for d in desc]

    def lift(y, z, phi):          # phi: desc[y] -> desc[z] as index maps; returns a permutation of 0..n-1
        ky = [u for u in range(n) if u != y]
        kz = [u for u in range(n) if u != z]
        s = [None] * n
        s[y] = z
        for i, u in enumerate(ky):
            s[u] = kz[phi[i]]
        return tuple(s)
    group = set()
    done = set()
    for y in range(n):
        if y in done:
            continue
        orbit = [z for z in range(n) if canon[z] == canon[y]]
        done.update(orbit)
        stab = [lift(y, y, phi) for phi in all_isos(desc[y], desc[y])]
        for z in orbit:
            phi = next(all_isos(desc[y], desc[z]))
            t = lift(y, z, phi)
            for s in stab:
                group.add(compose(t, s))
    return sorted(group), canon


if __name__ == "__main__":
    header, gs = L.read_spence(sys.argv[1])
    canon25 = [L.canonical_form(g) for g in gs]
    index = {c: i + 1 for i, c in enumerate(canon25)}
    auts = [[tuple(p) for p in L.automorphism_group(g)] for g in gs]
    print("(0) |Aut| of the 15 graphs:", [len(a) for a in auts], flush=True)

    # (1) two-graphs
    print("\n(1) regular two-graphs on 26 points as permutation groups", flush=True)
    seen = set()
    for gi, g in enumerate(gs):
        desc = TW.descendants(g)
        names = [index[L.canonical_form(d)] for d in desc]
        key = tuple(sorted(names))
        if key in seen:
            continue
        seen.add(key)
        G, canon = two_graph_group(desc)
        n = 26
        # check: every element preserves the coherent triples (two-graph = triples with an odd number of edges in
        # the graph g + isolated point 25)
        H = [set(x) for x in g] + [set()]
        def odd(a, b, c):
            return ((b in H[a]) + (c in H[a]) + (c in H[b])) % 2
        import itertools
        triples = [t for t in itertools.combinations(range(n), 3) if odd(*t)]
        tset = set(triples)
        ok = all(tuple(sorted((s[a], s[b], s[c]))) in tset for s in G for (a, b, c) in triples[:400])
        orders = {}
        for s in G:
            o = perm_order(s)
            orders[o] = orders.get(o, 0) + 1
        abelian = all(compose(a, b) == compose(b, a) for a in G[:60] for b in G[:60]) if len(G) <= 72 else "not tested"
        orbs = L.orbits(H, list(G))
        print("two-graph containing graph #%d: |Aut(T)| = %d, preserves triples (sample): %s, element orders %s, "
              "abelian %s" % (gi + 1, len(G), ok, dict(sorted(orders.items())), abelian), flush=True)
        print("   coherent triples: %d; orbits (size: descendant #, |Aut(desc)|):" % len(triples), flush=True)
        for O in orbs:
            print("     size %2d: points %s -> descendant #%d (|Aut| %d)"
                  % (len(O), O, names[O[0]], len(auts[names[O[0]] - 1])), flush=True)
        if len(G) == 6:
            # describe the generators: an element of order 6 or the S3 structure
            for s in G:
                cyc, seenv = [], set()
                for v in range(n):
                    if v in seenv:
                        continue
                    c, w = [], v
                    while w not in seenv:
                        seenv.add(w)
                        c.append(w)
                        w = s[w]
                    if len(c) > 1:
                        cyc.append(tuple(c))
                print("     element of order %d: %s" % (perm_order(s), cyc), flush=True)

    # (2) GM switching stabilisers
    print("\n(2) Godsil-McKay switchings of size 4: (target, |Stab_Aut(G)(D)|, |Aut(target)|) -> count", flush=True)
    for gi, g in enumerate(gs):
        sets = GM.gm_sets(g, 4)
        tally = {}
        bad = 0
        for D in sets:
            Ds = set(D)
            st = [s for s in auts[gi] if {s[d] for d in D} == Ds]
            h = GM.switch(g, D)
            t = index[L.canonical_form(h)]
            # law check: every element of st is an automorphism of h
            for s in st:
                if not all({s[w] for w in h[v]} == h[s[v]] for v in range(25)):
                    bad += 1
            key = (t, len(st), len(auts[t - 1]))
            tally[key] = tally.get(key, 0) + 1
        print("  #%2d (|Aut| %3d): %3d sets; law violations %d; %s" % (gi + 1, len(auts[gi]), len(sets), bad,
              dict(sorted(tally.items()))), flush=True)

    # (3) certificates
    print("\n(3) local-graph invariant + refinement", flush=True)
    for gi, g in enumerate(gs):
        types = []
        for v in range(25):
            N = sorted(g[v])
            pos = {u: i for i, u in enumerate(N)}
            loc = [set(pos[w] for w in g[u] if w in pos) for u in N]
            types.append(L.canonical_form(loc))
        keys = sorted(set(types))
        col = [keys.index(t) for t in types]
        sizes = sorted([col.count(c) for c in set(col)], reverse=True)
        r = L.refine(g, col)
        orbs = L.vertex_orbits(g)
        print("  #%2d |Aut| %3d: %2d local types, class sizes %s; refined cells %d (orbits %d)%s"
              % (gi + 1, len(auts[gi]), len(keys), sizes, len(set(r)), len(orbs),
                 "  -> DISCRETE: Aut = 1 certified" if len(set(r)) == 25 else ""), flush=True)
