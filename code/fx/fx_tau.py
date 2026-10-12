"""Opposite-corner map tau(z_ab) = z_{a'b'} on Delta_x: is it an automorphism of F_x?  How does it act on cycles?"""
import collections
from fx_cycles import load, rook3
def analyse(n, adj, x):
    N = adj[x]; mate = {a: (N & adj[a]).pop() for a in N}
    D = [z for z in range(n) if z != x and z not in N]
    pair = {z: frozenset(N & adj[z]) for z in D}; zof = {p: z for z, p in pair.items()}
    tau = {z: zof[frozenset(mate[u] for u in pair[z])] for z in D}
    sp = {z: set() for z in D}
    for z in D:
        for a in pair[z]: sp[z].add(((adj[z] & adj[a]) - {x}).pop())
    is_aut = all({tau[w] for w in sp[z]} == sp[tau[z]] for z in D)
    # cycles
    seen, cyc_of, cycles = set(), {}, []
    for z0 in D:
        if z0 in seen: continue
        cyc = [z0]; seen.add(z0); prev, cur = None, z0
        while True:
            nxt = [w for w in sp[cur] if w != prev][0] if prev is not None else sorted(sp[cur])[0]
            if nxt == z0: break
            cyc.append(nxt); seen.add(nxt); prev, cur = cur, nxt
        for z in cyc: cyc_of[z] = len(cycles)
        cycles.append(cyc)
    act = collections.Counter()
    for i, cyc in enumerate(cycles):
        targets = {cyc_of[tau[z]] for z in cyc}
        if len(targets) > 1: act[('scattered', len(cyc))] += 1; continue
        j = targets.pop()
        if j != i: act[('swapped', len(cyc))] += 1
        else:
            pos = {z: p for p, z in enumerate(cyc)}; L = len(cyc)
            shift = (pos[tau[cyc[0]]] - 0) % L
            rot = all(tau[cyc[p]] in pos and (pos[tau[cyc[p]]] - p) % L == shift for p in range(L))
            act[('invariant', L, 'rotation by %d' % shift if rot else 'reflection')] += 1
    return is_aut, act
R = '/home/user/strongly-regular-graphs-research/results/srg243_family/'
for name, (n, adj) in [('Paley9', rook3())] + [(f, load(R + f)) for f in ['bvls243.edges', 'twin243.edges', 'gamma3_aut864.edges', 'gamma4_aut3888.edges']]:
    tot = collections.Counter(); auts = collections.Counter()
    for x in range(n):
        a, act = analyse(n, adj, x); auts[a] += 1; tot += act
    print(name, 'tau automorphism of F_x:', dict(auts), '| action on cycles:', dict(tot))
