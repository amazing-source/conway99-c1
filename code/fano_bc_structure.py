"""notes/104 §7: consequences of the Fano skeleton.
Skeleton (ell_skeleton.py): there is a Fano plane Phi on the 7 classes; l = 4 on its 7 pencils, 2 on the 56
'no line' triangles, 0 on the 42 'one line' triangles.  At each pair P the l = 2 triangles all have the
S_3-holonomy fixing one partition X_P, and X is parallel along every non-pencil edge.
B = {P : X_P = A_P}, C = the rest.  Proved by hand (notes/104): C is independent in the non-pencil graph,
non-pencil edges inside B are isometric, non-pencil edges B-C are not, pencil edges B-C are not.
Here: enumerate all C (independent sets of the non-pencil graph) and all statuses of the remaining pencil
edges, and test (T1) triangle rule, (T2) G_P empty or connected with an even number of edges, (a) at most
2 fully non-isometric pairs per class."""
import itertools, os
NO_A = os.environ.get('APPLY_A') != '1'   # default: (T1), (T2) only (35 survivors); APPLY_A=1 adds (a) (21)

lines = [tuple(sorted(((0 + d) % 7, (1 + d) % 7, (3 + d) % 7))) for d in range(7)]
pairs = list(itertools.combinations(range(7), 2))
def disjoint(a, b): return not set(a) & set(b)
def vpt(P):
    L = next(L for L in lines if set(P) <= set(L))
    return next(c for c in L if c not in P)
pencil_edge = lambda P, Q: disjoint(P, Q) and vpt(P) == vpt(Q)
kedges = [(P, Q) for P, Q in itertools.combinations(pairs, 2) if disjoint(P, Q)]
np_adj = {P: [Q for Q in pairs if disjoint(P, Q) and not pencil_edge(P, Q)] for P in pairs}
tris = [t for t in itertools.combinations(pairs, 3) if all(disjoint(a, b) for a, b in itertools.combinations(t, 2))]

def connected_even(G):
    if not G:
        return True
    if len(G) % 2:
        return False
    verts = set(v for e in G for v in e)
    seen = {next(iter(verts))}
    ch = True
    while ch:
        ch = False
        for u, v in G:
            if (u in seen) != (v in seen):
                seen |= {u, v}
                ch = True
    return seen == verts

# independent sets of the non-pencil graph
indep = [[]]
def grow(cur, start):
    for n in range(start, 21):
        P = pairs[n]
        if all(Q not in np_adj[P] for Q in cur):
            indep.append(cur + [P])
            grow(cur + [P], n + 1)
grow([], 0)
print('independent sets of the non-pencil graph (incl. empty):', len(indep), ' max size', max(map(len, indep)))

def pages(P, Q):
    return [R for R in pairs if disjoint(R, P) and disjoint(R, Q)]

survivors = []
for C in indep:
    if not C:
        continue
    Cs = set(C)
    status = {}      # frozenset edge -> 0 iso / 1 non-iso
    free = []
    for P, Q in kedges:
        e = frozenset((P, Q))
        inC = (P in Cs) + (Q in Cs)
        if not pencil_edge(P, Q):
            status[e] = 0 if inC == 0 else 1
        elif inC == 1:
            status[e] = 1                          # pencil edge B-C: proved non-isometric
        elif inC == 2:
            free.append(e)
        else:                                      # pencil edge B-B: isometric unless both T0 pages lie in C
            pg = [R for R in pages(P, Q) if not pencil_edge(R, P)]
            if all(R in Cs for R in pg):
                free.append(e)
            else:
                status[e] = 0
    for bits in itertools.product((0, 1), repeat=len(free)):
        st = dict(status)
        st.update(zip(free, bits))
        ok = True
        for t in tris:
            n_iso = sum(1 for a, b in itertools.combinations(t, 2) if st[frozenset((a, b))] == 0)
            if n_iso == 2:
                ok = False
                break
        if not ok:
            continue
        full = {i: 0 for i in range(7)}
        for P in pairs:
            G = [Q for Q in pairs if disjoint(P, Q) and st[frozenset((P, Q))] == 1]
            if not connected_even(G):
                ok = False
                break
            if len(G) == 10:
                for i in P:
                    full[i] += 1
        if ok and (NO_A or max(full.values()) <= 2):
            survivors.append((C, dict(st)))
print('(C, pencil statuses) passing (T1), (T2), (a):', len(survivors))
for C, st in survivors[:40]:
    nu = sum(st.values())
    print('  |C| =', len(C), C, ' non-isometric edges:', nu)

if __name__ == '__main__':
    import pickle
    pickle.dump(survivors, open('../data/fano_bc_survivors.pkl', 'wb'))
    C, st = survivors[0]
    print('\nfirst survivor, C =', C)
    for P in pairs:
        G = sorted(Q for Q in pairs if disjoint(P, Q) and st[frozenset((P, Q))] == 1)
        pen = [Q for Q in pairs if pencil_edge(P, Q)]
        print('  %s %s v=%d pencil %s | non-iso to: %s' % (P, 'C' if P in C else 'B', vpt(P), pen, G))
    tri_types = {}
    for t in tris:
        n = sum(1 for a, b in itertools.combinations(t, 2) if st[frozenset((a, b))] == 1)
        tri_types[n] = tri_types.get(n, 0) + 1
    print('  triangles by number of non-isometric edges:', tri_types)
