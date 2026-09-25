# notes/111: L14, |C| = 2 -- independent re-check of the hand refutation (no search beyond 3! = 6 assignments).
# Classes 0..6, labels (c, s), s in {+1,-1}.  Twisting labels a = (0,+), b = (1,+), both twisting C = {2,3}.
# Rule-based adjacency oracle for pairs of Gamma_2(x)-vertices that SHARE a label or a class (determined by tau, rho);
# generic adjacencies (disjoint class pairs) only where forced/assumed (B_{02,13} option); the rest is 'unknown'.
import itertools
P_, M_ = 1, -1
def mate(l): return (l[0], -l[1])
def V(*ls): return frozenset(ls)

def build(case):
    tau = {}
    labels = [(c, s) for c in range(7) for s in (P_, M_)]
    for l in labels:
        tau[l] = {m: mate(m) for m in labels if m[0] != l[0]}          # untwisted by default
    tau[(0, P_)].update({(2, P_): (3, P_), (3, P_): (2, P_), (2, M_): (3, M_), (3, M_): (2, M_)})
    if case == 'P':
        tau[(1, P_)].update({(2, P_): (3, P_), (3, P_): (2, P_), (2, M_): (3, M_), (3, M_): (2, M_)})
    else:
        tau[(1, P_)].update({(2, P_): (3, M_), (3, M_): (2, P_), (2, M_): (3, P_), (3, P_): (2, M_)})
    Z = {2: {(0, P_), (1, P_)}, 3: {(0, P_), (1, P_)}}                  # labels twisting class c
    def rho(c, l):                                                      # shadow partner label (L13)
        if c in Z and l in Z[c]:
            return next(m for m in Z[c] if m != l)
        return l
    def adj_rule(y, w):
        """True/False if decided by labels/classes (shared label -> tau line; shared class, mate labels -> shadow)."""
        sl = y & w
        if len(sl) == 1:
            (l,) = sl
            (u,) = y - sl; (v,) = w - sl
            return tau[l][u] == v
        for u in y:
            for v in w:
                if u[0] == v[0] and u != v:                           # mate labels u, v = mate(u)
                    (yo,) = y - {u}; (wo,) = w - {v}
                    return wo == rho(u[0], yo)
        return None
    return tau, adj_rule

A, B, C, D = V((0,P_),(2,P_)), V((0,P_),(2,M_)), V((0,M_),(2,P_)), V((0,M_),(2,M_))
E, F, G, H = V((1,P_),(3,P_)), V((1,P_),(3,M_)), V((1,M_),(3,P_)), V((1,M_),(3,M_))
Q02, Q13 = [A, B, C, D], [E, F, G, H]
name = {A:'A',B:'B',C:'C',D:'D',E:'E',F:'F',G:'G',H:'H'}
labels = [(c, s) for c in range(7) for s in (P_, M_)]
allV = [frozenset(p) for p in itertools.combinations(labels, 2) if list(p)[0][0] != list(p)[1][0]]

def nonadj_pairs(Q, adj):
    return [frozenset(p) for p in itertools.combinations(Q, 2) if not adj(*p)]

for case in ('P', 'R'):
    tau, adj_rule = build(case)
    for opt in (1, 2):
        B0213 = {(C, G), (D, H)} if opt == 1 else {(C, H), (D, G)}
        def adj(y, w):
            r = adj_rule(y, w)
            if r is not None:
                return r
            if {y, w} <= set(Q02) | set(Q13) and ((y in Q02) != (w in Q02)):
                return (y, w) in B0213 or (w, y) in B0213
            return None
        # special common neighbours of (y, w): vertices in Q_{P} with P meeting {0,1,2,3} in >= ... i.e. any vertex
        # of Gamma_2 whose adjacency to both y and w is decided by the rules (shares a class with each)
        M = {}
        for y in Q02:
            for w in Q13:
                if adj(y, w):
                    base = 1                      # lambda: exactly one common neighbour
                else:
                    base = 2
                common = 0
                for z in allV:
                    if z in (y, w):
                        continue
                    a1, a2 = adj(y, z), adj(w, z)
                    if a1 and a2:
                        common += 1
                # common neighbours among labels: y's labels vs w's labels (disjoint class pairs -> none)
                M[(y, w)] = base - common        # what must come from Q_45, Q_46, Q_56 (generic, undecided)
        # doubles: non-adjacent pairs inside Q02 and Q13; each has exactly ONE decided common neighbour
        for Q in (Q02, Q13):
            for p, q in itertools.combinations(Q, 2):
                if adj(p, q):
                    continue
                dec = sum(1 for z in allV if z not in (p, q) and adj(p, z) and adj(q, z))
                lab = len(p & q)                  # a shared label is a common neighbour too
                assert dec + lab == 1, (case, opt, name[p], name[q], dec, lab)
        na02, na13 = nonadj_pairs(Q02, lambda p, q: adj(p, q)), nonadj_pairs(Q13, lambda p, q: adj(p, q))
        feasible = 0
        for perm in itertools.permutations(na13):
            Dm = {k: 0 for k in M}
            for pr02, pr13 in zip(na02, perm):
                for y in pr02:
                    for w in pr13:
                        Dm[(y, w)] += 1
            S = {k: M[k] - Dm[k] for k in M}
            if min(S.values()) < 0:
                continue
            # singles: 6 vertices, each contributes one (y,w); row/col sums of S must be (3 - #doubles through y)
            ok = all(sum(S[(y, w)] for w in Q13) == 3 - sum(1 for p in na02 if y in p) for y in Q02) and \
                 all(sum(S[(y, w)] for y in Q02) == 3 - sum(1 for p in na13 if w in p) for w in Q13)
            feasible += ok
        print(f'case {case}, B_02,13 option {opt}: nonadj Q02 {sorted("".join(sorted(name[v] for v in p)) for p in na02)}, '
              f'Q13 {sorted("".join(sorted(name[v] for v in p)) for p in na13)}')
        block = sum(M[(y, w)] for y in (A, B) for w in (E, F))
        print('   M (rows A..D, cols E..H):', [[M[(y, w)] for w in Q13] for y in Q02],
              ' feasible double assignments:', feasible, '| available in block {A,B}x{E,F}:', block, '(demand >= 5)')
        assert feasible == 0 and block == 4
