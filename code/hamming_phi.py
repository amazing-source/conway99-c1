"""Hamming point of srg(99,14,1,2), compact 'phi' model (equivalent to hamming_point.py, derived in notes/20).
Q_P (P = class pair {i<j}) = 4 X-vertices, indexed by signs (a,b) in F_2^2 (a: sign at i, b: sign at j).
For disjoint pairs P, P': a bijection phi_{P,P'} : Q_P -> Q_P' (the disjoint edges), phi_{P',P} = inverse.
Facts (all equivalent to the SRG equations given tau = mate at x and grid tightness):
 B  (lambda) u in Q_P, P' disjoint: exactly one P'' in pairs(rest(P,P')) with phi_{P'P''}(phi_{PP'}(u)) = phi_{PP''}(u)
 C  (mu, P = ij, P' = ik): u in Q_P, w in Q_P': #{P'' in pairs([7]-{i,j,k}) : phi_{PP''}(u) = phi_{P'P''}(w)}
       = 1 if u, w have the same sign at i, = 2 otherwise
 D  (mu, P, P' disjoint, w != phi(u)): [phi^{-1}(w) ~ u] + [phi(u) ~ w] + #coincidences over pairs(rest) = 2
       (~ = adjacent in the 4-cycle = differ in exactly one sign)
 E  (label counts) u in Q_P, free class m: among the 4 pairs P' = {m,l}, phi_{PP'}(u) has sign + at m exactly twice
Options: --iso forces all phi to be isometries (antipode-commuting), i.e. sigma_x is an automorphism (C2 case);
         --noniso requires at least one non-isometric phi (the C1-relevant case).
Symmetry breaking: phi_{01,23} fixes (0,0) (sign flips of classes 2, 3).
"""
import argparse, itertools, time, json
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

C7 = range(7)
PAIRS = list(itertools.combinations(C7, 2))
SIGNS = [(a, b) for a in (0, 1) for b in (0, 1)]


def sign_at(P, s, c):
    return s[0] if P[0] == c else s[1]


def adj4(s, t):
    return (s[0] != t[0]) + (s[1] != t[1]) == 1


def build(iso=False, noniso=False, use=('B','C','D','E'), breaksym=False):
    pool = IDPool()
    cnf = CNF()

    def y(P, Q, s, t):
        # canonical orientation: P < Q lexicographically
        if P < Q:
            return pool.id(('y', P, Q, s, t))
        return pool.id(('y', Q, P, t, s))
    disjoint = [(P, Q) for P, Q in itertools.combinations(PAIRS, 2) if not set(P) & set(Q)]
    for P, Q in disjoint:
        for s in SIGNS:
            cnf.extend(CardEnc.equals([y(P, Q, s, t) for t in SIGNS], 1, vpool=pool, encoding=EncType.pairwise).clauses)
        for t in SIGNS:
            cnf.extend(CardEnc.equals([y(P, Q, s, t) for s in SIGNS], 1, vpool=pool, encoding=EncType.pairwise).clauses)
    # isometry indicators
    nonisos = []
    for P, Q in disjoint:
        # phi is an isometry iff it maps antipodal pairs to antipodal pairs: phi(s + 11) = phi(s) + 11
        for s in SIGNS:
            sb = (1 - s[0], 1 - s[1])
            for t in SIGNS:
                tb = (1 - t[0], 1 - t[1])
                # y(s,t) & not y(sb,tb) -> non-isometric
                nv = pool.id(('noniso', P, Q, s, t))
                cnf.extend([[-nv, y(P, Q, s, t)], [-nv, -y(P, Q, sb, tb)], [nv, -y(P, Q, s, t), y(P, Q, sb, tb)]])
                nonisos.append(nv)
                if iso:
                    cnf.append([-y(P, Q, s, t), y(P, Q, sb, tb)])
    if noniso:
        cnf.append(nonisos)

    def coinc(P, s, Q, t, R):
        """indicator: phi_{PR}(s) == phi_{QR}(t)  (P, Q each disjoint from R)"""
        key = ('co',) + tuple(sorted([(P, s), (Q, t)])) + (R,)
        if key in COINC:
            return COINC[key]
        c = pool.id(key)
        ands = []
        for z in SIGNS:
            a = pool.id(key + ('z', z))
            cnf.extend([[-a, y(P, R, s, z)], [-a, y(Q, R, t, z)], [a, -y(P, R, s, z), -y(Q, R, t, z)]])
            ands.append(a)
        cnf.append([-c] + ands)
        for a in ands:
            cnf.append([c, -a])
        COINC[key] = c
        return c
    COINC = {}
    rest_pairs = lambda used: [R for R in PAIRS if not set(R) & used]
    # B and D
    for P, Q in itertools.permutations(PAIRS, 2):
        if set(P) & set(Q):
            continue
        Rs = rest_pairs(set(P) | set(Q))
        for s in SIGNS:
            for t in SIGNS:
                cs = [coinc(P, s, Q, t, R) for R in Rs]
                e = y(P, Q, s, t)
                # adjacent (e): exactly 1 coincidence ; else: count formula
                if 'B' in use:
                    for cl in CardEnc.equals(cs, 1, vpool=pool, encoding=EncType.pairwise).clauses:
                        cnf.append([-e] + cl)
                if P < Q and 'D' in use:  # D once per unordered pair
                    # non-adjacent: [phi^{-1}(t) ~ s] + [phi(s) ~ t] + #cs = 2
                    lits = list(cs)
                    for s2 in SIGNS:
                        if adj4(s, s2):
                            lits.append(y(P, Q, s2, t))  # phi(s2) = t with s2 ~ s
                    for t2 in SIGNS:
                        if adj4(t, t2):
                            lits.append(y(P, Q, s, t2))  # phi(s) = t2 with t2 ~ t
                    for cl in CardEnc.equals(lits, 2, vpool=pool, encoding=EncType.seqcounter).clauses:
                        cnf.append([e] + cl)
    # C
    for P, Q in itertools.permutations(PAIRS, 2):
        common = set(P) & set(Q)
        if len(common) != 1 or P > Q or 'C' not in use:
            continue
        (i,) = common
        Rs = rest_pairs(set(P) | set(Q))
        for s in SIGNS:
            for t in SIGNS:
                cs = [coinc(P, s, Q, t, R) for R in Rs]
                want = 1 if sign_at(P, s, i) == sign_at(Q, t, i) else 2
                cnf.extend(CardEnc.equals(cs, want, vpool=pool, encoding=EncType.seqcounter).clauses)
    # E
    for P in (PAIRS if 'E' in use else []):
        free = [c for c in C7 if c not in P]
        for s in SIGNS:
            for m in free:
                lits = []
                for l in free:
                    if l == m:
                        continue
                    Q = tuple(sorted((m, l)))
                    for t in SIGNS:
                        if sign_at(Q, t, m) == 0:
                            lits.append(y(P, Q, s, t))
                cnf.extend(CardEnc.equals(lits, 2, vpool=pool, encoding=EncType.seqcounter).clauses)
    # symmetry breaking
    cnf.append([y((0, 1), (2, 3), (0, 0), (0, 0))])
    if breaksym:
        # u0 = (0,0) in Q_01. (1) fix the near-1-factorisation of K5 on classes 2..6 realised by the triangles at u0
        # (all 6 labelled NFs form one S5-orbit); canonical NF on vertices 0..4 (class = vertex + 2):
        NF = {0: [(1, 2), (3, 4)], 1: [(0, 3), (2, 4)], 2: [(0, 4), (1, 3)], 3: [(0, 2), (1, 4)], 4: [(0, 1), (2, 3)]}
        u0, P0 = (0, 0), (0, 1)
        for d, (e1, e2) in NF.items():
            for ea, eb in ((e1, e2), (e2, e1)):
                K = tuple(sorted((ea[0] + 2, ea[1] + 2)))
                M = tuple(sorted((eb[0] + 2, eb[1] + 2)))
                for z in SIGNS:
                    for w in SIGNS:
                        cnf.append([-y(P0, K, u0, z), -y(P0, M, u0, w), y(K, M, z, w)])
        # (2) sign normalisation by flipping classes 4,5 and 6 (classes 2,3 already used above)
        cnf.append([y(P0, (4, 5), u0, (0, 0))])
        cnf.append([y(P0, (2, 6), u0, (0, 0)), y(P0, (2, 6), u0, (1, 0))])
    return cnf, pool, disjoint, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--iso', action='store_true')
    ap.add_argument('--noniso', action='store_true')
    ap.add_argument('--use', default='BCDE')
    ap.add_argument('--breaksym', action='store_true')
    ap.add_argument('--dimacs', default=None)
    a = ap.parse_args()
    t0 = time.time()
    cnf, pool, disjoint, y = build(a.iso, a.noniso, tuple(a.use), a.breaksym)
    print(f'phi model: {len(disjoint)} bijections, {pool.top} vars, {len(cnf.clauses)} clauses ({time.time()-t0:.1f}s)', flush=True)
    if a.dimacs:
        cnf.to_file(a.dimacs); print('written', a.dimacs, flush=True); return
    S = Cadical153(bootstrap_with=cnf.clauses)
    t1 = time.time()
    ok = S.solve()
    print('result:', 'SAT' if ok else 'UNSAT', f'({time.time()-t1:.1f}s)', flush=True)
    if ok:
        m = set(l for l in S.get_model() if l > 0)
        sol = {f'{P}->{Q}': {str(s): str(t) for s in SIGNS for t in SIGNS if y(P, Q, s, t) in m} for P, Q in disjoint}
        json.dump(sol, open('../data/hamming_phi_solution.json', 'w'), indent=0)
        print('solution saved')


if __name__ == '__main__':
    main()
